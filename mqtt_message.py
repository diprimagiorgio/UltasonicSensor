import paho.mqtt.client as mqtt
#sort of singleton class, I want to initialize just one Client, and reuse it
class MyMQTT:
    __instance__  : mqtt.Client = None

    def __init__(self, host: str, port: int ):
        if not MyMQTT.__instance__ :
            MyMQTT.__instance__ = mqtt.Client()
            MyMQTT.__instance__.connect(host, port)

    @staticmethod
    def send(topic, message, host="localhost", port=1883):
        my_mqtt = MyMQTT(host, port)
        # send mqtt message
        MyMQTT.__instance__.publish(topic,message)
        return