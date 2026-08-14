def call(Closure body) {
    def config = [:]
    body.resolveStrategy = Closure.DELEGATE_FIRST
    body.delegate = config
    body()

    pipeline {
        agent { label 'linux-docker' }
        options {
            timestamps()
            disableConcurrentBuilds()
            buildDiscarder(logRotator(numToKeepStr: '20'))
        }
        environment {
            IMAGE_TAG = "${env.GIT_COMMIT ?: 'local'}"
        }
        stages {
            stage('Quality') {
                steps {
                    sh 'test -f Dockerfile'
                    sh 'python3 -m compileall .'
                }
            }
            stage('Build') {
                steps {
                    sh "docker build --pull -t ${config.imageRepository}:${IMAGE_TAG} ."
                }
            }
            stage('Security') {
                steps {
                    sh "trivy image --exit-code 1 --severity CRITICAL ${config.imageRepository}:${IMAGE_TAG}"
                    sh "syft ${config.imageRepository}:${IMAGE_TAG} -o cyclonedx-json > sbom.json"
                }
            }
            stage('Publish') {
                when { branch 'main' }
                steps {
                    sh "docker push ${config.imageRepository}:${IMAGE_TAG}"
                    archiveArtifacts artifacts: 'sbom.json', fingerprint: true
                }
            }
            stage('Production approval') {
                when { branch 'main' }
                input {
                    message "Deploy ${config.serviceName}:${IMAGE_TAG} to ${config.productionEnvironment}?"
                    ok 'Deploy'
                }
                steps {
                    echo "Deployment is performed by the GitOps repository using immutable tag ${IMAGE_TAG}."
                }
            }
        }
    }
}
