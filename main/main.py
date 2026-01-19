# Script for posting input from camera or sensor to AWS via API
# Universal for all stations and sensors
# Edit variables in config.py and see readme file

import os
import sys
import time
import serial
from datetime import datetime
from dateutil import tz
import requests
import json

from config import *
from module.utils.logger import setup_custom_logger  # same import style as miljøstasjon

# --------------------
# Logger
# --------------------
log = setup_custom_logger("kioWebcamVisits")

# Keep same working directory behavior as before
os.chdir("/home/pi/Desktop")

device = DeviceConfig()
common = CommonConfig()
device_name = device.device_name
device_class = get_device_class(device_name)

# Get attributes from config file
width = int(common.picture_width)
height = int(common.picture_height)
crop_width = int(common.crop_width)
crop_height = int(common.crop_height)

picture_title = str(device_class.picture_title)
open_hour = int(device_class.open_hour)
close_hour = int(device_class.close_hour)
open_hour_weekend = int(device_class.open_hour_weekend)
close_hour_weekend = int(device_class.close_hour_weekend)
station_id = int(device_class.station_id)
sensor_id = str(device_class.sensor_id)
device_id = device_class.device_id
enable_double_sensor = device_class.enable_double_sensor
plassering_id = device_class.plassering_id
public_picture_name = device_class.public_picture_name
enable_camera = int(device_class.enable_camera)
enable_sensor = int(device_class.enable_sensor)
enable_blur = device_class.enable_blur


def env_required(name: str) -> str:
    v = os.getenv(name)
    if v is None or v == "":
        raise RuntimeError(f"Mangler miljøvariabel: {name}")
    return v


# PROD is required (matches your prod.env)
lifesignal_api_key_prod = env_required("PROD_API_GATEWAY_LIFESIGNAL_KEY")
lifesignal_api_url_prod = env_required("PROD_API_GATEWAY_LIFESIGNAL_URL")

sensor_api_key_prod = env_required("PROD_API_GATEWAY_SENSOR_KEY")
sensor_api_url_prod = env_required("PROD_API_GATEWAY_SENSOR_URL")

camera_api_key_prod = env_required("PROD_API_GATEWAY_CAMERA_KEY")
camera_api_url_prod = env_required("PROD_API_GATEWAY_CAMERA_URL")

# DEV is optional (only used if both are set)
sensor_api_key_dev = os.getenv("DEV_API_GATEWAY_SENSOR_KEY")
sensor_api_url_dev = os.getenv("DEV_API_GATEWAY_SENSOR_URL")


# Local variables
hours = 0
minutes = 0
seconds = 0
old_minutes = 0
station_status = 0
day = 0
timestamp = 0
prev_minute_picture = 0
prev_minute_lifesignal = 0
date = ""
sensor_timestamp = ""


# Common functions for web camera and sensor
def reboot():
    log.warning("Rebooting soon.")
    time.sleep(65)
    os.system("sudo reboot")


def restart_script():
    log.warning("Restarting script.")
    time.sleep(30)
    os.execv(sys.executable, ["python3"] + sys.argv)


def update_time_date():
    global date, day, hours, minutes, timestamp, sensor_timestamp

    oslo = tz.gettz("Europe/Oslo")
    now = datetime.now(oslo)

    date = now.strftime("%a-%d-%m-%Y")
    day = now.strftime("%a")
    hours = now.hour
    minutes = now.minute
    timestamp = now.strftime("%H:%M:%S")
    sensor_timestamp = now.strftime("%Y%m%dT%H%M%S%z")


def check_opening_hours():
    global station_status

    if day in ["Mon", "Tue", "Wed", "Thu"]:
        station_status = 0 if (hours < open_hour or hours > close_hour) else 1

    elif day in ["Fri", "Sat"]:
        station_status = (
            0 if (hours < open_hour_weekend or hours > close_hour_weekend) else 1
        )

    elif day == "Sun":
        station_status = 0


# Print timestamp each minute to see that code is running.
def print_status():
    global old_minutes

    if minutes != old_minutes:
        check_opening_hours()

        if station_status == 0:
            log.info("%s Station closed", timestamp)
        else:
            log.info("%s Station open", timestamp)

        old_minutes = minutes
        log.info(
            "-------------------------------------------------------------------------------"
        )


