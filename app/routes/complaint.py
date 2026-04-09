from flask import Blueprint, request, jsonify, session, render_template, url_for,redirect
from app.models import Complaint
from app import db
import os
import time
from werkzeug.utils import secure_filename

complaint_bp = Blueprint('complaint', __name__)

# ✅ Upload page
@complaint_bp.route('/upload')
def upload_page():
    return render_template('upload.html')


@complaint_bp.route('/submit-issue', methods=['POST'])
def submit_issue():
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 401

    image = request.files.get('image')
    description = request.form.get('description')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    address = request.form.get('address')

    print("FILES:", request.files)
    print("FORM:", request.form)

    if not image:
        return jsonify({"error": "No image uploaded"}), 400

    upload_folder = "static/uploads"
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(image.filename)
    filename = str(int(time.time())) + "_" + filename

    file_path = os.path.join(upload_folder, filename)
    image.save(file_path)

    image_path = f"uploads/{filename}"

    new_complaint = Complaint(
        user_id=session['user'],
        image_path=image_path,
        description=description,
        issue_type="general",
        latitude=latitude,
        longitude=longitude,
        address=address
    )

    db.session.add(new_complaint)
    db.session.commit()

    return jsonify({
        "message": "Complaint submitted successfully",
        "redirect": url_for('auth.user_dashboard')
    })


# ✅ Get user's complaints
@complaint_bp.route('/my-complaints')
def my_complaints():
    if 'user' not in session:
        return jsonify([])

    complaints = Complaint.query.filter_by(user_id=session['user']).all()

    data = []
    for c in complaints:
        data.append({
            "id": c.id,
            "image_path": c.image_path,
            "issue_type": c.issue_type,
            "status": c.status,
            "assigned_to": c.assigned_to
        })

    return jsonify(data)


# ✅ Admin: get all complaints
@complaint_bp.route('/all-complaints')
def all_complaints():
    complaints = Complaint.query.all()

    data = []
    for c in complaints:
        data.append({
            "id": c.id,
            "image_path": c.image_path,
            "issue_type": c.issue_type,
            "status": c.status,
            "assigned_to": c.assigned_to
        })

    return jsonify(data)


# ✅ Admin: update status
@complaint_bp.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):
    complaint = Complaint.query.get(id)

    new_status = request.form.get('status')
    complaint.status = new_status

    db.session.commit()

    return jsonify({"message": "Status updated"})