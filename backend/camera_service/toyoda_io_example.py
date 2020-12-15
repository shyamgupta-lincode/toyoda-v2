from toyoda_io import *
import time
import datetime


t=toyoda_io("1A86:7523","5")
print(t.read(9))

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

#simple example
started = 0

while 1:

	#redis accepted / rejected - #TO DO
	# part_status = 

	if started == 1 and ((datetime.datetime.now()-start) >= datetime.timedelta(seconds=5)):
		started=0
		#set redis keyholder to start the process
		rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder)}) 
		t.write(8,0)

	time.sleep(0.2)
	if t.read(9) == 1:
		#-------------------do the process--------------------


		#
		if part_status == 'Good':
			start=datetime.datetime.now()
			started=1
			t.write(8,1)
		elif part_status == 'NG':
			pass
