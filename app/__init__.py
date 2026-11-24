import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    default_db_path = os.path.join(base_dir, 'instance', 'app.db')
    default_upload_folder = os.path.join(base_dir, 'private_uploads')

    max_mb = int(os.environ.get('MAX_UPLOAD_MB', 5))
    session_idle_minutes = int(os.environ.get('SESSION_IDLE_MINUTES', 30))
    cookie_secure = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-anemiascan'),
        DATABASE_PATH=os.environ.get('DATABASE_PATH', default_db_path),
        UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', default_upload_folder),
        MAX_CONTENT_LENGTH=max_mb * 1024 * 1024,
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=session_idle_minutes),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=cookie_secure,
    )

    if test_config:
        app.config.update(test_config)

    # Ensure required directories exist
    os.makedirs(os.path.dirname(app.config['DATABASE_PATH']), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    csrf.init_app(app)
    limiter.init_app(app)

    # Initialize database
    from app.models import init_app as init_db_app
    init_db_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reports_bp)

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "img-src 'self' data: blob:; "
            "media-src 'self' blob:; "
            "style-src 'self'; "
            "script-src 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

    # Custom error handlers
    @app.errorhandler(400)
    def bad_request_error(e):
        return render_template('errors/400.html', error=e), 400

    @app.errorhandler(403)
    def forbidden_error(e):
        return render_template('errors/403.html', error=e), 403

    @app.errorhandler(404)
    def not_found_error(e):
        return render_template('errors/404.html', error=e), 404

    @app.errorhandler(413)
    def payload_too_large_error(e):
        return render_template('errors/413.html', error=e), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html', error=e), 500

    return app
