import pyqrcode 
import png 
from pyqrcode import QRCode 
from datetime import datetime
import base64


def qrcode_generator(short_number, part_counter):

    # String which represents the QR code 
    print("type(part_counter)::::::",type(part_counter))
    print("part_counter:::::", part_counter)
    d_date = datetime.now()
    reg_format_date = d_date.strftime("%d-%m-%Y%I:%M%p")
    if len(str(part_counter+1)) == 1:
        # Generate QR code 
        url = pyqrcode.create(str(short_number)+"-"+str(reg_format_date)+"00"+str(part_counter+1))
    elif len(str(part_counter+1)) == 2:
        # Generate QR code 
        url = pyqrcode.create(str(short_number)+"-"+str(reg_format_date)+"0"+str(part_counter+1)) 
    else:
        # Generate QR code 
        url = pyqrcode.create(str(short_number)+"-"+str(reg_format_date)+str(part_counter+1)) 
    
    #print("generating_qr",url)
    my_string = url.png_as_base64_str(scale=1, module_color=(0, 0, 0, 255), background=(255, 255, 255, 255), quiet_zone=4)
   
    return my_string


#if __name__ == '__main__':
    #qrcode_generator("IG90",221)

