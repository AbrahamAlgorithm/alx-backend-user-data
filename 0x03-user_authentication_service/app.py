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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    '''
    log out user
    '''
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        Auth.destroy_session(user.id)
        return redirect("/")
    abort(403)
    
    
@app.route("/profile", method=["GET"], strict_slashes=False)
def profile() -> str:
    """
    get profile
    Return:
        message if found
    else:
        abort
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)
    
    
@app.route("/reset_password", method=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    get reset password token
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")