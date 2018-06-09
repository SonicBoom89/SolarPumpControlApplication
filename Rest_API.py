from flask import Flask, abort, jsonify, request

import PoolTransitionError
from Logger import Logger
from SolarPumpController import PoolpumpMode, SolarPumpController
from HardwareController import HardwareController
from time import localtime, strftime
from threading import Thread

app = Flask(__name__)

_log = Logger()
_solarController = SolarPumpController()
_hardwareController = HardwareController()

def startWebApi():
        app.run(debug=True, host="0.0.0.0", threaded=True)

@app.route('/poolpump')
def poolpump_get():
	_log.info("GET Request received: " + str(request))
        poolpumpStatus = _solarController.getPoolpumpMode()
        _log.info("Poolpump Status [" + str(poolpumpStatus) + "]")
	cpuTemp = _hardwareController.getCpuTemp()
        return jsonify(Device="Poolpump", Status=str(poolpumpStatus), CpuTemp=str(cpuTemp),
                       Timestamp=str(strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))

@app.route('/poolpump/on')
def poolpump_on():
	_log.info("Turn on GET Request received: " + str(request))
        #requestedModeParam = request.form.get('SelectedMode', None)
	requestedModeParam = "Solar"
	if requestedModeParam is None:
            response = "SelectedMode not set!"
            abort(400)
        else:
            requestedMode = PoolpumpMode[requestedModeParam]
            try:
		_solarController.switchToMode(requestedMode)
                response = "Poolpump successfully set to " + str(requestedMode)
            except PoolTransitionError as error:
                abort(400)
                response = "Error, trying to switch poolpump from " \
                           + str(error.previous) \
                           + " -> " \
                           + str(error.next) \
                           + " (" + str(error.message) + ")"
                _log.error(response)

	cpuTemp = _hardwareController.getCpuTemp()
	return jsonify(result=response, CpuTemp=str(cpuTemp))

@app.route('/poolpump/off')
def poolpump_off():
        _log.info("Turn off GET Request received: " + str(request))
        #requestedModeParam = request.form.get('SelectedMode', None)
        requestedModeParam = "Normal"
        if requestedModeParam is None:
            response = "SelectedMode not set!"
            abort(400)
        else:
            requestedMode = PoolpumpMode[requestedModeParam]
            try:
                _solarController.switchToMode(requestedMode)
                response = "Poolpump successfully set to " + str(requestedMode)
            except PoolTransitionError as error:
                abort(400)
                response = "Error, trying to switch poolpump from " \
                           + str(error.previous) \
                           + " -> " \
                           + str(error.next) \
                           + " (" + str(error.message) + ")"
                _log.error(response)

	cpuTemp = _hardwareController.getCpuTemp()
	return jsonify(result=response, CpuTemp=str(cpuTemp))


startWebApi()
