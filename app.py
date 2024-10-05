from flask import Flask, render_template, request

app = Flask(__name__)

# Sample course topics
course_topics = {
    'data_science': [
        'Python Basics',
        'Data Structures',
        'Pandas and Numpy',
        'Data Visualization',
        'Machine Learning Introduction',
    ],
    'machine_learning': [
        'Supervised Learning',
        'Linear Regression',
        'Classification Algorithms',
        'Clustering',
        'Neural Networks',
    ],
    'web_development': [
        'HTML & CSS',
        'JavaScript Basics',
        'Responsive Design',
        'Back-end with Flask/Django',
        'Deploying Web Applications',
    ]
}

@app.route('/')
def home():
    return render_template('home.html')

# Route to handle course selection and display topics
@app.route('/select_course', methods=['POST'])
def select_course():
    selected_course = request.form['course']
    topics = course_topics.get(selected_course, [])
    return render_template('course_topics.html', course=selected_course, topics=topics)

if __name__ == "__main__":
    app.run(debug=True)
