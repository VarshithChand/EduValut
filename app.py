from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = 'uploads'
USER_DATA_FILE = 'users.txt'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xlsx', 'csv', 'ppt', 'pptx', 'mp4', 'avi', 'zip', 'rar'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

USER_DATA = {}
SUPERUSER_DATA = {"varshith": "1234"}
COURSES = ["Python", "Java", "C", "C++"]

# Load users from file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    username, password = line.strip().split(',')
                    USER_DATA[username] = password

# Save users to file
def save_user_data():
    with open(USER_DATA_FILE, 'w') as f:
        for username, password in USER_DATA.items():
            f.write(f"{username},{password}\n")

load_user_data()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_folder(username):
    path = os.path.join(app.config['UPLOAD_FOLDER'], username)
    os.makedirs(path, exist_ok=True)
    return path

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USER_DATA and password == USER_DATA[username]:
            session["username"] = username
            session["is_superuser"] = False
            return redirect(url_for("welcome"))
        elif username in SUPERUSER_DATA and password == SUPERUSER_DATA[username]:
            session["username"] = username
            session["is_superuser"] = True
            return redirect(url_for("superuser_dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/welcome")
def welcome():
    if "username" in session and not session.get("is_superuser"):
        username = session["username"]
        user_folder = get_user_folder(username)
        uploaded_files = os.listdir(user_folder)

        # Include superuser uploads in updates
        superuser_folder = get_user_folder("varshith")
        superuser_files = os.listdir(superuser_folder) if os.path.exists(superuser_folder) else []

        return render_template("welcome.html",
                               username=username,
                               files=uploaded_files,
                               superuser_files=superuser_files)
    return redirect(url_for("login"))

@app.route("/courses", methods=["GET", "POST"])
def courses():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST" and session.get("is_superuser"):
        action = request.form.get("action")
        course_name = request.form.get("course_name", "").strip()
        if course_name:
            if action == "add" and course_name not in COURSES:
                COURSES.append(course_name)
            elif action == "delete" and course_name in COURSES:
                COURSES.remove(course_name)

    return render_template("courses.html", courses=COURSES, is_superuser=session.get("is_superuser"))

@app.route("/uploads", methods=["GET", "POST"])
def uploads():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    is_superuser = session.get("is_superuser")
    user_folder = get_user_folder(username)

    if request.method == "POST":
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder, filename))
            return redirect(url_for("uploads"))

    files = os.listdir(user_folder)
    dashboard_url = url_for('superuser_dashboard') if is_superuser else url_for("welcome")

    superuser_files = []
    if not is_superuser:
        superuser_folder = get_user_folder("varshith")
        superuser_files = os.listdir(superuser_folder) if os.path.exists(superuser_folder) else []

    return render_template("uploads.html", files=files, dashboard_url=dashboard_url, superuser_files=superuser_files)

@app.route("/delete_files", methods=["POST"])
def delete_files():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    is_superuser = session.get("is_superuser")
    target_user = request.form.get("target_user", username)

    if not is_superuser and username != target_user:
        return "Unauthorized", 403

    user_folder = get_user_folder(target_user)
    selected_files = request.form.getlist("selected_files")

    for file in selected_files:
        file_path = os.path.join(user_folder, file)
        if os.path.exists(file_path):
            os.remove(file_path)

    return redirect(url_for("uploads"))

@app.route("/serve_file/<username>/<filename>")
def serve_file(username, filename):
    if "username" not in session:
        return redirect(url_for("login"))

    file_folder = get_user_folder(username)
    file_path = os.path.join(file_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(file_folder, filename)
    return "File not found or unauthorized", 404

@app.route("/superuser_dashboard")
def superuser_dashboard():
    if "username" in session and session.get("is_superuser"):
        users = list(USER_DATA.keys())
        user_files = {user: os.listdir(get_user_folder(user)) for user in users}
        return render_template("superuser_dashboard.html", users=users, user_files=user_files)
    return redirect(url_for("login"))

@app.route("/manage_users", methods=["POST"])
def manage_users():
    if "username" in session and session.get("is_superuser"):
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")
        if action == "add" and username and password:
            USER_DATA[username] = password
            save_user_data()
        elif action == "delete" and username in USER_DATA:
            del USER_DATA[username]
            save_user_data()
    return redirect(url_for("superuser_dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
