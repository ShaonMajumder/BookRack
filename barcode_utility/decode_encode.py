#https://note.nkmk.me/en/python-pillow-qrcode/
#from barcode import EAN8,Code128,Code39
# encode,decode,display,actual_data,make_barcode_matrix
try:
    reduce
except NameError:
    from functools import reduce
#from io import BytesIO
from barcode.writer import ImageWriter
from barcode import __BARCODE_MAP
from pyzbar import pyzbar
from PIL import Image


import numpy as np
import shaonutil
import barcode
import qrcode
import sys
import cv2
import PIL
import os

def calculate_checksum(data):
    """Calculates the checksum for EAN13-Code / EAN8-Code
    return type: Integer
    """
    def sum_(x, y):
        return int(x) + int(y)

    evensum = reduce(sum_, data[-2::-2])
    oddsum = reduce(sum_, data[-1::-2])
    return (10 - ((evensum + oddsum * 3) % 10)) % 10

def verify_data(data):
	verification_digit = int(data[-1])
	check_digit = data[:-1]
	return verification_digit == calculate_checksum(check_digit)

def actual_data(decodedObjects):
	if len(decodedObjects) > 0:
		obj = decodedObjects[0]
		data = obj.data.decode('ascii')
	else:
		return False

	if 'ean' in obj.type.lower():
		if verify_data(data):
			return data[:-1]
		else:
			return False
	else:
		return data


def encode(type_,file_,data,rt='FILE'):
	# rt = 'OBJ'
	__BARCODE_MAP['qrcode'] = ''
	if not type_.lower() in __BARCODE_MAP:
		raise ValueError("BarCode Type invalid")
	"""
	if type_ == 'EAN8':
		
		# print to a file-like object:
		#rv = BytesIO()
		#EAN8(str(1708929), writer=ImageWriter()).write(rv)
		
		# or sure, to an actual file:
		with open(file_, 'wb') as f:
		    EAN8(data, writer=ImageWriter()).write(f)
	elif type_ == 'Code128':
		with open(file_, 'wb') as f:
		    Code128(data, writer=ImageWriter()).write(f)
	elif type_ == 'Code39':
		with open(file_, 'wb') as f:
		    Code39(data, writer=ImageWriter()).write(f)
	elif type_ == 'qrcode':

		qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=10,
		    border=4,
		)
		qr.add_data(data)
		qr.make(fit=True)

		img = qr.make_image(fill_color="black", back_color="white")
		img.save(file_)
	"""

	if type_ == 'qrcode':

		qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=10,
		    border=4,
		)
		qr.add_data(data)
		qr.make(fit=True)

		img = qr.make_image(fill_color="black", back_color="white")
		if  rt == 'OBJ':
			return img
		else:
			img.save(file_)
			return file_
	else:
		#ean = barcode.get('ean13', '123456789102', writer = barcode.writer.ImageWriter())
		#print(type(ean))
		
		bar_class = barcode.get_barcode_class(type_)
		#bar_class.default_writer_options['write_text'] = False
		bar_class.default_writer_options['text_distance'] = .5
		bar_class.default_writer_options['quiet_zone'] = 1.8
		bar_class.default_writer_options['module_height'] = int(15/1.1)
		
		writer=ImageWriter()
		bar = bar_class(data, writer)
		#print(type(bar))
		to_be_resized = bar.render()
		#bar.save('temp')
		#to_be_resized = Image.open('temp.png')
		del bar

		width,height = to_be_resized.size
		width = int(width/1.2)
		newSize = (width, height)
		resized = to_be_resized.resize(newSize, resample=PIL.Image.NEAREST)
		
		
		if  rt == 'OBJ':
			if os.path.exists(file_): os.remove(file_)
			return resized
		else:
			resized.save(file_)
			return file_

		



	
def decode(infile,log=False):
	if type(infile) == str:
		im = cv2.imread(infile)
	elif type(infile) == np.ndarray:
		im = infile

	data = False
	# Find barcodes and QR codes
	decodedObjects = pyzbar.decode(im)

	# Print results
	for obj in decodedObjects:
		if log: print('Type : ', obj.type)
		if log: print('Data : ', obj.data,'\n')
    
	return decodedObjects


def display(im, decodedObjects):

    # Loop over all decoded objects
    for decodedObject in decodedObjects: 
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else : 
            hull = points;

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0,n):
            cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

    return im

def make_barcode_matrix(type_,unique_ids,row_number,column_number,filename):
    if not len(unique_ids) == row_number * column_number:
        raise ValueError("number of ids not equal to row x column size")
    
    TwoDArray = np.array(unique_ids).reshape(row_number,column_number)
    column_img = []
    for row_ids in TwoDArray:
        row_img  = [encode(type_,'',row_ids[i],rt='OBJ') for i in range(column_number)] 
        row_concatenated_img = shaonutil.image.merge_horizontally(row_img)
        column_img.append(row_concatenated_img)

    shaonutil.image.merge_vertically(column_img,filename)