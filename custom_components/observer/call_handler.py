import socket
import logging
import asyncio

try:
	from .const import BUFFER, TIMEOUT
	from .const import REQUEST_CONTROLL
except ImportError:
	from const import BUFFER, TIMEOUT
	from const import REQUEST_CONTROLL


_LOGGER = logging.getLogger(__name__)


async def send_and_get(addr, msg):
	'''sends a call to the printer and returns a string of the recieved data'''

	printer = socket.socket()
	printer.settimeout(TIMEOUT)
	loop = asyncio.get_event_loop()

	try:

		await loop.sock_connect(printer, (addr['ip'], addr['port']))
		await loop.sock_sendall(printer, msg.encode() )
		data = await loop.sock_recv(printer, BUFFER)
		printer.close()

		return data.decode()
	except TimeoutError:
		return None
	except ConnectionRefusedError:
		_LOGGER.exception('Invalid Server, probably a wrong Port')
		return None
	except Exception as inst:
		_LOGGER.exception('Something went wrong while connecting to Printer')
		return None


async def recieve(addr, msg):
	'''Package the controll send and recieve data calls to the socket server'''
	try:
		test = await asyncio.wait_for(send_and_get(addr, REQUEST_CONTROLL), timeout=TIMEOUT)
	except asyncio.exceptions.TimeoutError:
		test = None
	except Exception:
		_LOGGER.exception('Something went wrong while sending the controll sequence to the server')

	if not test is None:
		data = await send_and_get(addr, msg)
		return data
	else:
		return None


if __name__ == '__main__':

	#Testing
	addr = {'ip': '192.168.178.198',
		    'port': 8899}

	import encodedata as ed

	print(asyncio.run(ed.get_head(addr)))

	print('Still working')

	'''
	print(ed.get_head(addr))
	print(ed.get_info(addr))
	print(ed.get_progress(addr))
	print(ed.get_status(addr))
	print(ed.get_temp(addr))
	'''
