# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# def get_request(endpoint, **kwargs):
# Add code for get requests to back end
def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key, value in kwargs.items():
            params = params+ key + "=" + value + "&"
    request_url = backend_url+endpoint+"?"+params
    # For example, if 
    # If backend_url is "http://localhost:3030", 
    # endpoint is "/api/data", and you pass id="123"
    # full URL will be: "http://localhost:3030/api/data?id=123&"
    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")


# Get sentiment analyzer
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "/analyze/" + text
    try:
        # Call get method of requests library with URL and params
        response = requests.get(request_url)
        # DEBUG: Print raw response to find issues
        print("Sentiment API Response Status:", response.status_code)
        print("Sentiment API Response Text:", response.text)
        if response.status_code == 200:
            return response.json().get("sentiment", "unknown")
        else:
            print("Error: Received non-200 status code.")
            return "error"
        
    except Exception as err:
        print(f"Unexpected {err = }, {type(err) = }")
        print("Network exception occured.")


# POST a review for a dealer 
def post_review(data_dict):
    """
    Add a review for specific dealer
    """
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url, json = data_dict)
        print(response.json())
        return response # Return the full response as object
    except Exception as exc:
        print("Network exception occured.", exc)
        return None


