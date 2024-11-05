
# LearneX - Personalized Course Recommendation System

LearneX is a personalized learning platform that recommends courses and content based on users' learning patterns and preferences. Built with Flask, Python, and integrated machine learning models, LearneX tailors learning journeys to individual users by analyzing their past interactions, video captions, and other behavioral data.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)

---

## Overview

LearneX uses advanced recommendation algorithms, including Sequential Pattern Mining with LSTM, to predict the next best video or topic for each learner. By analyzing user engagement, topics of interest, and even video captions, LearneX provides a dynamic, adaptive learning path to help students achieve their goals more effectively.

## Features

- **Personalized Recommendations**: Recommends courses based on user interactions, preferences, and sequential learning patterns.
- **Video and Topic Analysis**: Learns from video captions and metadata for improved content relevance.
- **Interactive Learning Roadmap**: Allows users to see their learning journey and track completed topics.
- **Sequential Pattern Mining**: Uses LSTM models to predict and suggest the next best video based on the user’s past interactions.
- **Real-time Adaptive Recommendations**: Adjusts content recommendations dynamically as users progress.

## Tech Stack

- **Backend**: Flask
- **Machine Learning**: TensorFlow, Keras, Pandas, Numpy
- **Database**: SQLAlchemy (SQLite)
- **Frontend**: HTML, CSS (Bootstrap), JavaScript

## Project Structure

```
|-- .gitignore
|-- app.py
|-- Procfile
|-- rec.py
|-- requirements.txt
|-- vercel.json
|-- YT_data_1.csv
|-- .vercel
  |-- project.json
  |-- README.txt
|-- instance
  |-- users.db
|-- __pycache__
  |-- app.cpython-311.pyc
|-- templates
  |-- course_topics.html
  |-- home.html
  |-- learning_page.html
  |-- login.html
  |-- module_page.html
  |-- register.html
  |-- roadmap_page.html

```

## Installation

### Prerequisites
- **Python 3.7 - 3.10**
- **pip** package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lavishkhanna/LearneX.git
   cd LearneX
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (if needed):
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

5. **Initialize the database**:
   ```bash
   flask db upgrade
   ```

## Usage

1. **Run the application**:
   ```bash
   flask run
   ```
   
2. **Access the platform**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

3. **Explore Features**:
   - Browse and start recommended courses.
   - Track your learning roadmap.
   - Enjoy personalized recommendations based on learning patterns.

## Deployment

### Deploy on Vercel (for Free)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Link Project and Deploy**:
   ```bash
   vercel
   ```

3. **Update Deployments**:
   Each push to the main branch (or the linked branch) triggers an automatic redeployment.

### Alternative Hosting
If Vercel doesn’t fit your needs, LearneX can also be deployed on:
- **Heroku** (Python buildpack)
- **AWS Elastic Beanstalk**
- **DigitalOcean** with Docker

## Future Improvements

- **Context-Aware Recommendations**: Incorporate additional contextual data (e.g., time of day, device).
- **Expanded Analytics**: Track and display user progress over time with detailed insights.
- **Enhanced Model**: Improve the recommendation algorithm using reinforcement learning or knowledge graph-based systems.
- **Improved UI/UX**: Add more interactivity and visualization to the learning roadmap.

## Contributing

Contributions are welcome! Please fork this repository, make changes, and submit a pull request. For any questions or feature requests, feel free to open an issue.

## License

This project is licensed under the MIT License. See `LICENSE` for more information.

---

Thank you for checking out LearneX!
