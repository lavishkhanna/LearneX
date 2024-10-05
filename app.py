from flask import Flask, render_template, request

app = Flask(__name__)

# Homepage route
@app.route('/')
def home():
    return render_template('home.html')

# Route to handle the selected course
@app.route('/select_course', methods=['POST'])
def select_course():
    selected_course = request.form['course']
    return f"You selected {selected_course}!"

if __name__ == "__main__":
    app.run(debug=True)
