import requests
from flask import Flask, request, Response
import random
import os

app = Flask(__name__)

# Feature toggle for movies endpoint (can be dynamically controlled)
#feature_toggle = 50  # mc moovies requests percentage
feature_toggle = int(os.environ.get('MOVIES_MIGRATION_PERCENT'))
#print('new ft =' + os.environ.get('FEATURE_TOGGLE'))
# Base URLs for the various services
MONOLITH = "http://monolith:8080/"
MOVIES_MC = "http://movies-service:8081/"
#EVENTS_SERVER = "http://events-service:8082/"

@app.route('/api/movies', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_movies():
    # Choose the server based on the feature toggle
    ft_selector = random.random()*100 < max(0, min(100, feature_toggle))
    if ft_selector:
        target_url = MOVIES_MC
    else:
        target_url = MONOLITH

    # Forward the request to the target server
    return forward_request(target_url)

@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_events():
    return forward_request(MONOLITH)

@app.route('/api/payments', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_events():
    return forward_request(MONOLITH)

@app.route('/api/subscriptions', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_events():
    return forward_request(MONOLITH)

@app.route('/health')
def health():
    return "Strangler Fig Proxy is healthy"

def forward_request(target_url):
    # Get the original request's URL and body
    original_url = request.url.replace(request.host_url, target_url)
    method = request.method
    headers = {key: value for key, value in request.headers.items() if key != 'Host'}
    print(headers, flush=True)
    # Forward the request to the target server
    response = requests.request(
        method=method,
        url=original_url,
        headers=headers,
        data=request.get_data(),
        allow_redirects=False,
        stream=True
    )

    
    # Return the response from the target server back to the client
    return Response(response.content, status=response.status_code, headers={'Content-Type': 'application/json'}) #, headers=dict(response.headers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
