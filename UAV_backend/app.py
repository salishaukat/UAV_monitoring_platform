from flask import Flask, jsonify, request
from models import db, Drone, Task, Image
import os
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uav_monitoring.db'
db.init_app(app)

# Print the absolute path where the SQLite file will be created
print("SQLite file will be created at:", os.path.abspath("uav_monitoring.db"))

# API endpoints
@app.route('/api/drones', methods=['GET'])
def get_drones():
    drones = Drone.query.all()
    drone_list = [{'id': drone.id, 'name': drone.name} for drone in drones]
    return jsonify(drone_list)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    drone_id = data.get('drone_id')

    task = Task(name=name, description=description, drone_id=drone_id)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    task_data = {
        'id': task.id,
        'name': task.name,
        'description': task.description,
        'drone': {'id': task.drone.id, 'name': task.drone.name}
    }
    return jsonify(task_data)

@app.route('/api/tasks/<int:id>/execute', methods=['POST'])
def execute_task(id):
    # Simulate image capture
    images = []
    for _ in range(5):
        # Generate random noisy image
        # Replace this with your actual image capture logic
        image = {'url': 'https://example.com/image.jpg', 'noise_level': random.random()}
        images.append(image)
    
    # Store images in the database
    task = Task.query.get_or_404(id)
    for img in images:
        image = Image(task_id=task.id, url=img['url'], noise_level=img['noise_level'])
        db.session.add(image)
    db.session.commit()
    
    return jsonify({'message': 'Task executed successfully'}), 200

@app.route('/api/tasks/<int:id>/images', methods=['GET'])
def get_task_images(id):
    task = Task.query.get_or_404(id)
    images = [{'url': img.url, 'noise_level': img.noise_level} for img in task.images]
    return jsonify(images)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
