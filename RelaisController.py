import RPi.GPIO as GPIO
import time


class RelaisController:

    RELAIS_A_GPIO = 3
    RELAIS_B_GPIO = 4

    def __init__(self):
        GPIO.setmode(GPIO.BCM)                    # GPIO Nummern statt Board Nummern
        GPIO.setup(self.RELAIS_A_GPIO, GPIO.OUT)  # GPIO Modus zuweisen
        GPIO.setup(self.RELAIS_B_GPIO, GPIO.OUT)

    def openRelais_A(self):
        GPIO.output(self.RELAIS_A_GPIO, GPIO.LOW)

    def openRelais_B(self):
        GPIO.output(self.RELAIS_B_GPIO, GPIO.LOW)

    def closeRelais_A(self):
        GPIO.output(self.RELAIS_A_GPIO, GPIO.HIGH)

    def closeRelais_B(self):
        GPIO.output(self.RELAIS_B_GPIO, GPIO.HIGH)

    def cleanUp(self):
        GPIO.cleanup()
