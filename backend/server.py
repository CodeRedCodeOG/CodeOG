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
    print("Summer Travel:")
    for row in summer_rows:
        print(row)  # Print each row
    
    # Execute the winter query
    cursor.execute(winter_query)
    
    # Fetch and process results for winter travel
    winter_rows = cursor.fetchall()
    print("Winter Travel:")
    for row in winter_rows:
        print(row)  # Print each row
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    
except psycopg2.Error as e:
    print("Error: Could not connect to PostgreSQL database:", e)
