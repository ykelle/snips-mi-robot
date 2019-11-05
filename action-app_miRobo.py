#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from valetudo import Valetudo, ValetudoError, ValetudoConnectionError, ValetudoRequestError

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class SnipsMiRobot(object):
    """Class used to wrap action code with mqtt connection"""

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # Get parameters
        self.ip =  self.config.get("secret").get("ip")

        # init Vacuum
        self.vacuum = Valetudo(ip=self.ip)

        # start listening to MQTT
        self.start_blocking()




    def startRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))
        msg = None
        try:
            self.vacuum.start_cleaning()
        except ValetudoConnectionError as ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except ValetudoRequestError:
            msg = "Der Roboter konnte das leider nicht ausführen"


        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")



    def stopRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        msg = None
        try:
            self.vacuum.stop_cleaning()
        except ValetudoConnectionError as ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except ValetudoRequestError:
            msg = "Der Roboter konnte das leider nicht ausführen"

        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")

    def pauseRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        msg = None
        try:
            self.vacuum.pause_cleaning()
        except ValetudoConnectionError as ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except ValetudoRequestError:
            msg = "Der Roboter konnte das leider nicht ausführen"

        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")

    def findRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        msg = None
        try:
            self.vacuum.find()
        except ValetudoConnectionError as ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except ValetudoRequestError:
            msg = "Der Roboter konnte das leider nicht ausführen"

        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")

    def statusRobo_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        msg = None
        try:
            self.vacuum.get_status()
        except ValetudoConnectionError as ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except ValetudoRequestError:
            msg = "Der Roboter konnte das leider nicht ausführen"

        if msg is not None:
            # if need to speak the execution result by tts
            hermes.publish_start_session_notification(intent_message.site_id, msg, "")


    def sendRoboHome_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        msg = None
        try:
            self.vacuum.send_home()
        except ValetudoConnectionError as ex:
            msg = "Konnte keine Verbindung zum Roboter herstellen."
        except ValetudoRequestError:
            msg = "Der Roboter konnte das leider nicht ausführen"

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


if __name__ == "__main__":
    SnipsMiRobot()
