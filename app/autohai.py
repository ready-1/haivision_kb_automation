import json
import requests
import toml
from pprint import pprint


def get_config():
    try:
        with open('toml/channel.toml', 'r') as f:
            c = toml.loads(f.read())
    except Error as e:
        return f'ERROR: {e}'
    return c


def read_template_file(filename):
    try:
        with open(f'json/{filename}', 'r') as f:
            t = json.loads(f.read())
    except Error as e:
        return f'ERROR: {e}'
    return t


def encoder_login(ip_address, username, password):
    url = "https://" + ip_address + ":1080/ecs/auth.json"
    payload = "{\n\"username\" :  \"" + username + \
        "\",\n\"password\" :  \"" + password + "\"\n}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False)
    session_id = json.loads(response.text)["sessionid"]
    return session_id


def encoder_logout(ip_address, session_id):
    url = "https://" + ip_address + ":1080/ecs/auth.json?Authorization=" + session_id
    payload = {}
    headers = {
        'Authorization': session_id
    }
    response = requests.request(
        "DELETE", url, headers=headers, data=payload, verify=False)
    return True


session_id = encoder_login("192.168.130.83", "haiadmin", "manager")
encoder_logout("192.168.130.83", session_id)
