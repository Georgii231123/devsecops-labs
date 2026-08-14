# Promotion workflow

1. A build produces an immutable image tag such as a release version or commit SHA.
2. Dev values are updated through a pull request.
3. CI renders and validates the chart.
4. Argo CD reconciles dev after merge.
5. After verification, a second pull request updates the prod image tag to the exact validated artifact.
6. Argo CD reconciles production from Git.

Production never tracks `latest`, and promotion does not rebuild the application artifact.
