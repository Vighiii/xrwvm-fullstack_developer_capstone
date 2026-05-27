# Best Cars Dealership - Full Stack Review Portal

## Project Overview
This is a Capstone project for the IBM Full Stack Software Developer Professional Certificate. The application is a central database for national car dealership reviews, allowing users to look up branches by state and view or add customer reviews.

## Architecture
The project is built using a microservices architecture:
- **Frontend:** React.js
- **Backend:** Django (Web Server & User Management)
- **Database:** SQLite (Cars Data) & MongoDB (Dealers and Reviews)
- **Microservices:** 
  - Node.js/Express (Dealers & Reviews API)
  - Python/Flask (Sentiment Analysis using NLTK)
- **Deployment:** Docker, Kubernetes, and IBM Cloud Code Engine.

## Features
- **Anonymous Users:** View About/Contact pages and dealership lists with state filtering.
- **Authorized Users:** Login/Logout and post reviews with sentiment analysis integration.
- **Admin Users:** Manage car makes and models through the Django admin site.

## Setup and Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run migrations: `python3 manage.py migrate`.
4. Start the server: `python3 manage.py runserver`.

## License
This project is licensed under the Apache 2.0 License.