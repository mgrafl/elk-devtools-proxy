# syntax=docker/dockerfile:1
#
# Optional environment variables:
#   KIBANA_URL             (required) URL of the Kibana instance (default: http://kibana:5601)
#   INSECURE_SKIP_VERIFY   (optional) Set to 1 to skip SSL certificate verification
#   CREDENTIAL_HEADER_NAME (optional) Name of the HTTP header to add for authentication (e.g., "Authorization" or "Cookie")
#                                     If set, the value will be read from stdin when the container starts.
#   LOG_LEVEL              (optional) Python log level (e.g., DEBUG, INFO, WARNING)
#
FROM python:3.14-alpine
WORKDIR /app
COPY proxy.py .
RUN pip install flask requests
ENV KIBANA_URL=http://kibana:5601
EXPOSE 8080
CMD ["python", "-u", "proxy.py"]
