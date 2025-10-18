from flask import Flask, render_template, request, session, jsonify
from models import create_user, find_user_by_email, get_all_careers, get_career_by_id, get_db_connection
from recommender import recommend
import bcrypt
from config import SECRET_KEY, SESSION_TYPE
from flask_session import Session

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = SECRET_KEY
app.config['SESSION_TYPE'] = SESSION_TYPE
Session(app)


# ----------------- ROUTES -----------------

@app.route('/')
def index():
    return render_template('index.html')


# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.get_json() or request.form
    first = data.get('first_name')
    last = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    education = data.get('education')
    cgpa = data.get('cgpa') or None

    if not (first and email and password):
        return jsonify({'error': 'Missing required fields'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        uid = create_user(first, last, email, hashed, education, cgpa)
        return jsonify({'message': 'User created', 'user_id': uid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json() or request.form
    email = data.get('email')
    password = data.get('password')

    user = find_user_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        session['user_id'] = user['user_id']
        session['user_name'] = user['first_name']
        return jsonify({'message': 'Logged in'}), 200

    return jsonify({'error': 'Invalid credentials'}), 401


# ---------- LOGOUT ----------
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'logged out'})


# ---------- PROFILE ----------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return jsonify({'error': 'not authenticated'}), 401
    
    user_id = session['user_id']

    if request.method == 'GET':
        return render_template('profile.html')

    data = request.get_json() or request.form
    skills = data.get('skills', '')
    interests = data.get('interests', '')

    db = get_db_connection()
    cur = db.cursor()

    # --- Skills ---
    if skills:
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
        for skill in skill_list:
            cur.execute("SELECT skill_id FROM Skills WHERE name=%s", (skill,))
            skill_row = cur.fetchone()
            if skill_row:
                sid = skill_row[0]
            else:
                cur.execute("INSERT INTO Skills (name) VALUES (%s)", (skill,))
                sid = cur.lastrowid

            cur.execute("SELECT user_skill_id FROM UserSkills WHERE user_id=%s AND skill_id=%s", (user_id, sid))
            if not cur.fetchone():
                cur.execute("INSERT INTO UserSkills (user_id, skill_id, proficiency) VALUES (%s,%s,'medium')", (user_id, sid))

    # --- Interests ---
    if interests:
        interest_list = [i.strip() for i in interests.split(',') if i.strip()]
        for interest in interest_list:
            cur.execute("SELECT interest_id FROM Interests WHERE name=%s", (interest,))
            int_row = cur.fetchone()
            if int_row:
                iid = int_row[0]
            else:
                cur.execute("INSERT INTO Interests (name) VALUES (%s)", (interest,))
                iid = cur.lastrowid

            cur.execute("SELECT user_interest_id FROM UserInterests WHERE user_id=%s AND interest_id=%s", (user_id, iid))
            if not cur.fetchone():
                cur.execute("INSERT INTO UserInterests (user_id, interest_id) VALUES (%s,%s)", (user_id, iid))

    db.commit()
    cur.close()
    db.close()

    return jsonify({'message': 'Profile updated'}), 200


# ---------- RECOMMEND ----------
@app.route('/recommend', methods=['GET'])
def recommend_route():
    if 'user_id' not in session:
        return jsonify({'error': 'not authenticated'}), 401

    user_id = session['user_id']
    recs = recommend(user_id, top_n=5)

    results = []
    for cid, score in recs:
        career = get_career_by_id(cid)
        results.append({'career': career, 'score': score})

    return jsonify({'results': results})


# ---------- RESULTS PAGE (for frontend) ----------
@app.route('/results', methods=['GET'])
def results_page():
    if 'user_id' not in session:
        return jsonify({'error': 'not authenticated'}), 401
    return render_template('results.html')


# ---------- ADMIN ----------
@app.route('/admin', methods=['GET'])
def admin():
    careers = get_all_careers()
    return render_template('admin.html', careers=careers)


# ---------- RUN APP ----------
if __name__ == '__main__':
    app.run(debug=True)
