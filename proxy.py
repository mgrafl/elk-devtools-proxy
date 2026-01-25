import logging
from flask import Flask, request, Response
import requests
import os
import sys

KIBANA_URL = os.environ.get('KIBANA_URL', 'http://kibana:5601')
KIBANA_API = '/api/console/proxy'

# Optionally skip SSL verification
INSECURE_SKIP_VERIFY = os.environ.get('INSECURE_SKIP_VERIFY', '0') == '1'

# Optionally read a credential header value from stdin if CREDENTIAL_HEADER env var is set
CREDENTIAL_HEADER_NAME = os.environ.get('CREDENTIAL_HEADER_NAME')
CREDENTIAL_HEADER_VALUE = None
if CREDENTIAL_HEADER_NAME:
    try:
        prompt = f"Enter value for {CREDENTIAL_HEADER_NAME} header (or leave blank): "
        print(prompt, end='', flush=True)
        line = sys.stdin.readline().strip()
        if line:
            CREDENTIAL_HEADER_VALUE = line
    except Exception:
        pass

# Configure logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Accept any path and method for proxying
@app.route('/', defaults={'es_path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:es_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy_any(es_path):
    # Forward the request to Kibana DevTools Console API
    # Always forward the request body as-is
    es_body = request.data if request.data else None
    method = request.method
    path = '/' + es_path
    # Append original query string to path if present
    if request.query_string:
        path += '?' + request.query_string.decode()
    # Log the outgoing request (debug only), set environment variable LOG_LEVEL=DEBUG to enable
    logger.debug(f"Proxying to Kibana: {KIBANA_URL + KIBANA_API}?method={method}&path={path}")
    logger.debug(f"Body: {es_body}")
    # Prepare headers for Kibana
    kibana_headers = {'kbn-xsrf': 'true'}
    if CREDENTIAL_HEADER_NAME and CREDENTIAL_HEADER_VALUE:
        kibana_headers[CREDENTIAL_HEADER_NAME] = CREDENTIAL_HEADER_VALUE
    resp = requests.post(
        KIBANA_URL + KIBANA_API,
        params={'method': method, 'path': path},
        data=es_body,
        headers=kibana_headers,
        verify=not INSECURE_SKIP_VERIFY
    )
    # Log the response from Kibana (debug only)
    logger.debug(f"Response status: {resp.status_code}")
    logger.debug(f"Response headers: {dict(resp.headers)}")
    logger.debug(f"Response body: {resp.text}")
    # Prepare headers for the client
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]

    # Return a proper Flask Response
    return Response(resp.content, resp.status_code, headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
