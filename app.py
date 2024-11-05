# from flask import Flask, render_template, request

# import pandas as pd

# # Load YouTube dataset
# data = pd.read_csv('YT_data_1.csv')  # Make sure to have the CSV file in your project directory

# import difflib

# def get_videos_for_topic(organisation, topic_type, module, topic):
#     # Use the correct values directly, no need for lowercasing or stripping
#     print(f"Organisation: {organisation}")
#     print(f"Topic Type: {topic_type}")
#     print(f"Module: {module}")
#     print(f"Topic: {topic}")

#     # Filter the dataset based on these four attributes
#     filtered_videos = data[
#         (data['organisation'] == organisation) &
#         (data['module'] == module) &
#         (data['topic'] == topic)
#     ]

#     # Print filtered videos for debugging
#     print(f"Filtered Videos DataFrame:\n{filtered_videos}")

#     if filtered_videos.empty:
#         print("No videos found for this combination.")
#     else:
#         print(f"Videos found: {len(filtered_videos)}")

#     # Return the videos in the desired format
#     videos = []
#     for _, row in filtered_videos.iterrows():
#         data = {
#             'title': row['title'],
#             'link': row['link'],
#             'channel': row['channel'],
#             'description': row['desc'],
#             'duration': row['duration']
#         }
#         videos.append(data)
    
#     return videos











# app = Flask(__name__)

# # Sample course topics
# course_topics = {
#     'data_science': [
#         'Python Basics',
#         'Data Structures',
#         'Pandas and Numpy',
#         'Data Visualization',
#         'Machine Learning Introduction',
#     ],
#     'machine_learning': [
#         'Supervised Learning',
#         'Linear Regression',
#         'Classification Algorithms',
#         'Clustering',
#         'Neural Networks',
#     ],
#     'web_development': [
#         'HTML & CSS',
#         'JavaScript Basics',
#         'Responsive Design',
#         'Back-end with Flask/Django',
#         'Deploying Web Applications',
#     ]
# }

topics = {
    "Python": {
        "Basics": ["Variables", "Data Types", "Operators", "Control Flow"],
        "Functions": ["Function Definition", "Parameters", "Return Values"],
        "Data Structures": ["Lists", "Tuples", "Dictionaries", "Sets"],
        "Object-Oriented Programming": ["Classes", "Inheritance", "Polymorphism"],
        "File Handling": ["Reading/Writing Files", "CSV/JSON Handling"],
        "Modules and Libraries": ["Importing Modules", "Standard Libraries"],
    },
    "Data Science": {
        "Data Manipulation": ["NumPy", "Pandas"],
        "Data Visualization": ["Matplotlib", "Seaborn"],
        "Machine Learning": ["Scikit-Learn", "Regression", "Classification"],
        "Deep Learning": ["TensorFlow", "Keras"],
        "Data Analysis": ["Exploratory Data Analysis", "Feature Engineering"],
        "Model Evaluation": ["Cross-Validation", "Metrics"],
    },
    "C++": {
        "Basics": ["Variables", "Data Types", "Operators", "Control Structures"],
        "Functions": ["Function Definition", "Parameters", "Return Values"],
        "Pointers and Memory Management": ["Pointers", "Dynamic Memory Allocation"],
        "Object-Oriented Programming": ["Classes", "Inheritance", "Polymorphism"],
        "STL (Standard Template Library)": ["Containers", "Algorithms"],
        "File Handling": ["File Streams", "Binary Files"],
    },
    "UI/UX": {
        "User Research": ["User Interviews", "Surveys", "Personas"],
        "User Interface Design": ["Layout", "Typography", "Color Theory"],
        "User Experience Design": ["User Flows", "Wireframing", "Prototyping"],
        "Interaction Design": ["Microinteractions", "Transitions"],
        "Usability Testing": ["A/B Testing", "User Feedback"],
        "Design Tools": ["Adobe XD", "Figma", "Sketch"],
    }
}



# @app.route('/')
# def home():
#     return render_template('home.html')

