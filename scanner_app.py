from flask import Flask, request, jsonify
from openai import OpenAI
import textract, re, os, numpy as np
from numpy.linalg import norm
from flask_cors import CORS
CORS(app)

app = Flask(__name__)
client = OpenAI(api_key="YOUR_API_KEY")

def extract_text(file):
    filename = file.filename
    file.save(filename)
    text = textract.process(filename).decode("utf-8")
    os.remove(filename)
    return text

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = set(["and","or","the","a","of","in","for","to","with"])
    return [w for w in words if w not in stopwords]

def semantic_score(resume_text, job_text):
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=[resume_text, job_text]
    )
    a, b = np.array(response.data[0].embedding), np.array(response.data[1].embedding)
    return float(np.dot(a,b)/(norm(a)*norm(b)))

@app.route("/scan_resume", methods=["POST"])
def scan_resume():
    try:
        if "resume_file" not in request.files:
            return jsonify({"error": "No resume uploaded"}), 400
        resume_text = extract_text(request.files["resume_file"])

        if "jd_file" in request.files:
            job_text = extract_text(request.files["jd_file"])
        else:
            job_text = request.form.get("job_description", "")
            if not job_text:
                return jsonify({"error": "No job description provided"}), 400

        resume_kw = set(extract_keywords(resume_text))
        job_kw = set(extract_keywords(job_text))
        matched = list(resume_kw & job_kw)
        missing = list(job_kw - resume_kw)

        similarity = semantic_score(resume_text, job_text)
        keyword_score = len(matched)/len(job_kw) if job_kw else 0
        match_score = round((0.5*keyword_score + 0.5*similarity)*100, 2)

        prompt = f"""
        Resume Text: {resume_text}
        Job Description: {job_text}

        Identify missing skills, suggest improvements, highlight strengths.
        """
        suggestions_resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=300
        )
        suggestions = suggestions_resp.choices[0].message.content.strip()

        return jsonify({
            "match_score": match_score,
            "matched_keywords": matched,
            "missing_keywords": missing,
            "suggestions": suggestions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
