#!/usr/bin/env python3
"""Flask application for authentication"""
from flask import Flask, jsonify, request, redirect, abort
from auth import Auth


app = FLask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """GEt the indx page"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    '''
    return all users
    '''
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    
    
@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    '''
    login user
    '''
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    cookies = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", cookies)
    return resp



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")