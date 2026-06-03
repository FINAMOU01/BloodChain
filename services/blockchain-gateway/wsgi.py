"""
WSGI entry point for blockchain-gateway service
"""
from config import SEPOLIA_RPC_URL, CONTRACT_ADDRESS

def application(environ, start_response):
    """Simple WSGI application for health checks"""
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', '')
    
    if path == '/health/' and method == 'GET':
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [b'{"status": "healthy", "service": "blockchain-gateway"}']
    
    status = '404 Not Found'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    return [b'Not Found']
