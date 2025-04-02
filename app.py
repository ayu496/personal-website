from flask import Flask, render_template, request, redirect, url_for

import sqlite3
DATABASE = "personal_site.db"

app = Flask(__name__)
from flask import flash
# Enable secret key for flash messages (at top, after app = Flask(...))
app.secret_key = 'dev' # in real app, use a secure key or load from config
# Homepage route
projects = [
{"title": "Coffee Shop Sales Analysis - Data Analytics", "desc": "Analyzed and segmented coffee shop sales data by location, product category, detail, size, type, and order weeks.\n Created pivot tables and visualizations in Excel, delivering insights through comprehensive reports and dynamic dashboards. \n Developed actionable recommendations to optimize product offerings, inventory, and staffing based on sales patterns and demand"},
{"title": "Music Store Data Analysis Using SQL - Data Analytics", "desc": "Analyzed music store sales data to uncover insights and trends in customer behavior, popular genres, and sales patterns. \n Designed and implemented SQL queries to extract, manipulate, and visualize data, identifying opportunities for business growth. \n Optimized queries to improve performance and reduce processing time, enabling efficient reporting and decision-making"}
,{"title":"Clothing Store Annual Report Analysis - Data Analytics", "desc": "Conducted data analysis of Clothing Store’s annual sales segmented by gender, age group, channel, month and state.\n Created visualizations and reports using Excel, identifying key sales trends and providing strategic recommendations. \n Delivered in-depth insights to enhance targeted marketing strategies, driving improvements in product offerings and customer engagement"}
]

experiences = [
    {"title":"LEARN KOVALENT | Market Research and AI Analytics","desc" : "Conducted market research and used AI analytics tools to identify trends, providing actionable insights for strategies. Collaborated with teams to design data collection methods, analyzing large datasets to support key business decisions. Utilized machine learning models to forecast market trends, enhancing predictive accuracy for targeted marketing campaigns."},
    {"title":"PREDICTRAM | Financial Research Analyst","desc":"Conducted in-depth research and analysis of financial events, providing actionable insights for fintech decision-making processes. Authored comprehensive reports on economic indicators, including inflation, money supply and industrial production for stakeholders. Collaborated with cross-functional teams, utilizing data-driven approaches to deliver clear, concise, and impactful content for audiences"}
    
]

@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if not title or not content:
            flash("Title and content are required!", "danger")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title,content))
            conn.commit()
            conn.close()
            flash("New post added successfully.", "success")
            return redirect(url_for('blog'))
    # If GET or if validation fails:
    return render_template("new_post.html")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # so we can treat rows like dictionaries
    return conn


@app.route("/init_post")
def init_post():
    conn = get_db_connection()
    conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
    ("My First Blog Post", "This is a sample blog post about my project."))
    conn.commit()
    conn.close()
    return "Initial post added."
@app.route("/blog")
def blog():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY created DESC").fetchall()

    conn.close()
    return render_template("blog.html", posts=posts)





@app.route("/")
def home():

    return render_template("home.html",projects=projects,experiences = experiences)
# (Optional) define other routes if needed, e.g., a dedicated page for contact
# For now, we might handle contact form on home itself via a POST route.
@app.route("/contact", methods=["POST"])
def contact():
    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    # In a real app, here you might save to database or send an email.
    # We'll just simulate by printing and then redirecting back to home with a success message.
    print(f"Received message from {name} ({email}): {message}")
    # You could flash a message or something, but let's keep it simple.
    return redirect(url_for("home"))
if __name__ == "__main__":
    # Initialize database (create table if not exists)
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    app.run(debug=True)

