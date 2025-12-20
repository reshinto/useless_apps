import requests
import json
import time


_SERVER = "https://home.sensibo.com/api/v2"


class SensiboClientAPI(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def _get(self, path, **params):
        params["apiKey"] = self._api_key
        response = requests.get(_SERVER + path, params=params)
        response.raise_for_status()
        return response.json()

    def _patch(self, path, data, **params):
        params["apiKey"] = self._api_key
        response = requests.patch(_SERVER + path, params=params, data=data)
        response.raise_for_status()
        return response.json()

    def devices(self):
        result = self._get("/users/me/pods", fields="id,room")
        return {x["room"]["name"]: x["id"] for x in result["result"]}

    def pod_measurement(self, podUid):
        result = self._get("/pods/%s/measurements" % podUid)
        return result["result"]

    def pod_ac_state(self, podUid):
        result = self._get("/pods/%s/acStates" % podUid, limit=1, fields="acState")
        return result["result"][0]["acState"]

    def pod_change_ac_state(self, podUid, currentAcState, propertyToChange, newValue):
        self._patch(
            "/pods/%s/acStates/%s" % (podUid, propertyToChange),
            json.dumps({"currentAcState": currentAcState, "newValue": newValue}),
        )


# source .venv/bin/activate
# python main.py api_key device_name
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sensibo client example parser")
    parser.add_argument("apikey", nargs="?", default=None)
    parser.add_argument("deviceName", nargs="?", default=None)
    args = parser.parse_args()

    apikey = args.apikey or "my own sensibo api key"
    deviceName = args.deviceName or "my own sensibo device name"

    SECONDS = 60  # 1 minute
    MINUTES = 60  # 1 hour
    SLEEP_SECONDS = SECONDS * MINUTES  # 1 hour

    while True:
        print("checking current AC condition:")
        client = SensiboClientAPI(apikey)
        devices = client.devices()
        print("devices:", devices)

        uid = devices[deviceName]
        ac_state = client.pod_ac_state(uid)
        print("AC State", ac_state)
        if not ac_state.get("on"):
            print("AC was turned off, turning AC on")
            client.pod_change_ac_state(uid, ac_state, "on", not ac_state["on"])

        print(f"Sleeping for {SLEEP_SECONDS // 60} minutes...\n")
        time.sleep(SLEEP_SECONDS)
