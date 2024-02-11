import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError, Location
from flask import Blueprint, render_template
import psycopg2
import threading
import requests

load_dotenv()
amadeus = Client(client_id=os.getenv('API_KEY'), client_secret=os.getenv('API_SECRET'))

try:
    # Connect to the PostgreSQL server
    connection = psycopg2.connect(
        host=os.getenv('host'),
        port=os.getenv('port'),
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password')
    )
    
    # Create a cursor object using the connection
    cursor = connection.cursor()
    
    # Define SQL queries
    summer_query = "SELECT * FROM summertravel;"
    winter_query = "SELECT * FROM wintertravel;"
    
    # Execute the summer query
    cursor.execute(summer_query)
    
    # Fetch and process results for summer travel
    summer_rows = cursor.fetchall()
    
    # Execute the winter query
    cursor.execute(winter_query)
    
    # Fetch and process results for winter travel
    winter_rows = cursor.fetchall()
    
    # Close the cursor and connection
    cursor.close()
    
except psycopg2.Error as e:
    print("Error: Could not connect to PostgreSQL database:", e)

app_blueprint = Blueprint('app_blueprint',__name__)

@app_blueprint.route('/')
def index():
    return render_template("index.html")

@app_blueprint.route('/index')
def index_click():
    return render_template("index.html")

@app_blueprint.route('/about')
def about():
    return render_template("about.html")

@app_blueprint.route('/flight')
def flight():
    return render_template("flight.html")

@app_blueprint.route('/flightNo')
def flightNo():
    return render_template("flightNo.html")

@app_blueprint.route('/flightYes')
def flightYes():
    return render_template("flightYes.html")

@app_blueprint.route('/orig/<start_point>/<end_point>/<dep_date>/<adult_count>', methods=['GET'])
def find_cheapest_on_specific_date(start_point, end_point, dep_date, adult_count):
    try:
        response = amadeus.shopping.flight_offers_search.get(
        originLocationCode=start_point,
        destinationLocationCode=end_point,
        departureDate=dep_date,
        adults=adult_count
    )
    except ResponseError as error:
        return error
    
    return response.result
    
def late_params(response):
    orig_loc, dest_loc, dept_date, dept_time, arv_date, arv_time, ac, cc, num, loc = [], [], [], [], [], [], [], [], [], []
    for i in range(len(response['data'])): #all results
        for j in range(len(response['data'][i]['itineraries'][0]['segments'])): #each partial flight
            orig_loc.append(response['data'][i]['itineraries'][0]['segments'][j]['departure']['iataCode']) #origin location MAD
            dest_loc.append(response['data'][i]['itineraries'][0]['segments'][j]['arrival']['iataCode']) #destination location EWR
            dept_date.append(response['data'][i]['itineraries'][0]['segments'][j]['departure']['at'][0:10]) #dep date 2024-11-01
            dept_time.append(response['data'][i]['itineraries'][0]['segments'][j]['departure']['at'][11:]) #dep time: 10:50:00
            arv_date.append(response['data'][i]['itineraries'][0]['segments'][j]['arrival']['at'][0:10]) #arrival date: 2024-11-01
            arv_time.append(response['data'][i]['itineraries'][0]['segments'][j]['arrival']['at'][11:]) #arrival time: 13:25:00
            ac.append(response['data'][i]['itineraries'][0]['segments'][j]['aircraft']['code']) #aircraft code: 763
            cc.append(response['data'][i]['itineraries'][0]['segments'][j]['carrierCode']) #carrier code: UA 
            num.append(response['data'][i]['itineraries'][0]['segments'][j]['number']) #number: 50
            loc.append(response['data'][i]['itineraries'][0]['duration']) #origin location: PT11H35M
    #delays = delay_percentage(orig_loc,dest_loc,dept_date,dept_time,arv_date,arv_time,ac,cc,num,loc)
    return ((orig_loc, dest_loc, dept_date, dept_time, arv_date, arv_time, ac, cc, num))

def running_threads(json):
    delays = []
    for i in range(len(json)):
        delays.append(json['data'][i]['probability'])
    return delays

""" def delay_percentage(orig_loc, dest_loc, dept_date, dept_time, arv_date, arv_time, ac, cc, num, loc):
    for i in range(len())
    try:
        response = amadeus.travel.predictions.flight_delay.get(originLocationCode=orig_loc,
destinationLocationCode=dest_loc, departureDate=dept_date, departureTime=dept_time, arrivalDate=arv_date, arrivalTime=arv_time, aircraftCode=ac, carrierCode=cc, flightNumber=num, duration=loc)
    except ResponseError as error:
        return error

    thread = threading.Thread(target=running_threads, args=(response.result,))
    thread.start()
    thread.join() """
    
@app_blueprint.route('/ontime/<ac>/<date>')
def on_time_percentage(ac, date):
    try:
        response = amadeus.airport.predictions.on_time.get(airportCode=ac, date=date)
    except ResponseError as error:
        return error
    return response.result

cheap_resp_res = find_cheapest_on_specific_date('MAD','BOS','2024-11-01','1')
#print(late_params(resp_res))
otp_resp_res = on_time_percentage('JFK','2024-09-01')
on_time = otp_resp_res['data']['probability']
print(on_time)
    

