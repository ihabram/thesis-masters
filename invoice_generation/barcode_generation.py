import barcode
import random
from barcode.writer import ImageWriter

ITF = barcode.get_barcode_class('itf')
folder = r'C:\Users\Habram\Documents\Datasets\Barcodes/'

for i in range(50):
    number = random.randint(30573142, 305731423442345632432)
    itf = ITF(str(number), writer=ImageWriter())
    fullname = itf.save(folder + str(i), options={"write_text": False})