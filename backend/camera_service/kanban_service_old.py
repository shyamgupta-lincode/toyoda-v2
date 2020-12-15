import pyzbar.pyzbar as pyzbar
from common_utils import *
from setting_keys import *
# from LIVIS.livis.toyoda.utils import *
# from LIVIS.livis.parts.utils import *

rch = CacheHelper()


def kanban_reading():
    data = RedisKeyBuilderWorkstation().workstation_info
    start_process_object = {}
    print("---data: ",data)
    kanban_placed = False
    c = 0

    for cam in data['camera_config']['cameras']:
        camera_name = cam['camera_name']
        if camera_name == "kanban_camera":
            camera_index = cam['camera_id']

    while True:
        key = RedisKeyBuilderWorkstation().get_key(camera_index,original_frame_keyholder)
        frame = rch.get_json(key)

        decodedObjects = pyzbar.decode(frame)
        if bool(decodedObjects):
            if not kanban_placed:
                try:
                    for obj in decodedObjects:
                        part_number = str(obj.data[:-5].decode('utf-8'))
                        part_number = part_number.replace("-","")
                        short_number = str(obj.data[-4:].decode("utf-8"))
                        # print("kanban_data>>>", short_number)
                        # print("part_number>>>", part_number)
                        rch.set_json({RedisKeyBuilderWorkstation().get_key(camera_index,short_number_keyholder):short_number})
                        rch.set_json({RedisKeyBuilderWorkstation().get_key(camera_index,part_number_keyholder):part_number})


                        print(rch.get_json(RedisKeyBuilderWorkstation().get_key(camera_index,short_number_keyholder)))
                        print(rch.get_json(RedisKeyBuilderWorkstation().get_key(camera_index,part_number_keyholder)))
                        kanban_placed = True

                except Exception as e:
                    # print(e)
                    pass
            c+=1
                    ###write to reddis
        else:
            try:
                rch.set_json({RedisKeyBuilderWorkstation().get_key(cam['camera_id'],short_number_keyholder):None})
                print("QR removed")
                kanban_placed = False

            except Exception as e:
                # print(e)
                pass    

            #starting the process when the Kanban is placed
            
            # if kanban_placed and c == 1:
            #     #start_process_util
            #     data1 = get_partInfo(short_number)
            #     user_id = "4783987hhr83hff"
            #     workstation_id = data['_id']
            #     start_process_object = start_toyoda_process()
            #     print("<<<<< ......Process STARTED...... >>>>>")     

            # #Ending the process when the Kanban is Removed
            # elif not kanban_placed:
            #     #end_process_util
            #     process_id = start_process_object["_id"]
            #     process_id_collection = {"process_id":process_id}
            #     end_toyoda_process(process_id_collection)
            #     print("<<<<< ......Process ENDED...... >>>>>")
            
            # else:
            #     pass

                  


kanban_reading()
