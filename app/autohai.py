import json
import requests
import toml
from pprint import pprint

IPADDRESS = "192.168.130.83"  # "192.168.128.71"


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


def encoder_create_channel(ip_address, session_id, channel_name):
    url = "https://" + ip_address + ":1080/ecs/channels.json"
    channel = {"channel": {"label": channel_name}}
    payload = json.dumps(channel)
    headers = {
        'Authorization': session_id,
        'Content-Type': 'application/json'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False)
    return response.text.encode('utf8')


def encoder_delete_channel(ip_address, session_id, channel_name):
    url = "https://" + ip_address + ":1080/ecs/channels/" + channel_name + ".json"
    channel = {"channel": {"label": channel_name}}
    payload = json.dumps(channel)
    headers = {
        'Authorization': session_id,
        'Content-Type': 'application/json'
    }
    response = requests.request(
        "DELETE", url, headers=headers, data=payload, verify=False)
    print(response.text.encode('utf8'))


session_id = encoder_login(IPADDRESS, "haiadmin", "manager")


# encoder_logout(IPADDRESS, session_id)

# encoder_create_channel(IPADDRESS, session_id, "Test_Channel_From_API")
encoder_delete_channel(IPADDRESS, session_id, "API_Channel")
