# webhook-repo

This is my Flask webhook app.

It listens to GitHub events
and stores them in MongoDB.

---

## What it does

- Receives Push events
- Receives Pull Request events
- Detects Merge events
- Stores data in MongoDB
- Shows events from last X minutes

---

## Tech used

- Python
- Flask
- MongoDB Atlas
- PyMongo
- Ngrok

---

## Setup

### 1. Create virtual env
# webhook-repo

This is my Flask webhook app.

It listens to GitHub events
and stores them in MongoDB.

---

## What it does

- Receives Push events
- Receives Pull Request events
- Detects Merge events
- Stores data in MongoDB
- Shows events from last X minutes

---

## Tech used

- Python
- Flask
- MongoDB Atlas
- PyMongo
- Ngrok

---

## Setup

### 1. Create virtual env
python -m venv venv
venv\Scripts\activate
### 2. Install packages
### 2. Install packages


pip install -r requirements.txt


---

## MongoDB Setup

1. Create cluster in MongoDB Atlas
2. Create database user
3. Add your IP in Network Access
4. Get connection string

Add this in `.env` file:


MONGO_URI=your_mongodb_connection_string


---

## Run app


python app.py


Runs on:
http://127.0.0.1:5000

---

## Start ngrok


ngrok http 5000


Copy HTTPS URL
Paste it in action-repo webhook settings.

---

## Endpoints

POST /webhook  
→ receives GitHub events  
→ stores in MongoDB  

GET /events?minutes=10  
→ shows events from last 10 minutes  

---

## Example output

Ashiq pushed to main on 01 March 2026 - 04:52 PM UTC  
Ashiq submitted a pull request from feature to main  
Ashiq merged branch feature to main  

---

That’s it.
