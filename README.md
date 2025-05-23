# ✈️ Skyscanner Flight Price Tracker

This is a simple Python app that checks Skyscanner flight prices and sends you an email when prices match your preferences.

## 📦 What It Does

- Tracks flight prices from Skyscanner using the [Skyscanner RapidAPI](https://rapidapi.com/skyscanner/api/skyscanner44/).
- Parses your preferences from a `config.json` file:

  - Departure/Return dates
  - Preferred time windows
  - Price range
  - Origin and destination airports (IATA codes like MNL, NRT)

- Sends you an email notification when flights match your criteria.

## ⚙️ Configuration

Create a file named `config.json` in the same folder:

```json
{
  "origin": "MNL",
  "destination": "NRT",
  "departure_date": "2025-10-23",
  "return_date": "2025-10-29",
  "departure_time_range": "00:00-03:00",
  "return_time_range": "18:00-22:00",
  "price_min": 7000,
  "price_max": 9000,
  "check_interval_hours": 6,
  "email": {
    "enabled": true
  }
}
```

## 🔐 .env File

Create a `.env` file for your API key and email credentials:

```env
SKYSCANNER_API_KEY=your_skyscanner_rapidapi_key
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=your_email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_PASSWORD=your_gmail_app_password
```

## ▶️ Running the App

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app manually:

```bash
python main.py
```

## ☁️ Free Deployment Options

- [Render.com](https://render.com/) — use a cron job or background worker
- [GitHub Actions](https://docs.github.com/en/actions) — run every few hours with a cron schedule

## 🧠 Notes

- Use [Gmail App Passwords](https://myaccount.google.com/apppasswords) if using Gmail.
- Set the `check_interval_hours` in `config.json` for your scheduler.

## ✅ Example Use Case

Track flights from Manila (MNL) to Tokyo Narita (NRT) for Oct 23-29, 2025. Get an alert if there's a red-eye departure (1 AM) and evening return (6-10 PM) and the round-trip cost is ₱7000–₱9000.

---

Made for travelers who like to snipe deals without refreshing Skyscanner every hour. 🧳
