import os
import re
import pandas as pd
from flask import Flask, render_template

# Paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(PROJECT_ROOT, "uploads")

csv_path = os.path.join(UPLOADS_DIR, "projects.csv")
df = pd.read_csv(csv_path)
projects = df.to_dict(orient="records")

# Flask render context only
app = Flask(__name__, static_folder="static", template_folder="templates")

with app.app_context():
    html = render_template("projects.html", projects=projects, query="")

    # Write directly to root folder as index.html
    output_path = os.path.join(PROJECT_ROOT, "index.html")

    # --- Fix asset paths ---
    # Make sure static assets resolve from root
    html = html.replace('href="static/', 'href="./static/')
    html = html.replace('src="static/',  'src="./static/')

    # 2) Ensure Bootstrap loads before styles.css (and update the styles.css path)
    bootstrap_tag = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">'
    styles_tag   = '<link rel="stylesheet" href="./static/styles.css">'

    # Remove any existing Bootstrap or styles.css <link> tags
    html = re.sub(r'<link[^>]+bootstrap@5\.3\.0[^>]*>\s*', '', html, flags=re.I)
    html = re.sub(r'<link[^>]+styles\.css[^>]*>\s*', '', html, flags=re.I)

    # Insert in correct order right before </head>
    html = re.sub(r'</head>', f'  {bootstrap_tag}\n  {styles_tag}\n</head>', html, count=1, flags=re.I)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

print(f"Static file written to {output_path}")
