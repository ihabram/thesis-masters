from PIL import Image, ImageDraw
import random

class DrawBarcodeField():
    def __init__(self):
        pass

    def __call__(self, invoice, bbox):
        # Get a random barcode
        barcode_dir = r'C:\Users\Habram\Documents\Datasets\Barcodes/'
        barcode_name = str(random.randint(0, 49))
        barcode = Image.open(barcode_dir + barcode_name + '.png')

        # Width of the bounding box
        width_bbox = bbox[2] - bbox[0]

        # Width of the barcode
        width_barcode, height_barcode = barcode.size

        # Calculate the resizing ratio, if the barcode is bigger than the bounding box
        if width_barcode > width_bbox:
            ratio = width_bbox / width_barcode

            new_width = int(width_barcode*ratio)
            new_height= int(height_barcode*ratio)

            barcode = barcode.resize((new_width, new_height))


        # Print the barcode on the invoice
        invoice.paste(barcode, (bbox[0], bbox[1]))