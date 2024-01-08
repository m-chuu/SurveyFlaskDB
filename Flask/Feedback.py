# Additionally, the feedbacks are stored in a list and written to a file, which can be displayed on the feedback page.
# BUT

# This is because our books are currently stored in the List all_books, 
# this variable gets re-initialised when we re-run main.py and all the data inside is lost.
# If this happened to our user's data, they would not have much faith in our website.
# In order to fix this, we need to learn about data persistence and how to work with databases in Flask applications

# So a cursor is also known as the mouse or pointer. 
# If we were working in Excel or Google Sheet, 
# we would be using the cursor to add rows of data or edit/delete data, 
# we also need a cursor to modify our SQLite database.

#  All actions in SQLite databases are expressed as SQL (Structured Query Language) commands.
# There are quite a few SQL commands. But don't worry, you don't have to memorise them.
# https://www.codecademy.com/article/sql-commands

import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for,json

app = Flask(__name__)

def init_db():
    db = sqlite3.connect("feedbacks_database.db")
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS feedbacks (
        User_ID INTEGER PRIMARY KEY,
        Satisfaction TEXT NOT NULL,
        Usability TEXT NOT NULL,
        Content_quality TEXT NOT NULL
    )""")

    try:
        cursor.execute("INSERT INTO feedbacks (User_ID, Satisfaction, Usability, Content_quality) VALUES (02, 'Perfect', 'Perfect', 'Normal')")
        db.commit()
    except sqlite3.IntegrityError:
        print("Record already exists.")
 
    db.close()

all_feedbacks = []

@app.route('/')
def index():
    return "Welcome to the Feedback Form"

@app.route('/feedback')
def feedback():
    return render_template('feedback_form.html', feedbacks=all_feedbacks)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    user_id = request.form["user-id"]
    overall_satisfaction = request.form["overall-satisfaction"]
    usability = request.form["usability"]
    content_quality = request.form["content-quality"]

    feedback_data = {
        "user_id": user_id,
        "overall_satisfaction": overall_satisfaction,
        "usability": usability,
        "content_quality": content_quality
    }

    all_feedbacks.append(feedback_data)
    print(feedback_data)

    with open('Feedback_data.txt', 'a') as file:
        file.write(json.dumps(feedback_data) + '\n')

    return redirect(url_for('feedback'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

