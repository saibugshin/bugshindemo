from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reports (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        crop TEXT,
                        description TEXT,
                        image_path TEXT,
                        date_reported TEXT
                    )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose():
    if request.method == 'POST':
        file = request.files['crop_image']
        if file:
            filename = file.filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            disease = "Leaf Spot"
            remedy = "Use copper-based fungicides."

            return render_template('diagnose.html', diagnosis=disease, remedy=remedy, image=filename)
    return render_template('diagnose.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        name = request.form['name']
        crop = request.form['crop']
        description = request.form['description']
        file = request.files['report_image']

        image_path = ""
        if file:
            filename = file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO reports (name, crop, description, image_path, date_reported) VALUES (?, ?, ?, ?, ?)",
                      (name, crop, description, image_path, datetime.now()))
            conn.commit()
        return redirect(url_for('index'))

    return render_template('report.html')

@app.route('/view_reports')
def view_reports():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM reports")
        reports = c.fetchall()
    return render_template('view_reports.html', reports=reports)

print(1    )
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
