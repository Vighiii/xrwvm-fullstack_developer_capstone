#!/bin/bash
# Run this in IBM IDE after: git clone https://github.com/LeoDuarte6/xrwvm-fullstack_developer_capstone.git

cat > server/djangoapp/models.py << 'EOF'
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class CarModel(models.Model):
    CAR_TYPES = [('SEDAN', 'Sedan'), ('SUV', 'SUV'), ('WAGON', 'Wagon')]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023, validators=[MaxValueValidator(2023), MinValueValidator(2015)])
    def __str__(self):
        return f"{self.car_make.name} {self.name}"
EOF

cat > server/djangoapp/admin.py << 'EOF'
from django.contrib import admin
from .models import CarMake, CarModel
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
EOF

cat > server/djangoapp/populate.py << 'EOF'
from .models import CarMake, CarModel
def initiate():
    makes = [CarMake.objects.create(name=n, description=d) for n, d in [("NISSAN", "Japanese"), ("Mercedes", "German"), ("Audi", "German"), ("Kia", "Korean"), ("Toyota", "Japanese")]]
    for name, ctype, year, idx in [("Pathfinder", "SUV", 2023, 0), ("Qashqai", "SUV", 2023, 0), ("A-Class", "SUV", 2023, 1), ("C-Class", "SEDAN", 2023, 1), ("A4", "SEDAN", 2023, 2), ("Sorrento", "SUV", 2023, 3), ("Corolla", "SEDAN", 2023, 4), ("Camry", "SEDAN", 2023, 4)]:
        CarModel.objects.create(name=name, car_make=makes[idx], type=ctype, year=year)
EOF

cat > server/djangoapp/restapis.py << 'EOF'
import requests, os
from dotenv import load_dotenv
load_dotenv()
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")
def get_request(endpoint, **kwargs):
    try: return requests.get(backend_url + endpoint + "?" + "&".join([f"{k}={v}" for k, v in kwargs.items()])).json()
    except: return None
def analyze_review_sentiments(text):
    try: return requests.get(sentiment_analyzer_url + "analyze/" + text).json()
    except: return None
def post_review(data_dict):
    try: return requests.post(backend_url + "/insert_review", json=data_dict).json()
    except: return None
EOF

cat > server/djangoapp/views.py << 'EOF'
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import json, logging
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
logger = logging.getLogger(__name__)
def about(request): return render(request, 'djangoapp/about.html')
def contact(request): return render(request, 'djangoapp/contact.html')
def index(request): return render(request, 'djangoapp/Home.html')
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    user = authenticate(username=data['userName'], password=data['password'])
    if user:
        login(request, user)
        return JsonResponse({"userName": data['userName'], "status": "Authenticated"})
    return JsonResponse({"userName": data['userName']})
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    try:
        User.objects.get(username=data['userName'])
        return JsonResponse({"userName": data['userName'], "error": "Already Registered"})
    except User.DoesNotExist:
        user = User.objects.create_user(username=data['userName'], first_name=data['firstName'], last_name=data['lastName'], password=data['password'], email=data['email'])
        login(request, user)
        return JsonResponse({"userName": data['userName'], "status": "Authenticated"})
def get_cars(request):
    if CarMake.objects.count() == 0: initiate()
    return JsonResponse({"CarModels": [{"CarModel": c.name, "CarMake": c.car_make.name} for c in CarModel.objects.select_related('car_make')]})
def get_dealerships(request, state="All"):
    return JsonResponse({"status": 200, "dealers": get_request("/fetchDealers" if state == "All" else f"/fetchDealers/{state}")})
def get_dealer_details(request, dealer_id):
    return JsonResponse({"status": 200, "dealer": get_request(f"/fetchDealer/{dealer_id}")})
def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
    if reviews:
        for r in reviews:
            s = analyze_review_sentiments(r['review'])
            r['sentiment'] = s.get('sentiment', 'neutral') if s else 'neutral'
    return JsonResponse({"status": 200, "reviews": reviews})
