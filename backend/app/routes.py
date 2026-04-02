import os
from flask import Blueprint, render_template, request, redirect, url_for, send_file, session, flash, jsonify, current_app
from .extensions import mongo
from bson.objectid import ObjectId
import gridfs
import io
import bcrypt

from datetime import datetime

main_bp = Blueprint('main', __name__)

# Authentication decorator for admin-only routes
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please login as admin to access this page', 'error')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Student Login Required Decorator
def student_required(f):
    def decorated_function(*args, **kwargs):
        if 'student_logged_in' not in session:
            flash('Please login as a student to access this page.', 'info')
            return redirect(url_for('main.student_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# General login required (Either Admin or Student)
def portal_login_required(f):
    def decorated_function(*args, **kwargs):
        if 'student_logged_in' not in session and 'admin_logged_in' not in session:
            flash('Please login or signup to view study materials.', 'info')
            return redirect(url_for('main.student_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Student Signup
@main_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        if not username or len(username) < 3:
            flash("Username must be at least 3 characters long.", "error")
            return redirect(url_for("main.signup"))
            
        if not password or len(password) < 6:
            flash("Password must be at least 6 characters long for your safety.", "error")
            return redirect(url_for("main.signup"))
        
        if mongo.db.students.find_one({"username": username}):
            flash("That username is taken. Try something else!", "error")
            return redirect(url_for("main.signup"))
            
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        mongo.db.students.insert_one({
            "username": username,
            "password": hashed_password,
            "favorites": [],
            "created_at": datetime.now()
        })
        flash("Welcome to StudyPortal! Please login to continue.", "success")
        return redirect(url_for("main.student_login"))
        
    return render_template("signup.html")

# Student Login
@main_bp.route("/student/login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        student = mongo.db.students.find_one({"username": username})
        if student and bcrypt.checkpw(password.encode('utf-8'), student["password"]):
            session['student_logged_in'] = True
            session['student_id'] = str(student["_id"])
            session['username'] = username
            flash(f"Nice to see you again, {username}!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid credentials. Please check your username and password.", "error")
            
    return render_template("student_login.html")

# Student Favorites
@main_bp.route("/favorites")
@student_required
def favorites():
    student = mongo.db.students.find_one({"_id": ObjectId(session['student_id'])})
    fav_ids = student.get('favorites', [])
    
    files = list(mongo.db.files.find({"file_id": {"$in": [ObjectId(f) for f in fav_ids]}}))
    for f in files:
        f["file_id"] = str(f["file_id"])
        
    return render_template("favorites.html", files=files)

@main_bp.route("/favorite/toggle/<file_id>")
@student_required
def toggle_favorite(file_id):
    student_id = ObjectId(session['student_id'])
    
    student = mongo.db.students.find_one({"_id": student_id})
    favorites = student.get('favorites', [])
    
    if file_id in favorites:
        mongo.db.students.update_one({"_id": student_id}, {"$pull": {"favorites": file_id}})
        flash("Removed from favorites.", "info")
    else:
        mongo.db.students.update_one({"_id": student_id}, {"$push": {"favorites": file_id}})
        flash("Added to favorites!", "success")
        
    # Redirect back to where they were
    return redirect(request.referrer or url_for('main.home'))

def get_fs():
    """Helper to get GridFS instance from current mongo connection"""
    return gridfs.GridFS(mongo.db)

# Admin Notifications
@main_bp.route("/admin/notify", methods=["GET", "POST"])
@admin_required
def admin_notify():
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            mongo.db.notifications.insert_one({
                "message": message,
                "created_at": datetime.now()
            })
            flash("Notification posted successfully!", "success")
        return redirect(url_for('main.admin_dashboard'))
    
    notices = list(mongo.db.notifications.find().sort("created_at", -1))
    return render_template("admin_notify.html", notices=notices)


# Home (Welcome page)
# Admin Dashboard Analytics
@main_bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    # Total files
    total_files = mongo.db.files.count_documents({})
    
    # Most popular files (limit to top 5)
    popular_files = list(mongo.db.files.find().sort("downloads", -1).limit(5))
    for f in popular_files:
        f["file_id"] = str(f["file_id"])
        
    # Semester distribution for stats
    sem_stats = {}
    for sem in ["SEM1", "SEM2", "SEM3", "SEM4", "SEM5", "SEM6", "SEM7", "SEM8"]:
        sem_stats[sem] = mongo.db.files.count_documents({"semester": sem})
        
    return render_template("admin_dashboard.html", 
                         total_files=total_files,
                         popular_files=popular_files,
                         sem_stats=sem_stats)

@main_bp.route("/")
def home():
    notices = list(mongo.db.notifications.find().sort("created_at", -1).limit(3))
    return render_template("welcome.html", notices=notices)

# Semesters page
@main_bp.route("/semesters")
@portal_login_required
def semesters():
    semesters_list = [
        {"id": "SEM1", "name": "Semester 1", "subtitle": "Basic Engineering Sciences", "desc": "Foundation subjects including Mathematics, Physics, BEE, and Engineering Graphics."},
        {"id": "SEM2", "name": "Semester 2", "subtitle": "Engineering Fundamentals", "desc": "Core engineering subjects including Chemistry, Engineering Mechanics, and Programming."},
        {"id": "SEM3", "name": "Semester 3", "subtitle": "Core IT Foundations", "desc": "Access study materials for Semester 3 including Data Structures, OOPS, and more."},
        {"id": "SEM4", "name": "Semester 4", "subtitle": "Advanced Concepts", "desc": "Explore materials for Semester 4 covering Advanced Programming, DBMS, and CG."},
        {"id": "SEM5", "name": "Semester 5", "subtitle": "Specialized IT Domains", "desc": "Access materials for Semester 5 including OS, CN, ML, and Advanced DBMS."},
        {"id": "SEM6", "name": "Semester 6", "subtitle": "Advanced Topics", "desc": "Materials for Semester 6 covering Emerging Technologies and Capstone Projects."},
        {"id": "SEM7", "name": "Semester 7", "subtitle": "Professional Electives", "desc": "Advanced topics including ISR, SPM, Deep Learning, and Mobile Computing."},
        {"id": "SEM8", "name": "Semester 8", "subtitle": "Entrepreneurship", "desc": "Final semester covering Distributed Systems and Startup development."}
    ]
    
    # Calculate unique subject counts per semester
    for sem in semesters_list:
        subjects_count = len(mongo.db.files.distinct("subject", {"semester": sem["id"]}))
        sem["subjects_count"] = subjects_count

    return render_template("semesters.html", semesters=semesters_list)

# Contact
@main_bp.route("/contact")
def contact():
    return render_template("contact.html")

# Login (Admin only)
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Get admin credentials from environment variables
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH', '')
        admin_password_plain = os.environ.get('ADMIN_PASSWORD', '')

        # Verify credentials
        if username != admin_username:
            error = "Invalid username. Admin account not found."
        else:
            # Username is correct, now check password
            is_valid = False
            if admin_password_hash:
                try:
                    if bcrypt.checkpw(password.encode('utf-8'), admin_password_hash.encode('utf-8')):
                        is_valid = True
                except Exception as e:
                    if admin_password_plain and password == admin_password_plain:
                        is_valid = True
            elif admin_password_plain and password == admin_password_plain:
                is_valid = True
            
            if is_valid:
                session['admin_logged_in'] = True
                session['username'] = username
                flash('Successfully logged in as admin!', 'success')
                return redirect(url_for("main.admin_dashboard"))
            else:
                error = "Incorrect password. Please try again."

    return render_template("login.html", error=error)

# Logout route
@main_bp.route("/logout")
def logout():
    session.pop('admin_logged_in', None)
    session.pop('student_logged_in', None)
    session.pop('student_id', None)
    session.pop('username', None)
    flash('Successfully logged out', 'success')
    return redirect(url_for('main.home'))

# Upload PDF (Admin Only)
@main_bp.route("/upload", methods=["GET", "POST"])
@admin_required
def upload():
    fs = get_fs()
    if request.method == "POST":
        file = request.files["pdf"]
        semester = request.form.get("semester")
        subject = request.form.get("subject")

        if file and file.filename.endswith(".pdf"):
            file_id = fs.put(file, filename=file.filename)
            mongo.db.files.insert_one({
                "file_id": file_id,
                "filename": file.filename,
                "semester": semester,
                "subject": subject
            })
            flash('PDF uploaded successfully!', 'success')
            return redirect(url_for("main.view_pdfs"))
        else:
            flash('Please select a valid PDF file', 'error')
    return render_template("upload.html")

@main_bp.route("/pdfs")
@portal_login_required
def view_pdfs():
    # Get unique subjects for filter dropdown
    all_subjects = sorted(mongo.db.files.distinct("subject"))
    
    # Get selected subject from query param
    selected_subject = request.args.get('subject')
    
    query = {}
    if selected_subject and selected_subject != "All":
        query['subject'] = selected_subject
        
    files = list(mongo.db.files.find(query).sort("semester", 1))
    
    for f in files:
        f["file_id"] = str(f["file_id"])
        
    return render_template("view_pdfs.html", 
                         files=files, 
                         subjects=all_subjects, 
                         selected_subject=selected_subject)

# View all subjects for a specific semester
@main_bp.route("/pdfs/<semester>")
@portal_login_required
def view_semester_subjects(semester):
    subjects = mongo.db.files.distinct("subject", {"semester": semester})
    semester_info = {
        "SEM1": {"name": "Semester 1", "subjects": ["M1", "Physics", "BEE", "FPL", "EG"]},
        "SEM2": {"name": "Semester 2", "subjects": ["Chemistry", "EM", "M2", "PPS", "BXE"]},
        "SEM3": {"name": "Semester 3", "subjects": ["DM", "LDCO", "DSA", "OOPS", "BCN"]},
        "SEM4": {"name": "Semester 4", "subjects": ["M3", "PA", "DBMS", "CG", "SE"]},
        "SEM5": {"name": "Semester 5", "subjects": ["OS", "TOC", "ML", "HCI", "ADMBS"]},
        "SEM6": {"name": "Semester 6", "subjects": ["CNS", "DSBDA", "WAD"]},
        "SEM7": {"name": "Semester 7", "subjects": ["ISR", "SPM", "DL", "Mobile Computing", "Wireless Communication"]},
        "SEM8": {"name": "Semester 8", "subjects": ["DS", "STARTUP", "Blockchain Technology", "NLP"]}
    }

    semester_data = semester_info.get(semester, {"name": semester, "subjects": []})
    subject_files = {}
    for subject in semester_data["subjects"]:
        count = mongo.db.files.count_documents({"semester": semester, "subject": subject})
        subject_files[subject] = count

    return render_template("semester_subjects.html",
                         semester=semester,
                         semester_name=semester_data["name"],
                         subjects=semester_data["subjects"],
                         subject_files=subject_files)

# View PDFs for a specific semester + subject
@main_bp.route("/pdfs/<semester>/<subject>")
@portal_login_required
def view_subject_pdfs(semester, subject):
    files = list(mongo.db.files.find({"semester": semester, "subject": subject}))
    for f in files:
        f["file_id"] = str(f["file_id"])
    return render_template("subject_pdfs.html", files=files, semester=semester, subject=subject)

# Global Search for Materials
@main_bp.route("/search")
@portal_login_required
def search():
    query_str = request.args.get('q', '').strip()
    if not query_str:
        return redirect(url_for('main.home'))
        
    search_query = {
        "$or": [
            {"subject": {"$regex": query_str, "$options": "i"}},
            {"filename": {"$regex": query_str, "$options": "i"}},
            {"semester": {"$regex": query_str, "$options": "i"}}
        ]
    }
    
    files = list(mongo.db.files.find(search_query))
    for f in files:
        f["file_id"] = str(f["file_id"])
        
    return render_template("search_results.html", query=query_str, files=files)

# Download/View PDF - Public Access
@main_bp.route("/pdf/<file_id>")
@portal_login_required
def get_pdf(file_id):
    fs = get_fs()
    try:
        # Get file metadata to increment download count
        file_meta = mongo.db.files.find_one({"file_id": ObjectId(file_id)})
        if file_meta:
            mongo.db.files.update_one(
                {"_id": file_meta["_id"]},
                {"$inc": {"downloads": 1}}
            )

        file_obj = fs.get(ObjectId(file_id))
        return send_file(io.BytesIO(file_obj.read()), 
                       download_name=file_obj.filename, 
                       mimetype="application/pdf")
    except Exception as e:
        flash('File not found or corrupted', 'error')
        return redirect(url_for('main.view_pdfs'))

@main_bp.route("/delete/<file_id>")
@admin_required
def delete_pdf(file_id):
    try:
        file_oid = ObjectId(file_id)
        get_fs().delete(file_oid)
        mongo.db.files.delete_one({"file_id": file_oid})
        flash("Study Material deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting material: {str(e)}", "error")
    
    return redirect(request.referrer or url_for('main.semesters'))
