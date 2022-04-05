from paho.mqtt import client as mqtt
import time as stime
import ssl
import calendar
import datetime
import json
import random
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib import parse
from hmac import HMAC


def generate_sas_token(_uri, _key, _policy_name, _expiry=3600):
    ttl = time() + _expiry
    sign_key = "%s\n%d" % ((parse.quote_plus(_uri)), int(ttl))
    print("SIGN KEY", sign_key)
    signature = b64encode(HMAC(b64decode(_key), sign_key.encode('utf-8'), sha256).digest())

    raw_token = {
        'sr':  uri,
        'sig': signature,
        'se': str(int(ttl))
    }

    if policy_name is not None:
        raw_token['skn'] = _policy_name
    return 'SharedAccessSignature ' + parse.urlencode(raw_token)


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed for m" + str(mid))


def on_connect(client, userdata, flags, rc, *args):
    print('ON CONNECT', client, userdata, flags, rc, args)
    #print("Connected with result code " + str(rc))


def on_message(client, userdata, message):
    print(
        "Received message '"
        + str(message.payload)
        + "' on topic '"
        + message.topic
        + "' with QoS "
        + str(message.qos)
    )


def on_log(client, userdata, level, buf):
    print("log: ", buf)


device_id = "refrigerator"  # Add device id
iot_hub_name = "itohubdemo1"  # Add iot hub name
resource_uri = iot_hub_name + ".azure-devices.net" + "/" + "devices" + "/" + device_id
policy_name = "iothubowner"
"""
Shared Access Policy 	Permissions
iothubowner 	        All permission
service 	            ServiceConnect permissions                 
device 	                DeviceConnect permissions                  
registryRead 	        RegistryRead permissions                   
registryReadWrite 	    RegistryRead and RegistryWrite permissions 

more at https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-dev-guide-sas?tabs=node
"""

uri = resource_uri
key = "cKyY8ED2I5bN7mgUqPXOVtyO4IkqFpjMw09tNZuyk4A="
expiry = 3600
policy = "iothubowner"
sas_token = generate_sas_token(uri, key, policy, expiry)


# Subscriber
print('CREATE SUBSCRIBER')
subscriber = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311, clean_session=False)
subscriber.on_log = on_log
subscriber.tls_set_context(context=None)

# Set up client credentials
username = "{}.azure-devices.net/{}/api-version=2018-06-30".format(
    iot_hub_name, device_id
)
subscriber.username_pw_set(username=username, password=sas_token)

# Connect to the Azure IoT Hub
subscriber.on_connect = on_connect
subscriber.connect(iot_hub_name + ".azure-devices.net", port=8883)
subscriber.on_message = on_message
subscriber.on_subscribe = on_subscribe
subscriber.subscribe(
    "devices/{device_id}/messages/devicebound/#".format(device_id=device_id)
)

subscriber.loop_start()

print("SAS", sas_token)
print('CREATE PUBLISHER')
publisher = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311, clean_session=False)
publisher.on_log = on_log
publisher.tls_set_context(context=None)

# Set up client credentials
username = "{}.azure-devices.net/{}/api-version=2018-06-30".format(
    iot_hub_name, device_id
)
publisher.username_pw_set(username=username, password=sas_token)

# Connect to the Azure IoT Hub
publisher.on_connect = on_connect
publisher.connect(iot_hub_name + ".azure-devices.net", port=8883)

# Publish
stime.sleep(1)
for x in range(3):
    print('PUBLISHING FOR', x + 1)
    exp = datetime.datetime.utcnow()
    abcstring1 = {"AI01": random.randint(0, 100)}
    data_out1 = json.dumps(abcstring1)
    publisher.publish(
        "devices/{device_id}/messages/events/".format(device_id=device_id),
        payload=data_out1,
        qos=1,
        retain=False,
    )
    print("Publishing on devices/" + device_id + "/messages/events/", data_out1)
    stime.sleep(3)


subscriber.loop_stop()
publisher.loop_stop()
