import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from app.routes import login_required
from app.models import create_scan, get_scans_for_user, get_scan_for_user
from app.services.validation import validate_patient_form, validate_image_file
from app.services.storage import save_uploaded_image
from app.services.predictor import predict
from app.services.locations import search_locations

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/locations/search', methods=['GET'])
def search_locations_api():
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    results = search_locations(query)
    return jsonify(results)

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_view():
    user_id = session['user_id']
    scans = get_scans_for_user(user_id)

    selected_scan_id = request.args.get('scan_id')
    current_scan = None
    if selected_scan_id:
        current_scan = get_scan_for_user(selected_scan_id, user_id)
    elif scans:
        # Default to showing latest scan in result panel if requested or just scanned
        if request.args.get('show_latest') == '1':
            current_scan = scans[0]

    return render_template('dashboard.html', scans=scans, current_scan=current_scan)

@dashboard_bp.route('/scan', methods=['POST'])
@login_required
def create_scan_view():
    user_id = session['user_id']

    name = request.form.get('patient_name', '')
    age = request.form.get('patient_age', '')
    place = request.form.get('patient_place', '')
    city = request.form.get('patient_city', '')
    state = request.form.get('patient_state', '')
    country = request.form.get('patient_country', '')
    image = request.files.get('image')

    cleaned_data, form_errors = validate_patient_form(name, age, place)
    img_valid, img_error = validate_image_file(image)

    all_errors = list(form_errors)
    if not img_valid:
        all_errors.append(img_error)

    if all_errors:
        for err in all_errors:
            flash(err, "alert")
        scans = get_scans_for_user(user_id)
        return render_template(
            'dashboard.html',
            scans=scans,
            current_scan=None,
            form_data={'patient_name': name, 'patient_age': age, 'patient_place': place}
        ), 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    saved_filename = save_uploaded_image(image, upload_folder)
    image_full_path = os.path.join(upload_folder, saved_filename)

    # Predictor call
    prediction = predict(image_full_path)

    scan_id = create_scan(
        user_id=user_id,
        patient_name=cleaned_data['name'],
        patient_age=cleaned_data['age'],
        patient_place=cleaned_data['place'],
        image_filename=saved_filename,
        status=prediction['status'],
        hemoglobin=prediction['hemoglobin'],
        confidence=prediction.get('confidence'),
        is_placeholder=prediction.get('is_placeholder', True),
        patient_city=city,
        patient_state=state,
        patient_country=country
    )

    flash("Scan analysis completed successfully.", "success")
    return redirect(url_for('dashboard.dashboard_view', scan_id=scan_id))
