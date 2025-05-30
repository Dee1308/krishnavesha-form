
from flask import Flask, render_template, request, redirect, url_for, flash
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'  # You can set this to any random string

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("gspread_credentials.json", scope)
gc = gspread.authorize(creds)

sheet = gc.open("Krishnavesha_Registrations").sheet1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mode = request.form.get('mode')

        if mode == 'individual':
            name = request.form.get('parent_name')
            mobile = request.form.get('parent_mobile')
            email = request.form.get('parent_email')
        elif mode == 'school':
            name = request.form.get('school_name')
            mobile = request.form.get('coordinator_mobile')
            email = request.form.get('coordinator_email')
        else:
            flash("Please select a registration mode")
            return redirect(url_for('index'))

        consent = request.form.get('consent')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Process participants
        participants = []
        for key in request.form:
            if key.startswith("participant_name_"):
                suffix = key.split("_")[-1]
                pname = request.form.get(f'participant_name_{suffix}')
                pschool = request.form.get(f'participant_school_{suffix}')
                gender = request.form.get(f'participant_gender_{suffix}')
                dob = request.form.get(f'participant_dob_{suffix}')
                category = calculate_category(dob)
                costume = 'Yes' if request.form.get(f'costume_{suffix}') else 'No'
                group = 'Yes' if request.form.get(f'group_{suffix}') else 'No'

                participants.append([timestamp, mode, name, mobile, email, consent, pname, pschool, gender, dob, category, costume, group])

        if len(participants) == 0:
            flash("Please add at least one participant before submitting.")
            return redirect(url_for('index'))

        for row in participants:
            sheet.append_row(row)

        flash("Form submitted successfully!")
        return redirect(url_for('index'))

    return render_template('form.html')

def calculate_category(dob_str):
    dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d")
    if dob >= datetime.datetime(2024, 8, 9):
        return "A"
    elif dob >= datetime.datetime(2022, 8, 9):
        return "B"
    elif dob >= datetime.datetime(2020, 8, 9):
        return "C"
    elif dob >= datetime.datetime(2018, 8, 9):
        return "D"
    elif dob >= datetime.datetime(2016, 8, 9):
        return "E"
    elif dob >= datetime.datetime(2013, 8, 9):
        return "F"
    elif dob >= datetime.datetime(2010, 8, 9):
        return "G"
    else:
        return "Invalid"

if __name__ == '__main__':
    app.run(debug=True)