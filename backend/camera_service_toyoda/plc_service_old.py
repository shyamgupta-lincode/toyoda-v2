from toyoda_io import *
import time
import datetime
import redis
from common_utils import *
from setting_keys import *
import random
from print_qr_image import *


t = toyoda_io("2341:0043")
print(t.read(5))

#to connect to the Arduino using the following command
#t= toyoda_io("vid_pid","ser")

#for getting the vid_pid and ser, use the following command
#toyoda_io.list_all_ports()

#example : t=toyoda_io("1A86:7523","5")

#to read a pin use the following command
#t.read(address)
#t.read(9)
#it will return 1/0 based on the status of the pin
#Address for reading the pushbutton is 9

#to write use the following command
#t.write(address,val)
#t.write(8,1)
#the function will write 1/0 to the given address based on the value written in the val location

wid = json.load(open("workstation_id.json"))
data = RedisKeyBuilderServer(wid).workstation_info
rch = CacheHelper()
#simple example
started = 0
part_status = None

while 1:

	#redis accepted / rejected - #TO DO
	# started = random.choice([0,1])
	# print(started)
	try:
		if started == 1 and ((datetime.datetime.now()-start) >= datetime.timedelta(seconds=5)):
			started=0
			#set redis keyholder to start the process

			t.write(8,0)

		time.sleep(0.2)

		if t.read(5) == 1:
			rch.set_json({RedisKeyBuilderServer(wid).get_key(0,process_start_keyholder) : True}) 
			print(1)

		if rch.get_json(RedisKeyBuilderServer(wid).get_key(0,process_completed)) == True:


			#-------------------do the process--------------------
			if rch.get_json(RedisKeyBuilderServer(wid).get_key(0,part_accepted_keyholder)) :
				# part_status = "Good"
				start=datetime.datetime.now()
				started=1
				t.write(8,1)
				qr_string = rch.get_json(RedisKeyBuilderServer(wid).get_key(0,qr_string_keyholder))
				# print("imgggggggggggggggggggggg::::", type(img))
    			# print("imgggggggggggggggggggggg11111::::", img)
				
				if bool(qr_string):
					decode_base64_into_image(bytes(qr_string,'ascii'))
					print_qrImage()
			# else:
			# 	part_status == 'NG'

			# if part_status == 'Good':
			# 	start=datetime.datetime.now(),
			# 	started=1
			# 	t.write(8,1)
			# 	# rch.set_json({RedisKeyBuilderServer(wid).get_key(0,part_accepted_keyholder) : False}) 
			# elif part_status == 'NG':
			# 	pass
			rch.set_json({RedisKeyBuilderServer(wid).get_key(0,process_completed) : False})
	
	except Exception as e:
		print(e)
		pass
