# PlanMyEscape

PlanMyEscape is a Flask-based travel planning API with a React front-end that helps users plan their vacations, calculate budgets, and manage travel itineraries with ease. The application allows users to enter vacation dates, budget information, and origin to find and save customized travel options.

## Features

- **Vacation Planning**: Users can input vacation dates to calculate required days off, accounting for weekends and holidays.
- **Budget Planning**: Based on the user's origin and budget, the app recommends top travel packages tailored to the user's preferences.
- **Full Travel Itinerary**: Users can review and adjust the estimated costs for flights, accommodation, and local transportation.
- **Bookkeeping**: Users can track travel expenses by entering categories, descriptions, and amounts, with an option to delete records.
- **Authentication**: Users can log in, sign up, and access features based on their login status.

## Tech Stack

- **Backend**: Flask, MongoDB, Gunicorn
- **Frontend**: React, Bootstrap
- **Deployment**: Gunicorn, Flask-CORS

## Prerequisites

- **Python 3.x**
- **Node.js & npm**
- **MongoDB**: To store user and travel data
- **Gunicorn**: For running the application in production

## Setup Instructions

### Backend

1. **Clone the repository**:
   ```bash
   git clone https://github.com/OldAlexhub/py-panmyescape.git
   cd PlanMyEscape
   ```
