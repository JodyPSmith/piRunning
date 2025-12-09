from gpiozero import PWMLED
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse
import json
import csv
import time
from time import sleep

import config
from components.calorieCalculator import calculate_calories_burned

app = FastAPI()


# dictionary to store speed, incline, distance values
data_log = {
    "speed": 0.0,
    "incline": 0.0,
    "distance": 0.0,
    "heart_rate": 120,
    "calories": 0,
    "duration_seconds": 678,
    "start_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
}

start_time = ""


# websocket to listen to frontend and send updated data_log dictionary
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_text()
        print(data)
        calories = calculate_calories_burned(config.config["gender"], config.config["age"], config.config["weight_lbs"], data_log["heart_rate"], data_log["duration_seconds"] / 60)
        data_log["calories"] = calories
        print(f"Calculated calories: {calories:.2f}")
        if data == "start":
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data_log["start_time"] = start_time
            # zero out distance and calories
            data_log["distance"] = 0.0
            data_log["calories"] = 0.0
        elif data == "stop":
            print("Workout stopped")
            # log data to csv file
            with open('workout_log.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([data_log["start_time"], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), data_log["distance"], data_log["calories"]])
        else:
            data_json = json.loads(data)
            if data_json["type"] == "speedSet":
                if data_json["value"] == "increase":
                    data_log["speed"] += 0.1
                elif data_json["value"] == "decrease":
                    data_log["speed"] -= 0.1
            elif data_json["type"] == "inclineSet":
                if data_json["value"] == "increase":
                    data_log["incline"] += 0.1
                elif data_json["value"] == "decrease":
                    data_log["incline"] -= 0.1
        

        await websocket.send_text(json.dumps(data_log))


app.mount("/", StaticFiles(directory="static", html=True), name="static")
# app.mount("/", StaticFiles(directory="svelteFrontend/build", html=True), name="static")



# from signal import pause

# gpio16 = LED(16)
# gpio13 = LED(13)
pwm = PWMLED(12)
# while True:
#   red.on()
#  sleep(1)
# red.off()
# sleep(1)

def speed_step(start, finish):
    # determine the difference between the start and finish speeds and reduce the difference by 0.1 each 500ms until finish speed is reached
    step = 0.1 if start < finish else -0.1
    sequence = []
    speed = start
    while (speed <= finish) if step > 0 else (speed >= finish):
        pwm.value = float(f"{speed:.1f}")
        sleep(0.5)  # 500ms delay
        speed += step
    return

# @app.get("/on")
# async def on():
#     # gpio16.on()
#     return {"message": "turning on pin 36, GPIO 16"}


# @app.get("/off")
# async def off():
#     # gpio16.off()
#     return {"message": "turning off pin 36, GPIO 16"}


@app.get("/speed")
async def speed(value: float = 0.5):
    start = pwm.value
    finish = value
    print(f"here is value {pwm.value}")
    speed_step(start, finish)
    return {"message" : "pulsing pin 36, GPIO 16"}

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
