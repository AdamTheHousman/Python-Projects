from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime

#import json

app = Flask(__name__)
key = ""

@app.route('/')
def main():
    return redirect('/city')
 
@app.route("/city", methods = ["POST", "GET"])
def city():
    if request.method == "POST":
        cityName = request.form("name")
        return render_template('weather.html', name = cityName)
    else:
        return render_template("city.html")


@app.route("/weather", methods = ['POST', 'GET'])
def weather():
    cityName = request.form.get("name")
    # Get current weather report and load data
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=%s,us&APPID=%s" % (cityName, key))
    weatherData = r.json()
    data = weatherData["weather"]
    weather = weatherData["main"]
    for d in data:
        iconCode = d["icon"]
    iconUrl = "http://openweathermap.org/img/w/" + iconCode + ".png"
    temp = weather["temp"]
    tempF = (9/5)*(temp-273) + 32
    
    return render_template('weather.html', name = cityName, iconUrl = iconUrl, temp = tempF)

@app.route("/fig/<cityName>")
def fig(cityName):
    import matplotlib.pyplot as plt
    from io import BytesIO
    from flask import send_file
    # Get weather forecast and load data
    r = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=%s,us&APPID=%s" % (cityName, key))
    weatherData = r.json()
    data = weatherData["list"]
    weather = []
    tempDates = []
    for d in data:
        weather.append(d["main"])
        tempDates.append(d["dt_txt"])
    dates = []
    for date in tempDates:
        datetime_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        dates.append(datetime_object)
    temps = []
    for item in weather:
        temp = item['temp']
        temp = (9/5)*(temp-273) + 32
        temps.append(temp)
    fig = plt.figure()
    plt.plot(dates, temps)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500
	
if __name__ == '__main__':
  app.run(debug = True)

