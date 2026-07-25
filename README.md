# Full Stack Application Development Capstone — Best Cars Dealership

This repository contains the completed IBM/Coursera Full Stack Application Development Capstone project. The application combines:

- Django authentication and API proxy endpoints
- React pages for dealerships, dealer reviews, registration, login, and review submission
- Node.js/Express/MongoDB dealership and review services
- Flask sentiment analysis
- GitHub Actions CI checks
- Container-ready deployment configuration

## Project structure

```text
server/
├── djangoapp/              # Django models, authentication, dealer/review APIs
├── djangoproj/             # Django project configuration
├── frontend/               # React client and static About/Contact pages
├── database/               # Node.js + MongoDB service
├── sentiment_analyzer/     # Flask sentiment service
├── manage.py
└── requirements.txt
```

## Run locally in the Coursera lab

### 1. Start the database service

```bash
cd server/database
docker compose up --build -d
```

### 2. Start the sentiment analyzer

```bash
cd server/sentiment_analyzer
python3 -m pip install -r requirements.txt
python3 app.py
```

It runs on port `5050` by default.

### 3. Build the React client

```bash
cd server/frontend
npm install
npm run build
```

### 4. Start Django

```bash
cd server
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 0.0.0.0:8000
```

Open the application on port `8000`.

## Main endpoints

| Endpoint | Method | Purpose |
|---|---:|---|
| `/djangoapp/login` | POST | Authenticate a user |
| `/djangoapp/logout` | GET/POST | End the current session |
| `/djangoapp/register` | POST | Register and log in a user |
| `/djangoapp/get_dealers` | GET | Return all dealerships |
| `/djangoapp/get_dealers/<state>` | GET | Filter dealerships by state or abbreviation |
| `/djangoapp/dealer/<id>` | GET | Return one dealership |
| `/djangoapp/reviews/dealer/<id>` | GET | Return reviews with sentiment labels |
| `/djangoapp/add_review` | POST | Add a dealership review |
| `/djangoapp/get_cars` | GET | Return car makes and models |
| `/djangoapp/analyze/<text>` | GET | Analyze review sentiment |

## Submission

See [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) for the 28 required artifacts, exact cURL commands, screenshot names, and GitHub URLs.
