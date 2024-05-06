from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='drone', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    drone_id = db.Column(db.Integer, db.ForeignKey('drone.id'), nullable=False)
    images = db.relationship('Image', backref='task', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    url = db.Column(db.String(255))
    noise_level = db.Column(db.Float)
