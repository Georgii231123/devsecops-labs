FROM golang:1.26 AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /operator ./cmd

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /operator /operator
USER 65532:65532
ENTRYPOINT ["/operator"]
