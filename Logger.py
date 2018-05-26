import logging


class Logger:
    logger = None

    def setUpLocalLogger(self):
        self.logger = logging.getLogger('SolarPumpControlApplication')
        hdlr = logging.FileHandler('SolarPumpControlApplication.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)
