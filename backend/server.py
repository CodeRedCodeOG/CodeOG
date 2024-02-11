import requests
import os
import psycopg2
from dotenv import load_dotenv
from amadeus import Client, ResponseError, Location
#apis: [flightdates, flightofferssearch, flightdelay,pointsofinterest, airportontime]
#maybe apis: [flightorders, flightorder, ]
load_dotenv()
amadeus = Client(client_id=os.getenv('API_KEY'), client_secret=os.getenv('API_SECRET'))
#conn = psycopg2.connect("dbname=? user=? password=?")
#origin loc, destination loc, dep date, dep time, arrive date, arrive time, aircraft code, carrier code, flight num, duration
try:
    response = amadeus.airport.predictions.on_time.get(
                airportCode='JFK',
                date='2024-09-01')

except ResponseError as error:
    print(error)

print(response.result['data']['probability'])