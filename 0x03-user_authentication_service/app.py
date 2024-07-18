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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")