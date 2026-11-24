from functools import wraps
from flask import session, redirect, url_for, flash, make_response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access your dashboard.", "alert")
            return redirect(url_for('auth.auth_view'))
        
        response = make_response(f(*args, **kwargs))
        # Prevent caching of private health data
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        return response
    return decorated_function
