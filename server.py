from gpiozero import PWMLED
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

# from fastapi.responses import HTMLResponse
import json
import csv
import time
from datetime import datetime

from time import sleep

import config
from components.calorieCalculator import calculate_calories_burned

# this is just a fake out class for testing without gpiozero
class FAKEPWM:
    def __init__(self, value=0.0):
        self.value = value

try:
    pwm = PWMLED(12, frequency=20)  # GPIO pin 12 for PWM control
except Exception as e:
    print(f"Could not initialize PWMLED: {e}")
    print("Using fake PWM class for testing.")
    pwm = FAKEPWM()

app = FastAPI()
# dictionary to store speed, incline, distance values
data_log = {
    "speed": 0.0, #the pwm value will be between 0 and 1, representing 0 to max speed
    "incline": 0.0, #the incline value will be between 0 and 10, representing 0 to max incline
    "distance": 0.0,
    "heart_rate": 120,
    "calories": 0,
    "duration_seconds": 678,
    "start_time": "",
    "duration": 0
}

start_time = 0

# websocket to listen to frontend and send updated data_log dictionary
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        data_json = json.loads(data)
        
        # calculate and set calories burned
        calories = calculate_calories_burned(
            config.config["gender"],
            config.config["age"],
            config.config["weight_lbs"],
            data_log["heart_rate"],
            data_log["duration_seconds"] / 60,
        )
        data_log["calories"] = calories
        # print(f"Calculated calories: {calories:.2f}")

        if data_json["type"] == "start":
            current_datetime = datetime.now() 
            data_log["start_time"] = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print("Workout started")
            # zero out distance and calories
            data_log["distance"] = 0.0
            data_log["calories"] = 0.0
            data_log["speed"] = 0.0

        if data_json["type"] == "stop":
            print("Workout stopped")
            # log data to csv file
            with open("workout_log.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        data_log["start_time"],
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        data_log["distance"],
                        data_log["calories"],
                    ]
                )
        
        if data_json["type"] == "speedSet":
            if data_json["value"] == "increase":
                if pwm.value >= 0.98: #don't exceed max speed
                    data_log["speed"] = 1
                    pwm.value = 1
                elif pwm.value < 0.98:
                    data_log["speed"] += 0.02
                    pwm.value += 0.02
                print(f"Speed increased to {data_log['speed']} from input of {data_json["value"]}")            
            elif data_json["value"] == "decrease":
                if pwm.value <= 0.02: #don't go below 0 speed
                    data_log["speed"] = 0
                    pwm.value = 0
                elif pwm.value > 0.02:
                    data_log["speed"] -= 0.02
                    pwm.value -= 0.02
                print(f"Speed decreased to {data_log['speed']} from input of {data_json["value"]}")
            elif isinstance(data_json["value"], (int, float)):
                # check if value is between 0 and 10
                if data_json["value"] < 0:
                    data_json["value"] = 0
                elif data_json["value"] > 10:
                    data_json["value"] = 10                
                data_log["speed"] = data_json["value"] / 10
                pwm.value = data_json["value"] / 10
                print(f"Speed set to {data_log['speed']} from input of {data_json["value"]}")
        
        if data_json["type"] == "inclineSet":
            if data_json["value"] == "increase":
                if data_log["incline"] < 10:
                    data_log["incline"] += 1
                print(f"Incline increased to {data_log['incline']}")
            elif data_json["value"] == "decrease":
                if data_log["incline"] > 0:
                    data_log["incline"] -= 1
                print(f"Incline decreased to {data_log['incline']}")
            elif isinstance(data_json["value"], (int, float)):
                # check if value is between 0 and 10
                if data_json["value"] < 0:
                    data_json["value"] = 0
                elif data_json["value"] > 10:
                    data_json["value"] = 10                
                data_log["incline"] = data_json["value"]
                print(f"Incline set to {data_log['incline']}")
        
        # calculate duration in seconds
        if data_log["start_time"] != "":
            start_dt = datetime.strptime(data_log["start_time"], "%Y-%m-%d %H:%M:%S")
            current_dt = datetime.now()
            duration = current_dt - start_dt
            data_log["duration_seconds"] = int(duration.total_seconds())
            data_log["duration"] = str(duration).split(".")[0]  # HH:MM:SS format

        #update front end every second with current data_log
        await websocket.send_text(json.dumps(data_log))
        # await sleep(1)
        


        


app.mount("/", StaticFiles(directory="static", html=True), name="static")
# app.mount("/", StaticFiles(directory="svelteFrontend/build", html=True), name="static")


# from signal import pause

# gpio16 = LED(16)
# gpio13 = LED(13)

# while True:
#   red.on()
#  sleep(1)
# red.off()
# sleep(1)

# @app.get("/speed")
# async def speed(value: float = 0.5):
#     start = pwm.value
#     finish = value
#     print(f"here is value {pwm.value}")
#     speed_step(start, finish)
#     return {"message": "pulsing pin 36, GPIO 16"}

# @app.get("/speed0")
# async def speed(value: float = 0.5):
#     pwm.value = 0
#     return {"message": "pulsing pin 36, GPIO 16"}

# @app.get("/speed4")
# async def speed(value: float = 0.5):
#     pwm.value = 0.4
#     return {"message": "pulsing pin 36, GPIO 16"}

# @app.get("/speed10")
# async def speed(value: float = 0.5):
#     pwm.value = 1
#     return {"message": "pulsing pin 36, GPIO 16"}

# @app.get("/on")
# async def on():
#     # gpio16.on()
#     return {"message": "turning on pin 36, GPIO 16"}


# @app.get("/off")
# async def off():
#     # gpio16.off()
#     return {"message": "turning off pin 36, GPIO 16"}


# @app.get("/speedUp")
# async def speedup(value: float = 0.05):
#     if pwm.value >= 0.95:
#         pwm.value = 1
#         return {"message" : f"speed increased by {value}, new speed {pwm.value}"}
#     pwm.value = pwm.value + 0.05
#     print(f"here is value {pwm.value}")
#     return {"message" : f"speed increased by {value}, new speed {pwm.value}"}

# @app.get("/speedDown")
# async def speeddown(value: float = 0.05):
#     if pwm.value <= 0.05:
#         pwm.value = 0
#         return {"message" : f"speed decreased by {value}, new speed {pwm.value}"}
#     pwm.value = pwm.value - 0.05
#     print(f"here is value {pwm.value}")
#     return {"message" : f"speed decreased by {value}, new speed {pwm.value}"}
