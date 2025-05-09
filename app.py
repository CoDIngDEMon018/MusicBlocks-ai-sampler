from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'musicblocks_secure_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicblocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    skills = db.Column(db.String(200))
    role = db.Column(db.String(20), default='contributor')
    contributions = db.relationship(
        'Contribution', 
        backref='contributor', 
        foreign_keys='Contribution.user_id', 
        lazy=True
    )
    mentored_contributions = db.relationship(
        'Contribution', 
        backref='mentor', 
        foreign_keys='Contribution.mentor_id', 
        lazy=True
    )
class MusicblockProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20))
    skills_required = db.Column(db.String(200))
    status = db.Column(db.String(20), default='open')
    contributions = db.relationship('Contribution', backref='project', lazy=True)

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('musicblock_project.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    hours = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Application Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        skills = request.form.get('skills', '')
        role = request.form.get('role', 'contributor')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            password=password,
            skills=skills,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return redirect(url_for('pathway'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/pathway')
def pathway():
    projects = MusicblockProject.query.order_by(MusicblockProject.difficulty).all()
    return render_template('pathway.html', projects=projects)

@app.route('/projects')
def projects():
    projects = MusicblockProject.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/contribute', methods=['POST'])
def contribute():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        new_contribution = Contribution(
            user_id=session['user_id'],
            project_id=request.form['project_id'],
            hours=float(request.form['hours']),
            description=request.form['description'],
            status='pending'
        )
        db.session.add(new_contribution)
        db.session.commit()
        flash('Contribution logged successfully!')
    except:
        flash('Error logging contribution')

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    contributions = Contribution.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, contributions=contributions)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

# Database Initialization
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if not MusicblockProject.query.first():
            sample_projects = [
                MusicblockProject(
                    title="Rhythm Pattern Generator",
                    description="Create visual rhythm patterns",
                    difficulty="beginner",
                    skills_required="Python, Music Basics",
                    status="open"  # Add status field
                ),
                MusicblockProject(
                    title="MIDI Integration",
                    description="Implement MIDI file support",
                    difficulty="advanced",
                    skills_required="Python, MIDI Protocol",
                    status="open"  # Add status field
                )
            ]
            db.session.bulk_save_objects(sample_projects)
            db.session.commit()
    
    app.run(debug=True)