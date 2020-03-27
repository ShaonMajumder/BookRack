from shaonutil.strings import generateCryptographicallySecureRandomString
from decode_encode import make_barcode_matrix,encode,decode,actual_data

unique_ids = [generateCryptographicallySecureRandomString(stringLength=7,filters=['number']) for i in range(15)]
#make_barcode_matrix('ean8',unique_ids, 5,3,'matrix.jpg')
data = f"""godisgreat3242898432233"""

encode('qrcode','qrStatus.jpg',data)
print(actual_data(decode('qrStatus.jpg')))