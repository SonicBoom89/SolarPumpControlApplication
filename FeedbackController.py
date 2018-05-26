import RPi.GPIO as GPIO
import time


class FeedbackController:
    FEEDBACK_A_GPIO = 17
    FEEDBACK_B_GPIO = 16

    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # GPIO Nummern statt Board Nummern
        GPIO.setup(self.FEEDBACK_A_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.FEEDBACK_B_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def isInPosition_A(self):
        return GPIO.input(self.FEEDBACK_A_GPIO) == 1 and GPIO.input(self.FEEDBACK_B_GPIO) == 0

    def isInPosition_B(self):
        return GPIO.input(self.FEEDBACK_B_GPIO) == 1 and GPIO.input(self.FEEDBACK_A_GPIO) == 0

    def isSwitching(self):
        return GPIO.input(self.FEEDBACK_B_GPIO) == 0 and GPIO.input(self.FEEDBACK_A_GPIO) == 0

    def cleanUp(self):
        GPIO.clenup()
