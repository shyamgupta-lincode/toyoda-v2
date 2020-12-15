import serial
import serial.tools.list_ports as list_ports
import datetime
import sys
import time

def list_all_ports():
	for port,pid,hwid in sorted(list_ports.comports()):
		print(port,pid,hwid)
	if not list_ports.comports():
		print('No devices found')

class toyoda_io():
	def __init__(self,vid_pid):
		x=self.fetch_port(vid_pid)
		if x != "Device not found":
			connection_status = self.initialise(x)
		else :
			print(x)
			sys.exit(0)
		if connection_status == False:
			print('Serial Not connected')
			sys.exit(0)
		elif connection_status == True:
			print('Serial connected')
			time.sleep(3)
			self.write(8,0)

	def __send_command__(self,data):
		self.client.write(data)
		start = datetime.datetime.now()
		while datetime.datetime.now() - start < datetime.timedelta(seconds=1):
			if self.client.in_waiting:
				x=self.client.readline()
				# print(x)
				return(x)
		return False


	def fetch_port(self,vid_pid):
		try:
			for port,pid,hwid in sorted(list_ports.comports()):
				try:
					print(hwid)
					print(hwid.split())
					print((hwid.split())[1])
					print(((hwid.split())[1]).split('='))
					print((((hwid.split())[1]).split('='))[1])
					print((hwid.split())[2])
					print(((hwid.split())[2]).split('='))
					print((((hwid.split())[2]).split('='))[1])
					if ((hwid.split())[1].split('='))[1] == vid_pid:
						print(port)
						return port
				except:
					print("Skip")
			return "Device not found"
		except:
			return "Retry"

	def initialise(self,port):
		
		self.client = serial.Serial(port,timeout=1)
		return self.client.name == port

	def read(self,address):
		#write - (read_:4)
		#read - (4:1)for on / (4:0) for off
		response = self.__send_command__(b'*read_:'+str(address).encode()+b'__\r\n')
		if response != False:
			response = response.decode()
			# print(len(response))
			if len(response) == 5:
				# print('r',(response[0]))
				if int(response[0]) == address:
					# print(response[2])
					return int(response[2])
				else:
					return False
			else:
				return False
		else:
			return False

	def write(self,address,val):
		self.__send_command__(b'*write:'+str(address).encode()+b':'+str(1-val).encode()+b'\r\n')

		return self.read(address)==(1-val)