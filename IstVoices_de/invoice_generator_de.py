from fakedata_de import FakeData
from PIL import Image, ImageDraw, ImageFont
from draw_table_field_de import LayoutManager, Draw_Table
from draw_recipient_field_de import DrawRecipientField
from draw_supplier_field_de import DrawSupplierField, DrawDateField
from draw_graphicals_de import DrawBarcodeField, DrawLogoField
from draw_information_field_de import DrawInformationField
import json
import random

class InvoiceGenerator():
    def __init__(self, num_documents = 1) -> None:
        self.output_dir = r'C:\Users\Habram\Documents\Datasets\fake-invoices_de'
        self.num_documents = num_documents

        # Initialize the drawers + layout manager
        self.layout_manager      = LayoutManager()
        self.table_drawer        = Draw_Table()
        self.recipient_drawer    = DrawRecipientField()
        self.supplier_drawer     = DrawSupplierField()
        self.barcode_drawer      = DrawBarcodeField()
        self.logo_drawer         = DrawLogoField()
        self.date_drawer         = DrawDateField()
        self.info_drawer         = DrawInformationField()

        # Which drawer has to be called for which field
        self.layout2drawer = {
            'R_field': self.recipient_drawer,
            'S_field': self.supplier_drawer,
            'D_field': self.date_drawer,
            'L_field': self.logo_drawer,
            'T_field': self.table_drawer,
            'I_field': self.info_drawer,
            'Q_field': self.barcode_drawer
        }

    def get_canvas(self):
        # Open the blank, empty invoice image
        blank_dir = r'blank.tif'
        blank = Image.open(blank_dir)

        return blank
    
    def get_font(self):
        styles = ['arial.ttf', 'times.ttf', 'calibri.ttf', 'verdana.ttf']
        style = random.choice(styles)

        return ImageFont.truetype(style, random.randint(20, 30))

    def __call__(self):
        # Generate the fake data
        fake_data_generator = FakeData()
        fake_data = fake_data_generator(self.num_documents)

        # Draw the fake data on the image
        for i, document in enumerate(fake_data):
            # Start with an empty label list
            labels = []
            # Get an empty canvas
            canvas = self.get_canvas()
            drawer = ImageDraw.Draw(canvas)
            font = self.get_font()

            # Generate a layout
            layout = self.layout_manager.get_layout()
            # layout_manager.visualize_layout(self.layout, self.drawer, self.font, self.canvas)

            for layout_field in layout:
                if layout_field == 'L_field':
                    self.layout2drawer[layout_field](canvas, layout[layout_field])
                elif layout_field == 'Q_field':
                    self.layout2drawer[layout_field](canvas, layout[layout_field])
                else:
                    labels = self.layout2drawer[layout_field](labels, drawer, font, layout[layout_field], fake_data[i])

            # Save the labels
            with open(self.output_dir+ r'/Annotations/' + str(i) + '.json', 'w') as fp:
                json.dump(labels, fp)
            # Save the image
            canvas.save(self.output_dir+ r'/Images/' +str(i) +'.tif')