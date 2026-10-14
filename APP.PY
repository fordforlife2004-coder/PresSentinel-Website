import os
import secrets
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Tip

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SENTINEL_SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///sentinel.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.datetime.now().year,
        'tagline': "Liberty, Law, and Public Accountability for the Heartland"
    }

@app.route('/')
def home():
    featured_articles = [
        {
            "id": "PTS-2026-081",
            "title": "County Drainage Board Approves Undisclosed Easements",
            "category": "Land Rights & Zoning",
            "date": "Oct 10, 2026",
            "summary": "Internal county documents show expedited approvals for commercial drainage easements without public zoning hearing notices."
        },
        {
            "id": "PTS-2026-079",
            "title": "Municipal Budget Audit: Discrepancies in Heavy Fleet Procurement",
            "category": "Taxpayer Accountability",
            "date": "Oct 04, 2026",
            "summary": "A closer look at municipal spending contracts reveals unexplained cost overruns across three consecutive fiscal quarters."
        }
    ]
    return render_template('index.html', articles=featured_articles)

@app.route('/investigations')
def investigations():
    categories = [
        {"name": "Local Government Transparency", "count": 4, "desc": "Monitoring closed-door deliberations and open records compliance."},
        {"name": "Public Infrastructure & Spending", "count": 6, "desc": "Auditing secondary road asphalt and structural concrete certifications."},
        {"name": "Agricultural & Environmental Compliance", "count": 3, "desc": "Water drainage and agricultural chemical dispersal oversight."},
        {"name": "Civil Liberties & Due Process", "count": 2, "desc": "Asset forfeiture ledgers and administrative rule enforcement."}
    ]
    return render_template('investigations.html', categories=categories)

@app.route('/tip-desk', methods=['GET', 'POST'])
def submit_tip():
    if request.method == 'POST':
        jurisdiction = request.form.get('category', '').strip()
        subject = request.form.get('subject', '').strip()
        details = request.form.get('details', '').strip()
        callback = request.form.get('contact_method', '').strip()

        if not subject or not details or not jurisdiction:
            flash("All mandatory fields must be completed.", "error")
            return redirect(url_for('submit_tip'))

        raw_token = secrets.token_hex(6).upper()
        formatted_token = f"STNL-{raw_token[:4]}-{raw_token[4:8]}-{raw_token[8:]}"
        v_hash = Tip.generate_hash(formatted_token, details)

        record = Tip(
            token=formatted_token,
            jurisdiction=jurisdiction,
            subject=subject,
            details=details,
            callback_alias=callback if callback else None,
            verification_hash=v_hash
        )

        db.session.add(record)
        db.session.commit()

        return render_template('tip_success.html', token=formatted_token, category=jurisdiction)

    return render_template('submit_tip.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
