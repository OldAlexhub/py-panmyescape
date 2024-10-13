from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
from datetime import datetime
import holidays
import pymongo
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

mongo_url = os.getenv('MONGO_URL')
client = pymongo.MongoClient(mongo_url)
db = client['test']
users_collection = db['users']
details_collection = db['details']
dataset_collection = db['dataset']

users = pd.DataFrame(list(users_collection.find()))
details = pd.DataFrame(list(details_collection.find()))
dataset = pd.DataFrame(list(dataset_collection.find()))

app = Flask(__name__)
CORS(app)

@app.route("/", methods= ['POST'])
def homePage():
    return 'Hello World'

@app.route('/vacation', methods=['POST'])
def get_dates():
    try:
        data = request.get_json()
        from_date = data.get('fromDate')
        to_date = data.get('toDate')

        # Check if from_date and to_date are present
        if not from_date or not to_date:
            return jsonify({'error': 'Please provide both fromDate and toDate'}), 400

        # Convert dates to datetime objects
        from_date = pd.to_datetime(from_date)
        to_date = pd.to_datetime(to_date)

        # Define the U.S. holidays for the given range of dates
        us_holidays = holidays.US(years=range(from_date.year, to_date.year + 1))

        # Generate date range
        date_range = pd.date_range(from_date, to_date)
        holidays_in_range = [date for date in date_range if date in us_holidays]
        weekdays = date_range[date_range.dayofweek < 5]  # Weekdays (Monday=0, Friday=4)
        weekends = date_range[date_range.dayofweek >= 5]  # Weekends (Saturday=5, Sunday=6)

        # Prepare a list to hold results
        day_off_requests = []

        for day in date_range:
            if day in holidays_in_range or day in weekends:
                day_off_requests.append((day, "Not Needed"))
            else:
                day_off_requests.append((day, "Request Day Off"))

        # Create a DataFrame for better readability and convert to dictionary format
        result_df = pd.DataFrame(day_off_requests, columns=["Date", "Status"])
        
        holidays_count = len(holidays_in_range)
        weekdays_excluding_holidays = len([day for day in weekdays if day not in holidays_in_range])
        weekends_excluding_holidays = len([day for day in weekends if day not in holidays_in_range])
        
        
        results = result_df.to_dict(orient='records')

        return jsonify({'results': results, 'holidays': holidays_count, 'Weekdays': weekdays_excluding_holidays, 'weekends': weekends_excluding_holidays}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/completing', methods=['POST'])
def get_completed():
    try:
        data = request.get_json()
        origin = str(data.get('origin')).upper() 
        budget = int(data.get('budget'))
        
        # Ensure details has data and 'totalDays' column exists and is numeric
        if 'totalDays' not in details.columns or details.empty:
            return jsonify({'error': 'totalDays column missing or details dataframe is empty'}), 500
        
        totalDays = details['totalDays'].iloc[0]
        
        # Convert totalDays to float to ensure compatibility
        try:
            totalDays = float(totalDays)
        except ValueError:
            return jsonify({'error': 'totalDays must be a numeric value'}), 500
        
        # Calculate DailyBudget after confirming types
        DailyBudget = (budget / totalDays)
        
        # Filter dataset based on the origin and DailyBudget
        filtered_data = dataset[(dataset['origin'] == origin) & 
                                (dataset['funBudget'] <= DailyBudget)]
        
        # Check if filtered_data contains any results
        if filtered_data.empty:
            return jsonify({'error': 'No travel options available for the specified budget and origin'}), 200
        
        topThree = filtered_data.head(3)
        results_dict = topThree.to_dict(orient='records')
        # Convert any ObjectId in the results to strings
        for record in results_dict:
            record['_id'] = str(record.get('_id', ''))
        
        return jsonify({'results': results_dict}), 200
                      
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)