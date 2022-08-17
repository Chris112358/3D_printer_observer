DOMAIN = "observer"

UNAVAILABLE = 'unavailable'

MAX_RETRYS = 1

#  Request calls
REQUEST_CONTROLL = '~M601 S1\r\n'
REQUEST_INFO = '~M115\r\n'
REQUEST_POSITION = '~M114\r\n'
REQUEST_TEMPERATURE = '~M105\r\n'
REQUEST_PROGRESS = '~M27\r\n'
REQUEST_STATUS = '~M119\r\n'

#  Change calls
CHANGE_TEMPERATURE = '~M104 S{} T0\r\n'

# Constants for Socket call
BUFFER = 1024
TIMEOUT = 2

# REGEX Fields
TEMPS = ['T0', 'T1', 'B']
TEMPS_LONG = [item + '_actual' for item in TEMPS] + [item + '_target' for item in TEMPS]
INFOS = ['Type', 'Name', 'Firmware', 'SN', 'X', 'Count']
AXIS = ['X', 'Y', 'Z', 'A', 'B']
STATUS = ['MachineStatus', 'MoveMode', 'Endstop']
PROGRESS = ['Printed', 'Total', 'Percentage']

