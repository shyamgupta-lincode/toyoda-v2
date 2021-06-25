import win32print
import win32ui
from PIL import Image, ImageWin
import base64

def print_qrImage():    
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    
    printer_name = win32print.GetDefaultPrinter ()
    file_name = "generated_qr.png"
    
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    
    bmp = Image.open (file_name)
    
    hDC.StartDoc (file_name)
    hDC.StartPage ()
    
    bmp = bmp.convert('RGB')
    dib = ImageWin.Dib (bmp)
    
    dib.draw (hDC.GetHandleOutput (), (0,240,int((printer_size[0])/1.5),int((printer_size[1])/1.5)))
    
    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()
    
def decode_base64_into_image(base64_string):
    img = base64.decodestring(base64_string)
    image_result = open('generated_qr.png', 'wb') # create a writable image and write the decoding result
    image_result.write(img)
    
    
    
print_qrImage()    