# # Route to handle course selection and display topics
# @app.route('/select_course', methods=['POST'])
# def select_course():
#     selected_organisation = request.form['organisation']

#     # Get the default topic type, module, and topic for this organisation
#     organisation_topics = topics.get(selected_organisation, {})
    
#     # Let's pick the first available topic type and module (for simplicity)



# # ERROR HERE 



#     if organisation_topics:
#         first_topic_type = topics[selected_organisation][0]
#         first_module = organisation_topics[first_topic_type][0]
#     else:
#         first_topic_type = ""
#         first_module = ""

#     # Fetch videos for the first topic (for now, just simplifying to the first module)
#     videos = get_videos_for_topic(selected_organisation, first_topic_type, first_module, first_module)

#     return render_template('course_topics.html', organisation=selected_organisation, videos=videos)





# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd

data=pd.read_csv('YT_data_1.csv')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect users to the login page if not authenticated

# Define User model first
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Define the relationship with backref to Roadmap
    roadmaps = db.relationship('Roadmap', backref='user', lazy=True)

# Now define Roadmap model
class Roadmap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_name = db.Column(db.String(150), nullable=False)
    topic = db.Column(db.String(150), nullable=False)  # Main topic
    subtopic = db.Column(db.String(150), nullable=True)  # Subtopic
    completed = db.Column(db.Boolean, default=False)

    # No need to define the user relationship here since it's already defined in the User model




# Create the database
with app.app_context():
    db.create_all()

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Home route
@app.route('/')
def home():
    return render_template('home.html', user=current_user)


from flask import redirect, url_for, render_template
from flask_login import login_required

# # Example topics dictionary
# topics = {
#     "Python": ["Variables", "Data Types", "Control Flow", "Functions"],
#     "Data Science": ["NumPy", "Pandas", "Matplotlib", "Machine Learning"],
#     "C++": ["Pointers", "Memory Management", "Algorithms", "Data Structures"],
#     "UI/UX Design": ["User Research", "Prototyping", "User Flows", "Wireframing"]
# }


@app.route('/start_learning/<course_name>', methods=['GET', 'POST'])
@login_required
def start_learning(course_name):
    course_topics = topics.get(course_name, {})

    # Add both topics and subtopics to the user's roadmap
    for topic_category, subtopics in course_topics.items():
        # Add the topic itself (e.g., "Data Manipulation")
        existing_topic = Roadmap.query.filter_by(user_id=current_user.id, course_name=course_name, topic=topic_category).first()
        if not existing_topic:
            new_topic = Roadmap(user_id=current_user.id, course_name=course_name, topic=topic_category, subtopic=None)
            db.session.add(new_topic)

        # Add each subtopic (e.g., "NumPy", "Pandas")
        for subtopic in subtopics:
            existing_subtopic = Roadmap.query.filter_by(user_id=current_user.id, course_name=course_name, topic=topic_category, subtopic=subtopic).first()
            if not existing_subtopic:
                new_subtopic = Roadmap(user_id=current_user.id, course_name=course_name, topic=topic_category, subtopic=subtopic)
                db.session.add(new_subtopic)
    
    db.session.commit()
    return redirect(url_for('roadmap', course_name=course_name))




# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please log in.')
            return redirect(url_for('login'))

        # Create a new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your credentials.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Route for displaying the roadmap
@app.route('/roadmap/<course_name>', methods=['GET', 'POST'])
@login_required
def roadmap(course_name):
    # Fetch the list of topic categories (keys) for the selected course
    course_topics = topics.get(course_name, {})
    
    # If it's a POST request (user is removing a topic or modifying the roadmap)
    if request.method == 'POST':
        topic = request.form['topic']
        # Adding a new topic to roadmap
        new_topic = Roadmap(user_id=current_user.id, course_name=course_name, topic=topic, completed=False)
        db.session.add(new_topic)
        db.session.commit()

    # Fetch the user's roadmap for this course
    roadmap = Roadmap.query.filter_by(user_id=current_user.id, course_name=course_name).all()
    
    # Render the roadmap page
    return render_template('roadmap_page.html', course_name=course_name, course_topics=course_topics, roadmap=roadmap)

