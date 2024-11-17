from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import random
import pickle
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

app = Flask(__name__)
model = pickle.load(open("fp_predict.pkl", "rb"))

csv_path = 'data/flight_price.csv'
df = pd.read_csv(csv_path)

@app.route("/")
@cross_origin()
def index():
    return render_template("index.html",prediction_text="",graph_html="")


@app.route("/predict", methods=["GET","POST"])
@cross_origin()
def predict():

    valid_sources = ['Delhi', 'Kolkata', 'Mumbai', 'Chennai','Banglore']
    valid_destinations = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata','Banglore']

    if request.method == "POST":
        Source = request.form["Source"]
        Destination = request.form["Destination"]   

        if Source not in valid_sources or Destination not in valid_destinations:
            return render_template("index.html", prediction_text="Data not found for the selected locations.", graph_html="")
        

        month_prices = []
        dates = []

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        dep_date = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M")
        dep_month = dep_date.month
        dep_year = dep_date.year

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        # Total Stops
        Total_stops = int(request.form["stops"])

        Dep_Time = request.form["Dep_Time"]
        Arrival_Time = request.form["Arrival_Time"]

        # Get the current month and year
        today = datetime.today()
        current_year = today.year
        current_month = today.month

        base_price = 5000

        for day in range(1, 32):
            try:
               date = datetime(current_year, current_month, day)
               if date.weekday() >= 5:  # Saturday or Sunday
                   price = base_price + (date.weekday() * 1000)  # increase price on weekends
               else:  
                   price = base_price - (date.weekday() * 500)  # decrease price on weekdays

               price = min(price, 12000)
               month_prices.append(price)
               dates.append(date.strftime("%Y-%m-%d"))

            except ValueError:
                continue

        fig = go.Figure(data=[go.Scatter(x=dates, y=month_prices, mode='lines+markers', name='Flight Fare')])

        fig.update_layout(title='Fare Insights for the month',
                          xaxis_title='Date',
                          yaxis_title='Price (Rs)',
                          showlegend=True)
        
        graph_html = fig.to_html(full_html=False)


        # Airline
        airline = request.form['airline']
        if (airline == 'Jet Airways'):
            Jet_Airways = 1
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'IndiGo'):
            Jet_Airways = 0
            IndiGo = 1
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Air India'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 1
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Multiple carriers'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 1
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'SpiceJet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 1
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Vistara'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 1
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'GoAir'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 1
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Multiple carriers Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 1
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Jet Airways Business'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 1
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Vistara Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 1
            Trujet = 0

        elif (airline == 'Trujet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 1

        else:
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0


        Source = request.form["Source"]
        if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
            s_Banglore = 0

        elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0
            s_Banglore = 0

        elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0
            s_Banglore = 0

        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1
            s_Banglore = 0
        
        elif (Source == 'Banglore'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
            s_Banglore = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
            s_Banglore = 0

        Destination = request.form["Destination"]
        if (Destination == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Destination == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Destination == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif (Destination == 'Kolkata'):
            d_Cochin= 0
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0


        s_Delhi = 1 if Source == 'Delhi' else 0
        s_Kolkata = 1 if Source == 'Kokata' else 0
        s_Mumbai = 1 if Source == 'Mumbai' else 0
        s_Chennai = 1 if Source == 'Chennai' else 0

        d_Cochin = 1 if Destination == 'Cochin' else 0
        d_Delhi = 1 if Destination == 'Delhi' else 0
        d_Hyderabad = 1 if Destination == 'Hyderabad' else 0
        d_Kolkata = 1 if Destination == 'Kolkata' else 0
        

        prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            s_Banglore,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,    
            d_Kolkata 
        ]])

        output = round(prediction[0], 2)

        return render_template('index.html', prediction_text="Your predicted fare is Rs. {}".format(output), graph_html=graph_html,
                                           Source=Source, 
                                           Destination=Destination,
                                           Dep_Time=Dep_Time,
                                           Arrival_Time=Arrival_Time,
                                           Total_stops=Total_stops,
                                           airline=airline)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)