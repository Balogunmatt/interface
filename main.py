import requests
import datetime as dt
import smtplib

my_lat = 6.524379
my_long = 3.379206

my_email = "balogunmatthew01@gmail.com"
pwd = "zmmbswsqygwqfhwq"


def iss_data():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])
    if my_lat - 5 <= iss_lat <= my_lat + 5:
        return True


def night_time():
    parameter = {
        "lat": my_lat,
        "lng": my_long,
        "formatted": 0
    }
    connection = requests.get("https://api.sunrise-sunset.org/json", params=parameter)
    connection.raise_for_status()
    data = connection.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]
    sunrise_hour = int(sunrise.split("T")[1].split(":")[0])
    sunset_hour = int(sunset.split("T")[1].split(":")[0])

    time_now = dt.datetime.now().hour
    if time_now >= sunset_hour or time_now <= sunrise_hour:
        return True

if iss_data() and night_time():
    with smtplib.SMTP("smtp.gmail.com") as mail_connection:
        mail_connection.starttls()
        mail_connection.login(user=my_email, password=pwd)
        mail_connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject: ISS notification\n\nThe ISS is near your region"
        )
