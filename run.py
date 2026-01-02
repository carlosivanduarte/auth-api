#!/usr/bin/env python
import json
import os

import datetime
import jwt
import requests
from flask import Flask, jsonify
from flask import current_app
from flask import request

app = Flask(__name__)

# In-memory user database
with open(os.path.join(os.path.dirname(__file__), 'users.json'), 'rb') as f:
    users = json.load(f)


@app.route('/token', methods=['POST'])
def create_token():
    """
    Authenticates a user by username and password, returning an authentication token (valid for 30s)
    that can be used to make authenticated requests to other microservices.
    """
    username: str = request.form.get('username')
    password: str = request.form.get('password')

    if not username:
        return jsonify(error='Username is blank'), 422
    if not password:
        return jsonify(error='Password is blank'), 422

    for user in users:
        # Find user by username
        if user['username'] == username:
            # Validate password
            if user['password'] == password:
                payload = {
                    'user_id': user['id'],
                    'username': user['username'],
                    'can_transact': user['can_transact'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
                }

                token = jwt.encode(
                    payload,
                    current_app.config['JWT_SECRET'],
                    algorithm='HS256',
                )

                return jsonify(token=token)
            else:
                return jsonify(error='Invalid password'), 401
    else:
        return jsonify(error='User not found'), 404


@app.route('/health')
def health():
    return jsonify(healthy=True)


@app.route('/token', methods=['GET'])
def check_token():
    """
    Validates a JWT token and returns only validation status.
    Token should be provided in the Authorization header as 'Bearer <token>'.
    Returns minimal information to prevent information disclosure attacks.
    """
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return '', 401
    
    try:
        token = auth_header.split(' ', 1)[1]  # split only once
    except IndexError:
        return '', 401
    
    try:
        # Decode and validate the token
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET'],
            algorithms=['HS256']
        )
        
        # HTTP 200 indicates token is valid
        return '', 200
        
    except jwt.ExpiredSignatureError:
        return '', 401
    except jwt.InvalidTokenError:
        return '', 401

if __name__ == '__main__':
    # Env
    http_port: int = int(os.getenv('HTTP_PORT', 5000))
    jwt_secret: str = os.environ['JWT_SECRET']

    # Flask config
    app.config['JWT_SECRET'] = jwt_secret

    # Run app
    app.run(host='0.0.0.0', port=http_port, threaded=True)
