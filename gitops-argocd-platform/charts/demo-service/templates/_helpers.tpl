{{- define "demo-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "demo-service.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "demo-service.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
