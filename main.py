#!/usr/local/bin/python3 -tt

import random
import decimal
import time
from datetime import datetime
import requests
import config
from envirophat import weather


def main():
    # Squelch warning about unverified SSL cert for HTTPS - we know the API is OK!
    requests.packages.urllib3.disable_warnings()

    value = measure()
    status = sendToAPI(value)
    log(status)


def measure():
    return round(weather.temperature(), 2)


def sendToAPI(value):
    apiUrl = config.api["url"]
    token = config.api["token"]
    data = {
        "value": value,
        "location": "Ambient",
        # Epoch time in milliseconds
        "measuredAt": time.time() * 1000
    }

    req = requests.post(
        apiUrl, headers={"Authorization": "Bearer " + token}, verify=False, json=data)

    saveToFile(data)

    if (req.status_code == 200):
        return "Successfully sent data to API!"
    else:
        return "Error sending data to the API! Status code: " + req.status_code


def saveToFile(data):
    line = str(data["value"]) + "\t" + data["location"] + \
        "\t" + str(data["measuredAt"]) + "\n"
    file = open("values.txt", "a")
    file.write(line)
    file.close()


def log(message):
    logFile = open("log.txt", "a")
    logFile.write(str(datetime.now()) + "\t" + message + "\n")
    logFile.close()


if __name__ == "__main__":
    main()