# Functions for Webcam only
def take_picture():
    global picture_name
    log.info("Taking picture.")
    try:
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        picture_name = "station_id_{}_{}.jpg".format(station_id, ts)
        title_timestamp = str(datetime.now().strftime("%H:%M"))

        executor = (
            "fswebcam -d /dev/video0 -r "
            + str(width)
            + "x"
            + str(height)
            + "  --set 'Focus, Auto'=False --set 'Focus (absolute)'=2 "
            + "--top-banner --banner-colour '#034B45' --line-colour '#034B45' "
            + "--text-colour '#FFFFFF' --font 'sans:18' --no-shadow --list-controls "
            + "--crop "
            + str(crop_width)
            + "x"
            + str(crop_height)
            + " --title "
            + picture_title
            + title_timestamp
            + " --timestamp 'Oppdater nettsiden hvis bildet er gammelt' "
            + "--jpeg 50 -S 40 "
            + picture_name
        )

        os.system(executor)

        log.info(
            "-------------------------------------------------------------------------------"
        )
        log.info("%s: File %s is saved.", ts, picture_name)
        log.info(
            "-------------------------------------------------------------------------------"
        )

        if enable_blur == 1:
            add_blur(picture_name)

        post_picture_reg_prod(picture_name)

    except Exception:
        log.exception("Error while taking picture")
        time.sleep(600)
        reboot()


def add_blur(picture_name):
    log.info("Adding blur.")
    response = blur(picture_name)  # Separate script adding blur to the picture
    log.info("%s", response)
    log.info(
        "-------------------------------------------------------------------------------"
    )


def delete_picture(picture_name):
    os.remove(picture_name)
    log.info("File deleted successfully from Raspberry Pi: %s", picture_name)
    log.info(
        "-------------------------------------------------------------------------------"
    )


def post_picture_reg_prod(picture_name):
    payload = open(picture_name, "rb")
    headers = {"x-api-key": camera_api_key_prod, "Content-Type": "image/jpeg"}
    log.info("Posting picture to REG AWS Prod: %s %s", datetime.now(), picture_name)
    url = camera_api_url_prod + public_picture_name
    response = requests.request("PUT", url, headers=headers, data=payload)
    log.info("Reply from REG AWS Prod: %s", response.text)
    log.info(
        "-------------------------------------------------------------------------------"
    )
    delete_picture(picture_name)


# Functions for sensors only
def check_sensor():
    if ser_bytes_1.in_waiting > 0:
        ser_bytes_1.read(ser_bytes_1.in_waiting).decode(
            "utf-8"
        )  # Les bytes og tøm køen

        if station_status == 1:
            sensor = "Main sensor"
            save_data_to_file(sensor, "PROD")
            if sensor_api_key_dev and sensor_api_url_dev:
                save_data_to_file(sensor, "DEV")
        else:
            log.info("Visitor outside opening hours main sensor")
            log.info(
                "-------------------------------------------------------------------------------"
            )

    if enable_double_sensor == 1:
        if ser_bytes_2.in_waiting > 0:
            ser_bytes_2.read(ser_bytes_2.in_waiting).decode(
                "utf-8"
            )  # Les bytes og tøm køen

            if station_status == 1:
                sensor = "Second sensor"
                save_data_to_file(sensor, "PROD")
                if sensor_api_key_dev and sensor_api_url_dev:
                    save_data_to_file(sensor, "DEV")
            else:
                log.info("Visitor outside opening hours secondary sensor")
                log.info(
                    "-------------------------------------------------------------------------------"
                )


def save_data_to_file(sensor, environment="PROD"):
    data = {
        "tidspunkt": sensor_timestamp,
        "sensorId": sensor_id,
        "stasjonId": station_id,
        "plasseringId": plassering_id,
    }

    # Determine the file based on environment
    if environment == "PROD":
        file_name = "/home/pi/Desktop/sensor_data_prod.json"
    elif environment == "DEV":
        file_name = "/home/pi/Desktop/sensor_data_dev.json"
    else:
        raise ValueError("Invalid environment. Please choose 'PROD' or 'DEV'.")

    # Save data to file, to ensure secure upload
    with open(file_name, "a") as file:
        json.dump(data, file)
        file.write("\n")

    log.info(
        "Data saved to %s file: %s %s %s", environment, sensor, datetime.now(), data
    )

    try_post_data_from_file(environment)


