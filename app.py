from flask import Flask, render_template, request, redirect, url_for
import requests, json, os

app = Flask(__name__)

GITHUB_USER = "YOUR_GITHUB_USERNAME"
API_URL = f"https://api.github.com/users/{GITHUB_USER}/repos"
HIDDEN_FILE = "hidden_repos.json"

# Utility functions
def load_hidden():
    if os.path.exists(HIDDEN_FILE):
        with open(HIDDEN_FILE, "r") as f:
            return json.load(f)
    return []

def save_hidden(hidden):
    with open(HIDDEN_FILE, "w") as f:
        json.dump(hidden, f, indent=2)

def fetch_repos():
    r = requests.get(API_URL)
    r.raise_for_status()
    repos = []
    for repo in r.json():
        repos.append({
            "name": repo["name"],
            "description": repo["description"],
            "url": repo["html_url"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
        })
    return repos

# Routes
@app.route("/", methods=["GET"])
def index():
    hidden = load_hidden()
    repos = fetch_repos()
    # Filter hidden
    repos = [r for r in repos if r["name"] not in hidden]
    repos = sorted(repos, key=lambda r: r["stars"], reverse=True)
    return render_template("index.html", repos=repos)

@app.route("/toggle_hide", methods=["POST"])
def toggle_hide():
    hidden = set(load_hidden())
    repo_name = request.form.get("repo_name")
    action = request.form.get("action")

    if action == "hide":
        hidden.add(repo_name)
    elif action == "show" and repo_name in hidden:
        hidden.remove(repo_name)

    save_hidden(list(hidden))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
