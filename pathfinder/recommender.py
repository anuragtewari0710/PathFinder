from models import get_db_connection, get_career_by_id
# Import get_db_connection directly
from models import get_db_connection as _get_db

def score_user_for_career(user_id, career_id):
    db = _get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT s.skill_id, s.name, us.proficiency FROM UserSkills us JOIN Skills s ON us.skill_id=s.skill_id WHERE us.user_id=%s", (user_id,))
    user_skills_rows = cur.fetchall()
    user_skills = {r['skill_id']: r['proficiency'] for r in user_skills_rows}

    cur.execute("SELECT cs.skill_id, cs.importance FROM CareerSkills cs WHERE cs.career_id=%s", (career_id,))
    career_skills = cur.fetchall()

    score = 0.0
    max_score = 0.0
    prof_weight = {'low':1, 'medium':2, 'high':3}

    for cs in career_skills:
        skill_id = cs['skill_id']
        importance = cs['importance']
        max_score += importance * 3
        prof = user_skills.get(skill_id)
        if prof:
            score += importance * prof_weight.get(prof,2)

    cur.close(); db.close()
    return (score / max_score) if max_score > 0 else 0

def recommend(user_id, top_n=5):
    db = _get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT career_id FROM Careers")
    careers = [r['career_id'] for r in cur.fetchall()]
    results = []
    for cid in careers:
        s = score_user_for_career(user_id, cid)
        results.append((cid, s))
    results.sort(key=lambda x: x[1], reverse=True)

    # persist top N
    cur = db.cursor()
    for cid, sc in results[:top_n]:
        cur.execute("INSERT INTO Recommendations (user_id, career_id, score) VALUES (%s,%s,%s)", (user_id, cid, sc))
    db.commit()
    cur.close(); db.close()
    return results[:top_n]
