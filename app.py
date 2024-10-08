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
#         video_data = {
#             'title': row['title'],
#             'link': row['link'],
#             'channel': row['channel'],
#             'description': row['desc'],
#             'duration': row['duration']
#         }
#         videos.append(video_data)
    
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

# Create User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def home():
    return render_template('home.html', user=current_user)


from flask import redirect, url_for, render_template
from flask_login import login_required

# Example topics dictionary
topics = {
    "Python": ["Variables", "Data Types", "Control Flow", "Functions"],
    "Data Science": ["NumPy", "Pandas", "Matplotlib", "Machine Learning"],
    "C++": ["Pointers", "Memory Management", "Algorithms", "Data Structures"],
    "UI/UX Design": ["User Research", "Prototyping", "User Flows", "Wireframing"]
}

# Route for starting learning based on selected course
@app.route('/start_learning/<course_name>', methods=['GET'])
@login_required  # Ensure that only logged-in users can access this route
def start_learning(course_name):
    # Fetch the topics for the selected course
    course_topics = topics.get(course_name, [])

    # Redirect to the learning page with the topics of the selected course
    return render_template('learning_page.html', course_name=course_name, topics=course_topics)

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
