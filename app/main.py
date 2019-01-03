from app.views import app2
from flask import jsonify, render_template


@app2.route('/user/login', methods=['GET'])
def login():
    """Render user login page"""
    return render_template('index.html')

@app2.route('/user/register', methods=['GET'])
def register_user():
    """Render user register page."""
    return render_template('SignUp.html')

