# Security Risk Assessment - OCTAVE Allegro

This is a web-based application designed to implement the OCTAVE Allegro methodology for security risk assessment. It provides a structured, step-by-step process to help organizations identify, analyze, and mitigate information security risks related to their critical assets.

## 🚀 Features

* **Guided Assessment Process:** The application walks users through the essential steps of the OCTAVE Allegro methodology, from establishing risk measurement criteria to identifying and mitigating risks.
* **Project and Asset Management:** Users can create multiple assessment projects and add various critical assets to each project.
* **Dynamic Risk Scoring:** Implements a system for prioritizing impact areas and calculates a relative risk score for each identified threat.
* **Interactive Dashboard:** A central dashboard visualizes key metrics, including the total number of projects, assets, and identified risks. It also features charts to display risk distribution by category for both entire projects and individual assets.
* **CRUD Operations:** Full functionality to Create, Read, Update, and Delete projects and assets, allowing for easy management of the assessment lifecycle.
* **Risk Mitigation:** Provides a dedicated step for defining technical, physical, and people-based mitigation strategies for identified risks.

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** MySQL
* **ORM:** SQLAlchemy
* **Frontend:** HTML, CSS, JavaScript
* **Charting Library:** Chart.js

## 📦 Installation and Setup

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

* Python 3.x
* MySQL Server
* Git

### 2. Clone the Repository

```bash
git clone [https://github.com/your-username/Security-Risk-Assessment_Octave-Allegro.git](https://github.com/your-username/Security-Risk-Assessment_Octave-Allegro.git)
cd Security-Risk-Assessment_Octave-Allegro
3. Set Up a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.
```
For Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
For macOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
4. Install Dependencies
Install all the required Python packages using the requirements.txt file.

Bash

pip install -r requirements.txt
5. Database Setup
Make sure your MySQL server is running.

Connect to your MySQL instance and create a new database.

SQL

CREATE DATABASE octave_srm;
The application is configured to connect to a local MySQL database with username root and no password. If your configuration is different, please update the connection URI in Database/dbConnection.py:

Python

# in Database/dbConnection.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@localhost/octave_srm'
6. Run the Application
Once the setup is complete, run the app.py file to start the Flask development server.

Bash

python app.py
The application will be available at http://127.0.0.1:5000.

📖 How to Use
Navigate to the Homepage: Open your browser and go to http://127.0.0.1:5000. You will be redirected to the dashboard.

Create a New Project: Click the "Create Project" button to start a new risk assessment. This will take you to Step 1.

Follow the Steps: Complete the multi-step form, providing information about the project, critical assets, impact priorities, and potential risks.

View the Dashboard: After completing an assessment, the dashboard will be updated with the new project information and risk metrics. You can select a project from the dropdown to view its specific details and risk profile.

Add More Assets: You can add new assets to an existing project directly from the dashboard by selecting the project and clicking the "Add Asset" button.

📁 Project Structure
├── Database/
│   ├── dbConnection.py     # SQLAlchemy setup and database connection
│   └── database.sql        # SQL schema for the tables
├── Models/
│   ├── projectModel.py     # Database model for Projects
│   ├── assetInformationModel.py # Model for Asset Information
│   ├── assetRiskModel.py   # Model for Asset Risks
│   └── ...                 # Other database models
├── static/
│   ├── dashboard.css       # CSS for the dashboard
│   └── ...                 # Other CSS and static files
├── templates/
│   ├── dashboard.html      # Main dashboard page
│   ├── stepOne.html        # HTML for Step 1 of the assessment
│   └── ...                 # Other HTML templates
├── app.py                  # Main Flask application file with routes and logic
├── requirements.txt        # Python package dependencies
└── README.md               # This file
