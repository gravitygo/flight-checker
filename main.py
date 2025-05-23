import json
import requests
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load config
with open('config.json') as f:
    config = json.load(f)

API_URL = "https://skyscanner44.p.rapidapi.com/search"
HEADERS = {
    "X-RapidAPI-Key": os.getenv("SKYSCANNER_API_KEY"),
    "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
}

# Parse config values
origin = config['origin']
destination = config['destination']
departure_date = config['departure_date']
return_date = config['return_date']
dep_time_start, dep_time_end = config['departure_time_range'].split('-')
ret_time_start, ret_time_end = config['return_time_range'].split('-')
price_min = config['price_min']
price_max = config['price_max']

# Email setup
email_enabled = config['email']['enabled']
email_from = os.getenv("EMAIL_FROM")
email_to = os.getenv("EMAIL_TO")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT", 587))
email_password = os.getenv("EMAIL_PASSWORD")

def send_email(subject, body):
    if not email_enabled:
        return
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_from, email_password)
        server.send_message(msg)

def fetch_flights():
    params = {
        "adults": "1",
        "origin": origin,
        "destination": destination,
        "departureDate": departure_date,
        "returnDate": return_date,
        "currency": "PHP"
    }
    response = requests.get(API_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print("Failed to fetch flights")
        return []
    return response.json().get('itineraries', [])

def filter_flights(itineraries):
    matches = []
    for flight in itineraries:
        price = flight.get('price', {}).get('raw', 999999)
        if price_min <= price <= price_max:
            legs = flight.get('legs', [])
            if not legs:
                continue
            dep_time = legs[0]['departure'][-5:]
            ret_time = legs[-1]['arrival'][-5:]
            if dep_time >= dep_time_start and dep_time <= dep_time_end and \
               ret_time >= ret_time_start and ret_time <= ret_time_end:
                matches.append((price, flight))
    return matches

def main():
    print(f"Checking flights from {origin} to {destination} on {departure_date}...")
    flights = fetch_flights()
    matches = filter_flights(flights)
    if matches:
        body = "Matching flights found:\n\n"
        for price, flight in matches:
            link = flight.get('deeplink', 'N/A')
            body += f"Price: ₱{price}\nLink: {link}\n\n"
        send_email("[Flight Alert] Matching Price Found", body)
        print("Email sent.")
    else:
        print("No matching flights found.")

if __name__ == "__main__":
    main()
