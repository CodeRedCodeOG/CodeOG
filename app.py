from dotenv import load_dotenv
from flask import Flask
from app_blueprint import app_blueprint
#apis: [flightdates, flightofferssearch, flightdelay,pointsofinterest, airportontime]
#maybe apis: [flightorders, flightorder, ]

app = Flask(__name__)
app.register_blueprint(app_blueprint)

""" @app.route('/flightdate/<org>/<dest>')
def flight_get_dates(org, dest):
    try:
        response = amadeus.shopping.flight_dates.get(origin=org, destination=dest)
    except ResponseError as error:
        return error
    return response.result """

if __name__ == '__main__':
    app.run()