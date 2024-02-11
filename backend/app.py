import requests
import os
import psycopg2
from dotenv import load_dotenv
from amadeus import Client, ResponseError, Location
from flask import Flask, render_template
from flask_cors import CORS
#apis: [flightdates, flightofferssearch, flightdelay,pointsofinterest, airportontime]
#maybe apis: [flightorders, flightorder, ]
#conn = psycopg2.connect("dbname=? user=? password=?")

app = Flask(__name__,template_folder="Templates")

load_dotenv()
amadeus = Client(client_id=os.getenv('API_KEY'), client_secret=os.getenv('API_SECRET'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orig/<start_point>/<end_point>/<dep_date>/<adult_count>')
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

""" @app.route('/flightdate/<org>/<dest>')
def flight_get_dates(org, dest):
    try:
        response = amadeus.shopping.flight_dates.get(origin=org, destination=dest)
    except ResponseError as error:
        return error
    return response.result """

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

@app.route('/ontime/<ac>/<date>')
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