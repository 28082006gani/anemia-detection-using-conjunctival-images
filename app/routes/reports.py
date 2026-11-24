from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort, send_file, current_app
from app.routes import login_required
from app.models import get_scan_for_user, delete_scan_for_user
from app.services.storage import get_image_path, delete_image_file

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/report/<scan_id>', methods=['GET'])
@login_required
def view_report(scan_id):
    user_id = session['user_id']
    scan = get_scan_for_user(scan_id, user_id)
    if not scan:
        # Rule: Return 404 (not 403) to prevent resource enumeration
        abort(404)

    return render_template('report.html', scan=scan)

@reports_bp.route('/report/<scan_id>/image', methods=['GET'])
@login_required
def serve_scan_image(scan_id):
    user_id = session['user_id']
    scan = get_scan_for_user(scan_id, user_id)
    if not scan:
        abort(404)

    upload_folder = current_app.config['UPLOAD_FOLDER']
    image_path = get_image_path(scan['image_filename'], upload_folder)
    if not image_path:
        abort(404)

    response = send_file(image_path, mimetype='image/jpeg', as_attachment=False)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Disposition'] = f'inline; filename="scan-{scan_id}.jpg"'
    response.headers['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
    return response

@reports_bp.route('/report/<scan_id>/delete', methods=['POST'])
@login_required
def delete_report(scan_id):
    user_id = session['user_id']
    filename = delete_scan_for_user(scan_id, user_id)
    if not filename:
        abort(404)

    upload_folder = current_app.config['UPLOAD_FOLDER']
    delete_image_file(filename, upload_folder)

    flash("Report and associated conjunctival image deleted permanently.", "success")
    return redirect(url_for('dashboard.dashboard_view'))
