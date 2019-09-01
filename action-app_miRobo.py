#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from miio.vacuum import Vacuum

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

IP = None
TOKEN = None
VACUUM = None

class SnipsMiRobot(object):
    """Class used to wrap action code with mqtt connection"""

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # Get parameters
        IP =  self.config.get("secret").get("ip")
        TOKEN =  self.config.get("secret").get("token")

        # init Vaccum
        self.getVacuum()

        # start listening to MQTT
        self.start_blocking()




    def startRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))
        vac = self.getVacuum()
        msg = None
        try:
            vac.start()
        except DeviceException as dev_ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except:
            msg = "Konnte keine Verbindung zum Roboter herstellen."


        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")



    def stopRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))
        vac = self.getVacuum()
        msg = None
        try:
            vac.stop()
        except DeviceException as dev_ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except:
            msg = "Konnte keine Verbindung zum Roboter herstellen."


        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")

    def pauseRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))
        vac = self.getVacuum()
        msg = None
        try:
            vac.pause()
        except DeviceException as dev_ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except:
            msg = "Konnte keine Verbindung zum Roboter herstellen."


        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")

    def findRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))
        vac = self.getVacuum()
        msg = None
        try:
            vac.find()
        except DeviceException as dev_ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except:
            msg = "Konnte keine Verbindung zum Roboter herstellen."


        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")

    def statusRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))
        vac = self.getVacuum()
        msg = None
        try:
            vac.status()
        except DeviceException as dev_ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except:
            msg = "Konnte keine Verbindung zum Roboter herstellen."


        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")


    def sendRoboHome_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))
        vac = self.getVacuum()
        msg = None
        try:
            vac.home()
        except DeviceException as dev_ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except:
            msg = "Konnte keine Verbindung zum Roboter herstellen."


        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")





    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name

        if coming_intent == 'leggodt:startRobo':
            self.startRobo_callback(hermes, intent_message)
        if coming_intent == 'leggodt:stopRobo':
            self.stopRobo_callback(hermes, intent_message)
        if coming_intent == 'leggodt:pauseRobo':
            self.pauseRobo_callback(hermes, intent_message)
        if coming_intent == 'leggodt:findRobo':
            self.findRobo_callback(hermes, intent_message)
        if coming_intent == 'leggodt:statusRobo':
            self.statusRobo_callback(hermes, intent_message)
        if coming_intent == 'leggodt:sendRoboHome':
            self.sendRoboHome_callback(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()


    def getVacuum(self):
        if VACUUM is None:
            VACUUM = Vacuum(IP, TOKEN, 0, 0)
        return VACUUM



if __name__ == "__main__":
    SnipsMiRobot()