# @app.route('/roadmap/<course_name>', methods=['GET', 'POST'])
# @login_required
# def roadmap(course_name):
#     # Retrieve topics and subtopics for the selected course
#     course_topics = topics.get(course_name, {})  # Structured course data

#     # Fetch the user's roadmap progress data for this course from the database
#     roadmap = Roadmap.query.filter_by(user_id=current_user.id, course_name=course_name).all()
    
#     # Render the template with both course structure and user progress data
#     return render_template('roadmap_page.html', course_name=course_name, course_topics=course_topics, roadmap=roadmap)




# Route for marking a topic as completed
@app.route('/complete_topic/<int:roadmap_id>', methods=['POST'])
@login_required
def complete_topic(roadmap_id):
    roadmap_item = Roadmap.query.get_or_404(roadmap_id)
    if roadmap_item.user_id == current_user.id:
        roadmap_item.completed = True
        db.session.commit()
    return redirect(url_for('roadmap', course_name=roadmap_item.course_name))

# Route for removing a topic
@app.route('/remove_topic/<int:roadmap_id>', methods=['POST'])
@login_required
def remove_topic(roadmap_id):
    roadmap_item = Roadmap.query.get_or_404(roadmap_id)
    if roadmap_item.user_id == current_user.id:
        db.session.delete(roadmap_item)
        db.session.commit()
    return redirect(url_for('roadmap', course_name=roadmap_item.course_name))



@app.route('/add_topic/<course_name>', methods=['POST'])
@login_required
def add_topic(course_name):
    topic = request.form['topic']
    existing_topic = Roadmap.query.filter_by(user_id=current_user.id, course_name=course_name, topic=topic).first()
    if not existing_topic:
        new_topic = Roadmap(user_id=current_user.id, course_name=course_name, topic=topic, completed=False)
        db.session.add(new_topic)
        db.session.commit()

    return redirect(url_for('roadmap', course_name=course_name))




@app.route('/debug_roadmap', methods=['GET'])
@login_required
def debug_roadmap():
    roadmaps = Roadmap.query.filter_by(user_id=current_user.id).all()
    for roadmap in roadmaps:
        print(f"User: {current_user.username}, Course: {roadmap.course_name}, Topic: {roadmap.topic}, Completed: {roadmap.completed}")
    return "Check your console for debug info."



# ----------------------------------------------------------------THIS IS SEPERATE VIDOES SECTION FOR EACH TOPIC, THIS HAS WRONG NAMING CONVENTIONS, TO BE FIXED ACCORDING TO YT_DATA_1.CSV STRUCTURE ------------------------------------------------------
import random


@app.route('/module/<course_name>/<topic>/<subtopic>', methods=['GET'])
@login_required
def module_page(course_name, topic, subtopic):
    # Example data for demonstration
    video_url = f"https://example.com/video/{course_name}/{topic}/{subtopic}"  # Placeholder video URL
    content = {
        "description": f"This module covers {subtopic} in {course_name} - {topic}.",
        "resources": [
            {"name": "Documentation", "link": "https://www.example.com/docs"},
            {"name": "Practice Exercises", "link": "https://www.example.com/practice"}
        ]
    }

    video_row = data[
        (data['organisation'] == course_name) &
        (data['module'] == topic) &
        (data['topic'] == subtopic)
    ]

    video_url=video_row['link']

    
    import random

    # Check if video_row has any matches
    if not video_row.empty:
        # Randomly select a link from the 'link' column
        video_url = random.choice(video_row['link'].tolist())
        
        # Convert the YouTube link to embeddable format if necessary
        if "watch?v=" in video_url:
            video_id = video_url.split("watch?v=")[-1]
            video_url = f"https://www.youtube.com/embed/{video_id}"
    else:
        video_url = None  # Set a default or handle the case when no rows match



    
    # Render the module page with fetched content
    return render_template('module_page.html', course_name=course_name, topic=topic, subtopic=subtopic, video_url=video_url, content=content)












# Run the app
if __name__ == '__main__':
    app.run(debug=True)




