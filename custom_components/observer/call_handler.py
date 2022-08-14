import socket
import logging

try:
	from .const import BUFFER, TIMEOUT
	from .const import REQUEST_CONTROLL
except ImportError:
	from const import BUFFER, TIMEOUT
	from const import REQUEST_CONTROLL


_LOGGER = logging.getLogger(__name__)


def send_and_get(addr, msg):
	'''sends a call to the printer and returns a string of the recieved data'''

	printer = socket.socket()
	printer.settimeout(TIMEOUT)
	try:
		printer.connect((addr['ip'], addr['port']))
		printer.send(msg.encode())
		data = printer.recv(BUFFER)
		printer.close()

		return data.decode()
	except TimeoutError:
		return None
	except Exception as inst:
		_LOGGER.exception('Something went wrong while connecting to Printer')
		return None


def recieve(addr, msg):

	send_and_get(addr, REQUEST_CONTROLL)
	data = send_and_get(addr, msg)

	return data


if __name__ == '__main__':

	#Testing
	addr = {'ip': '192.168.178.98',
		    'port': 8899}

	import encodedata as ed

	print(ed.get_head(addr))
	print(ed.get_info(addr))
	print(ed.get_progress(addr))
	print(ed.get_status(addr))
	print(ed.get_temp(addr))
