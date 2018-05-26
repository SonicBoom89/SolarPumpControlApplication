from flask import Flask, abort, jsonify, request

import PoolTransitionError
from Logger import Logger
from SolarPumpController import PoolpumpMode, SolarPumpController
from time import localtime, strftime

app = Flask(__name__)


class Rest_API:

    def __init__(self):
        self._log = Logger()
        self._solarController = SolarPumpController();

    def startWebApi(self):
        app.run(debug=True, host="0.0.0.0", threaded=True)

    @app.route('/poolpump', methods=['GET', 'PUT'])
    def poolpump(self):
        if request.method == 'PUT':
            return self.poolpump_put(request)
        else:
            return self.poolpump_get(request)

    def poolpump_get(self, request):
        self._log.info("GET Request received: " + str(request))
        poolpumpStatus = self._solarController.getPoolpumpMode()
        self._log.info("Poolpump Status [" + str(poolpumpStatus) + "]")
        return jsonify(Device="Poolpump", Status=poolpumpStatus,
                       Timestamp=strftime("%a, %d %b %Y %H:%M:%S +0000", localtime()))

    def poolpump_put(self, request):
        self._log.info("PUT Request received: " + str(request))
        requestedModeParam = request.form.get('SelectedMode', None)
        if requestedModeParam is None:
            response = "SelectedMode not set!"
            abort(400)
        else:
            requestedMode = PoolpumpMode[requestedModeParam]
            try:
                self._solarController.switchToMode(requestedMode)
                response = "Poolpump successfully set to " + str(requestedMode)
            except PoolTransitionError as error:
                abort(400)
                response = "Error, trying to switch poolpump from " \
                           + str(error.previous) \
                           + " -> " \
                           + str(error.next) \
                           + " (" + str(error.message) + ")"
                self._log.error(response)

        return jsonify(result=response)