@csrf_exempt
def add_review(request):
    if request.user.is_anonymous: return JsonResponse({"status": 403, "message": "Unauthorized"})
    try:
        post_review(json.loads(request.body))
        return JsonResponse({"status": 200})
    except: return JsonResponse({"status": 401, "message": "Error"})
EOF

cat > server/djangoapp/urls.py << 'EOF'
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name = 'djangoapp'
urlpatterns = [
    path('', views.index, name='index'), path('about', views.about, name='about'), path('contact', views.contact, name='contact'),
    path('login', views.login_user, name='login'), path('logout', views.logout_request, name='logout'), path('register', views.registration, name='register'),
    path('get_cars', views.get_cars, name='getcars'), path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOF

cat > server/djangoproj/urls.py << 'EOF'
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views
import os
urlpatterns = [
    path('admin/', admin.site.urls), path('djangoapp/', include('djangoapp.urls')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),
    path('about/', views.about, name='about'), path('contact/', views.contact, name='contact'),
] + static('/static/', document_root=os.path.join(settings.BASE_DIR, 'static'))
EOF

cat > server/frontend/src/App.js << 'EOF'
import React from "react";
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealers/Dealer";
import PostReview from "./components/Dealers/PostReview";
import { Routes, Route } from "react-router-dom";
function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPanel />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}
export default App;
EOF

cat > server/database/app.js << 'EOF'
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;
app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));
mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' });
const Reviews = require('./review');
const Dealerships = require('./dealership');
try {
  Reviews.deleteMany({}).then(() => Reviews.insertMany(reviews_data['reviews']));
  Dealerships.deleteMany({}).then(() => Dealerships.insertMany(dealerships_data['dealerships']));
} catch (error) { console.log(error); }
app.get('/', async (req, res) => res.send("Welcome to the Mongoose API"));
app.get('/fetchReviews', async (req, res) => { try { res.json(await Reviews.find()); } catch (e) { res.status(500).json({ error: 'Error' }); } });
app.get('/fetchReviews/dealer/:id', async (req, res) => { try { res.json(await Reviews.find({ dealership: req.params.id })); } catch (e) { res.status(500).json({ error: 'Error' }); } });
app.get('/fetchDealers', async (req, res) => { try { res.json(await Dealerships.find()); } catch (e) { res.status(500).json({ error: 'Error' }); } });
app.get('/fetchDealers/:state', async (req, res) => { try { res.json(await Dealerships.find({ state: req.params.state })); } catch (e) { res.status(500).json({ error: 'Error' }); } });
app.get('/fetchDealer/:id', async (req, res) => { try { res.json(await Dealerships.find({ id: parseInt(req.params.id) })); } catch (e) { res.status(500).json({ error: 'Error' }); } });
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  const docs = await Reviews.find().sort({ id: -1 });
  const review = new Reviews({ id: docs[0]['id'] + 1, ...data });
  try { res.json(await review.save()); } catch (e) { res.status(500).json({ error: 'Error' }); }
});
app.listen(port, () => console.log(`Server running on http://localhost:${port}`));
EOF

cat > server/Dockerfile << 'EOF'
FROM python:3.12.0-slim-bookworm
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
EOF

cat > server/entrypoint.sh << 'EOF'
#!/bin/bash
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
EOF

cat > server/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dealership
spec:
  replicas: 1
  selector:
    matchLabels:
      run: dealership
  template:
    metadata:
      labels:
        run: dealership
    spec:
      containers:
      - image: us.icr.io/sn-labs-leoduarte6/dealership:latest
        name: dealership
        ports:
        - containerPort: 8000
EOF

mkdir -p .github/workflows
cat > .github/workflows/main.yml << 'EOF'
name: Lint Code
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with: { python-version: '3.12' }
      - run: pip install flake8 && flake8 server/djangoapp/ --exclude=migrations --max-line-length=120
EOF

echo "✅ Done! Now run: cd server && pip install -r requirements.txt && python manage.py makemigrations djangoapp && python manage.py migrate"
