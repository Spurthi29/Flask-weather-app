import requests, os, json
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def weather():
    if request.method == "POST":
        city = request.form["city"]
    else:
        city = "bangalore"
    api_key = "49d38129abd0212858bb60c7c1b4581a"
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api_key + '&units=metric')

    retrieve = response.json()
    file_path = os.path.join(app.root_path, 'static', 'city.json')
    with open(file_path, "w") as json_file:
        json.dump(retrieve, json_file)

    if response.status_code == 200:
        data = {
            "city": retrieve["name"],
            "temprature": str(retrieve["main"]["temp"]),
            "humidity": str(retrieve["main"]["humidity"]),
            "pressure": str(retrieve["main"]["pressure"]),
            "description": str(retrieve["weather"][0]["description"]),
            "icon": retrieve["weather"][0]["icon"],
        }
    else:
        data = {
            "city": str(retrieve["message"]),
            "icon": "04n",
            "city_name": city
        }
    print(f"##################### {data}")

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
