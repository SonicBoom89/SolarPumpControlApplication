import time

class HardwareController:

    cpuTempFile = "/sys/class/thermal/thermal_zone0/temp"

    def getCpuTemp(self):
        with open(self.cpuTempFile) as tempFile:
            temp = tempFile.read()
            temp = float(temp) / 1000
            return temp




print(HardwareController().getCpuTemp())

