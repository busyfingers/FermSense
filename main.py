#!/usr/local/bin/python3 -tt

import time
from datetime import datetime
import requests
import config
from envirophat import weather


def main():
    # Squelch warning about unverified SSL cert for HTTPS - we know the API is OK!
    requests.packages.urllib3.disable_warnings()

    try:
        process_backup()
        measure_and_send()
    except Exception as ex:
        log("Exception while running script: " + ", ".join(ex.args))


def process_backup():
    unsuccessful_lines = send_backup_data(read_from_file())
    resave_failed(unsuccessful_lines)


def measure_and_send():
    sendToAPI(get_measurement_data())


def send_backup_data(content):
    failed_lines = []
    for line in content:
        values = list(map(str.strip, line.split("\t")))
        data = {
            "value": values[0],
            "location": values[1],
            # Epoch time in milliseconds
            "measuredAt": values[2]
        }

        success = sendToAPI(data)

        if not success:
            failed_lines.append(line)

    return failed_lines


def get_measurement_data():
    return {
        "value": measureTemperature(),
        "location": config.location,
        # Epoch time in milliseconds
        "measuredAt": time.time() * 1000
    }


def measureTemperature():
    return round(weather.temperature(), 2)


def sendToAPI(data):
    status = False
    apiUrl = config.api["url"]
    token = config.api["token"]

    req = requests.post(
        apiUrl, headers={"Authorization": "Bearer " + token}, verify=False, json=data)

    if (req.status_code == 200):
        log("Successfully sent data to API!")
    else:
        saveToFile(data)
        log("Error sending data to the API! Status code: " + req.status_code)

    return status


def read_from_file():
    file = open("values.txt", "r")
    content = file.readlines()
    file.close()

    if len(content) < 1:
        return []
    else:
        return content


def resave_failed(content):
    file = open("values.txt", "w")
    file.writelines(content)
    file.close()


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
