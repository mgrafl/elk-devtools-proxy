# ELK DevTools Proxy

A minimal HTTP proxy for forwarding Elasticsearch API calls to the Kibana DevTools Console API. 

Designed for containerized environments and supports flexible authentication and SSL options.

## Features
- Forwards all HTTP methods and paths to Kibana DevTools Console API
- Supports query parameters and request bodies
- Optional SSL verification skipping
- Configurable logging level
- Optional credential header for authentication (read from stdin, configurable header name)

## Usage


### Build the Docker image
```
docker build -t mgrafl/elk-devtools-proxy .
```


### Run the container
```
docker run -p 8080:8080 \
  -e KIBANA_URL=https://your-kibana-server/kibana \
  [-e INSECURE_SKIP_VERIFY=1] \
  [-e CREDENTIAL_HEADER_NAME=Cookie] \
  [-e LOG_LEVEL=DEBUG] \
  mgrafl/elk-devtools-proxy
```

- `KIBANA_URL` (required): URL of the Kibana instance (default: http://kibana:5601)
- `LOG_LEVEL` (optional): Python log level (e.g., DEBUG, INFO, WARNING)
- `CREDENTIAL_HEADER_NAME` (optional): Name of the HTTP header to add for authentication (e.g., "Authorization" or "Cookie"). If set, you will be prompted to enter the value on startup.
- `INSECURE_SKIP_VERIFY` (optional): Set to 1 to skip SSL certificate verification


## Examples

Self-removing container without further authentication:
```
docker run --rm -e KIBANA_URL=https://your-kibana-server/kibana -p 8080:8080 mgrafl/elk-devtools-proxy
```


Self-removing container skipping server certificate verification, using "Cookie" credential header, logging at debug level:
```
docker run --rm -i -e KIBANA_URL=https://your-kibana-server/kibana -e INSECURE_SKIP_VERIFY=1 -e CREDENTIAL_HEADER_NAME=Cookie -e LOG_LEVEL=DEBUG -p 8080:8080 mgrafl/elk-devtools-proxy
```
