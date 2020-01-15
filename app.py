from script import run, returnCommits, returnIssues, returnPullRequests
from flask import Flask, render_template, request, jsonify

from rq import Queue
from rq.job import Job
from rq import get_current_job
from worker import conn

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
q = Queue(connection=conn)


@app.route('/')
def index():
    return render_template('home.html')


# Insert new repository to database
@app.route('/insert', methods=["POST"])
def insert_repository():
    if request.method == "POST":
        try:
            if not "owner" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o dono do repositório a ser inserido!"
                })
            if not "repository" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o nome do repositório a ser inserido!"
                })

            owner = request.json["owner"]
            repository = request.json["repository"]
            job = q.enqueue(run, (owner, repository))
            return jsonify({"response": "Insertion of this repository is started", "job_key": job.key.decode("utf-8")})
        except Exception as e:
            return jsonify({"error": str(e)})


@app.route('/progress/<job_key>', methods=["GET"])
def get_progress_insertion(job_key):
    if request.method == "GET":
        job_key = job_key.replace("rq:job:", "")
        try:
            job = Job.fetch(job_key, connection=conn)

            if(not job.is_finished):
                return "The insertion isn't finished yet!", 202
            else:
                return "The insertion is finished!", 200
        except Exception as e:
            return str(e), 203


@app.route('/issues', methods=["GET"])
def get_issues():
    if request.method == "GET":
        try:
            if not "owner" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o dono do repositório a ser recuperado!"
                })
            if not "repository" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o nome do repositório a ser recuperado!"
                })

            owner = request.json["owner"]
            repository = request.json["repository"]
            limit = request.json["limit"] if "limit" in request.json else None

            issues = returnIssues(owner, repository, limit)
            return jsonify(issues)
        except Exception as e:
            return jsonify({"error": str(e)})


@app.route('/commits', methods=["GET"])
def get_commits():
    if request.method == "GET":
        try:
            if not "owner" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o dono do repositório a ser recuperado!"
                })
            if not "repository" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o nome do repositório a ser recuperado!"
                })

            owner = request.json["owner"]
            repository = request.json["repository"]
            limit = request.json["limit"] if "limit" in request.json else None

            commits = returnCommits(owner, repository, limit)
            return jsonify(commits)
        except Exception as e:
            return jsonify({"error": str(e)})


@app.route('/pullrequests', methods=["GET"])
def get_pull_requests():
    if request.method == "GET":
        try:
            if not "owner" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o dono do repositório a ser recuperado!"
                })
            if not "repository" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o nome do repositório a ser recuperado!"
                })

            owner = request.json["owner"]
            repository = request.json["repository"]
            limit = request.json["limit"] if "limit" in request.json else None

            pullrequests = returnPullRequests(owner, repository, limit)
            return jsonify(pullrequests)
        except Exception as e:
            return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)
