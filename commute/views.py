import random
from django.shortcuts import render
from .api import geocode_location, fetch_traffic_data
from .scraper import scrape_traffic_news

def predict_delay(rain_mm=10, day_of_week=3):
    from sklearn.linear_model import LinearRegression
    import numpy as np

    data = np.array([
        [0, 0, 5],
        [10, 1, 15],
        [20, 2, 30],
        [0, 3, 6],
        [5, 4, 10],
        [30, 5, 45],
        [0, 6, 4]
    ])
    X = data[:, :2]
    y = data[:, 2]

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[rain_mm, day_of_week]])[0]
    return round(pred, 2)

def dashboard(request):
    location = request.GET.get("location")
    lat, lon = None, None
    traffic_info = None
    news = []
    chart_data = None
    delay_prediction = None
    error = None
    searched_location = None

    if location:
        lat, lon = geocode_location(location)

        if lat and lon:
            searched_location = location

            traffic_info = fetch_traffic_data(lat, lon)

            chart_values = [random.randint(5, 20) for _ in range(5)]
            chart_data = {
                "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                "values": chart_values
            }

            delay_prediction = predict_delay(
                rain_mm=random.randint(0, 20),
                day_of_week=random.randint(0, 6)
            )

            
            news = scrape_traffic_news(location)

        else:
            error = f"Could not geocode the location: {location}"

    else:
        delay_prediction = round(random.uniform(5, 30), 2)
        chart_data = {
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "values": [5, 8, 6, 7, 9]
        }

    context = {
        "searched_location": searched_location,
        "traffic_info": traffic_info,
        "delay_prediction": delay_prediction,
        "chart_data": chart_data,
        "news": news,
        "error": error,
        "lat": lat,
        "lon": lon,
        "tomtom_api_key": "AQC32Ji96lt815SPIrptJWeOBYsLuDcv",
    }

    return render(request, "commute/dashboard.html", context)
