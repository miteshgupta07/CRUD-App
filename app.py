# Import necessary modules and classes from Flask
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Create SQLAlchemy instance and bind it to the app
db = SQLAlchemy(app)

# Define a Todo class for the database model
class Todo(db.Model):
    # Define columns for the Todo table
    id = db.Column(db.Integer, primary_key=True)
    thing = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Define a string representation for a Todo object
    def __repr__(self):
        return '<Task %r>' % self.id

# Check if the script is being run directly
if __name__ == "__main__":
    # Create the database tables within the app context
    with app.app_context():
        db.create_all()

    # Define the route for the main page
    @app.route('/', methods=['POST', 'GET'])
    def index():
        # Handle POST requests to add new tasks
        if request.method == 'POST':
            thing_name = request.form['thing']
            thing_location = request.form['location']
            new_thing = Todo(thing=thing_name, location=thing_location)

            try:
                db.session.add(new_thing)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your thing and / or its location'
        # Handle GET requests to render the main page
        else:
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('index.html', tasks=tasks, font_url='https://fonts.googleapis.com/css2?family=Syne&display=swap')

    # Define the route for deleting tasks
    @app.route('/delete/<int:id>')
    def delete(id):
        task_to_delete = Todo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that task'

    # Define the route for updating tasks
    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update(id):
        task = Todo.query.get_or_404(id)

        # Handle POST requests to update tasks
        if request.method == 'POST':
            task.thing = request.form['thing']
            task.location = request.form['location']
            try:
                db.session.commit()
                return redirect('/')
            except:
                return 'There was a problem updating your task'
        # Handle GET requests to render the update page
        else:
            return render_template('update.html', task=task, font_url='https://fonts.googleapis.com/css2?family=Syne&display=swap')

    # Run the app in debug mode
    app.run(debug=True)
