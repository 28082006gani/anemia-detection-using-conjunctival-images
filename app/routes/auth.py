from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import get_user_by_email, create_user
from app.services.validation import validate_registration
from app import limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def auth_view():
    if session.get('user_id'):
        return redirect(url_for('dashboard.dashboard_view'))
    
    active_tab = request.args.get('tab', 'login')
    if active_tab not in ('login', 'register'):
        active_tab = 'login'
        
    return render_template('auth.html', active_tab=active_tab)

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def login():
    if session.get('user_id'):
        return redirect(url_for('dashboard.dashboard_view'))

    if request.method == 'GET':
        return render_template('auth.html', active_tab='login')

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        flash("Email and password are required.", "alert")
        return render_template('auth.html', active_tab='login', email=email), 400

    user = get_user_by_email(email)
    if not user or not check_password_hash(user['password_hash'], password):
        flash("Email or password is incorrect.", "alert")
        return render_template('auth.html', active_tab='login', email=email), 401

    session.clear()
    session['user_id'] = user['id']
    session['user_email'] = user['email']
    session.permanent = True

    return redirect(url_for('dashboard.dashboard_view'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@auth_bp.route('/signup', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def register():
    if session.get('user_id'):
        return redirect(url_for('dashboard.dashboard_view'))

    if request.method == 'GET':
        return render_template('auth.html', active_tab='register')

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    errors = validate_registration(email, password, confirm_password)
    if errors:
        for err in errors:
            flash(err, "alert")
        return render_template('auth.html', active_tab='register', email=email), 400

    existing = get_user_by_email(email)
    if existing:
        flash("An account with this email already exists.", "alert")
        return render_template('auth.html', active_tab='register', email=email), 400

    password_hash = generate_password_hash(password)
    user = create_user(email, password_hash)

    # Automatically sign in new user
    session.clear()
    session['user_id'] = user['id']
    session['user_email'] = user['email']
    session.permanent = True

    flash("Account registered successfully. Welcome to AnemiaScan!", "success")
    return redirect(url_for('dashboard.dashboard_view'))

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for('auth.auth_view'))
