import time
from PoolTransitionError import PoolTransitionError
from RelaisController import RelaisController
from FeedbackController import FeedbackController
from PoolpumpMode import PoolpumpMode
from Logger import Logger


class SolarPumpController:

    TIME_TO_SWITCH_MODE_SECONDS = 13

    def __init__(self):
        self._log = Logger()
        self._relaisController = RelaisController()
        self._feedbackController = FeedbackController()

    def switchToMode(self, poolPumpMode):
        self._log.info("Switching to " + str(poolPumpMode))
        if poolPumpMode == PoolpumpMode.Normal:
            if not self._feedbackController.isSwitching() and not self._feedbackController.isInPosition_B():
                self._powerOn()
                time.sleep(1)
                self._setPumpModeNormal()
                time.sleep(self.TIME_TO_SWITCH_MODE_SECONDS)
                self._powerOff()
            else:
                raise PoolTransitionError(PoolpumpMode.Switching, poolPumpMode, "Pump is still switching!")
        elif poolPumpMode == PoolpumpMode.Solar:
            if not self._feedbackController.isSwitching() and not self._feedbackController.isInPosition_A():
                self._powerOn()
                time.sleep(1)
                self._setPumpModeSolar()
                time.sleep(self.TIME_TO_SWITCH_MODE_SECONDS)
                self._powerOff()
            else:
                raise PoolTransitionError(PoolpumpMode.Switching, poolPumpMode, "Pump is still switching!")
        else:
            self._log.warn("Mode not supported!")

    def getPoolpumpMode(self):
        mode = None
        if self._feedbackController.isInPosition_A():
            mode = PoolpumpMode.Solar
        elif self._feedbackController.isInPosition_B():
            mode = PoolpumpMode.Normal
        elif self._feedbackController.isSwitching():
            mode = PoolpumpMode.Switching
        self._log.info("Retrieving Poolpumpmode -> " + str(mode))
        return mode

    def _powerOn(self):
        self._relaisController.openRelais_B()  # Strom ein

    def _powerOff(self):
        self._relaisController.closeRelais_B()  # Strom aus

    def _setPumpModeNormal(self):
        self._relaisController.openRelais_A()  # Ventil auf

    def _setPumpModeSolar(self):
        self._relaisController.closeRelais_A()  # Ventil zu

    def dispose(self):
        self._log.info("Disposing SolarController...")
        self._feedbackController.cleanUp()
        self._relaisController.cleanUp()
