from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Read projects from CSV
def get_projects():
    df = pd.read_csv("uploads/projects.csv")
    return df.to_dict(orient="records")

@app.route("/", methods=["GET"])
def home():
    query = request.args.get('q', '').lower()
    projects = get_projects()

    if query:
        projects = [p for p in projects if query in p['project-title'].lower() or query in p['description'].lower()]

    return render_template("index.html", projects=projects, query=query)

if __name__ == "__main__":
    app.run(debug=True)
