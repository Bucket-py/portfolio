import flask
import requests

username = "Bucket-py"
github_api_url = f"https://api.github.com/users/{username}/repos"

app = flask.Flask(__name__)
@app.route("/")
def index():
    response = requests.get(github_api_url)
    repos = response.json()
    return flask.render_template("index.html", repos=repos)

def show_repos():
    response = requests.get(github_api_url)
    repos = response.json()
    return repos

if __name__ == "__main__":
    app.run(debug=True)