def try_post_data_from_file(environment="PROD"):
    if environment == "PROD":
        file_name = "/home/pi/Desktop/sensor_data_prod.json"
        api_key = sensor_api_key_prod
        api_url = sensor_api_url_prod
    elif environment == "DEV":
        file_name = "/home/pi/Desktop/sensor_data_dev.json"
        api_key = sensor_api_key_dev
        api_url = sensor_api_url_dev
    else:
        raise ValueError("Invalid environment. Please choose 'PROD' or 'DEV'.")

    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

        if not lines:
            log.info("No data to upload for %s.", environment)
            return

        headers = {"Content-Type": "application/json", "x-api-key": api_key}

        # Store lines that failed to upload, so we can save them back to the file
        remaining_lines = []

        for line in lines:
            data_dict = json.loads(line.strip())
            data_json = json.dumps(data_dict, ensure_ascii=False).encode("utf8")
            log.info("Uploading from %s file.", environment)

            response = requests.post(api_url, headers=headers, data=data_json)

            if response.status_code == 200:
                log.info(
                    "Successfully uploaded data to %s: %s", environment, response.text
                )
            else:
                log.warning(
                    "Failed to upload data to %s. Keeping in file. Response: %s %s",
                    environment,
                    response.text,
                    data_json,
                )
                remaining_lines.append(line)

        # Save the lines that failed to upload back to the file
        with open(file_name, "w") as file:
            file.writelines(remaining_lines)

        log.info(
            "-------------------------------------------------------------------------------"
        )

    except FileNotFoundError:
        log.info("No file found for %s. No data to upload.", environment)
    except Exception as e:
        log.exception(
            "An error occurred while uploading data to %s: %s", environment, e
        )
        restart_script()
        log.info(
            "-------------------------------------------------------------------------------"
        )


# Functions for Raspberry Pi monitoring (lifesignal to AWS)
def send_lifesignal_prod():
    try:
        payload = json.dumps({"sensor_id": device_id})
        headers = {
            "x-api-key": lifesignal_api_key_prod,
            "Content-Type": "application/json",
        }
        log.info("Posting lifesignal to REG AWS Prod: %s %s", datetime.now(), payload)
        response = requests.request(
            "POST", lifesignal_api_url_prod, headers=headers, data=payload
        )
        log.info("Reply from REG AWS Prod: %s", response.text)
        log.info(
            "-------------------------------------------------------------------------------"
        )
    except Exception:
        log.exception("Error sending lifesignal")
        restart_script()
        return


# Main loop
update_time_date()
check_opening_hours()
log.info(
    "Starting program: Device name=%s | Sensor=%s | Camera=%s | Blur=%s",
    device_name,
    enable_sensor,
    enable_camera,
    enable_blur,
)
log.info(
    "-------------------------------------------------------------------------------"
)

# Take picture at startup
if enable_camera == 1:
    from kioGradualBlur import blur

    take_picture()

# These variables establishes communication via serial
if enable_sensor == 1:
    # Clear upload queue
    log.info("Checking for unuploaded data.")
    try_post_data_from_file(environment="PROD")
    if sensor_api_key_dev and sensor_api_url_dev:
        try_post_data_from_file(environment="DEV")

    # send_lifesignal_prod()
    prev_minute_lifesignal = minutes
    ser_bytes_1 = serial.Serial("/dev/ttyUSB0", 9600)
    if enable_double_sensor == 1:
        ser_bytes_2 = serial.Serial("/dev/ttyUSB1", 9600)

while True:
    if __name__ == "__main__":
        try:
            update_time_date()
            check_opening_hours()
            print_status()

            # Send lifesignal to AWS
            if minutes in [0, 6, 12, 18, 24, 30, 36, 42, 48, 54]:
                if enable_sensor == 1 and minutes != prev_minute_lifesignal:
                    prev_minute_lifesignal = minutes
                    # send_lifesignal_prod()

            # Read sensor or camera
            if station_status == 1:
                if minutes in [0, 10, 20, 30, 40, 50] and enable_camera == 1:
                    if minutes != prev_minute_picture:
                        prev_minute_picture = minutes
                        take_picture()

                if enable_sensor == 1:
                    check_sensor()

            # Reboot Raspberry Pi (kept as before)
            if hours == 5 and minutes == 10:
                reboot()

            time.sleep(5)

        except Exception:
            log.exception("Unhandled error in main loop")
            restart_script()
