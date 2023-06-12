from fakedata import FakeData
from PIL import Image, ImageDraw, ImageFont
from draw_table_field import LayoutManager, Draw_Table
from draw_recipient_field import DrawRecipientField
from draw_supplier_field import DrawSupplierField, DrawDateField
from draw_graphicals import DrawBarcodeField, DrawLogoField
import json

class InvoiceGenerator():
    def __init__(self, canvas, output_dir, num_documents = 1, det = True) -> None:
        self.canvas = canvas
        self.output_dir = output_dir
        self.drawer = ImageDraw.Draw(self.canvas)
        self.font = ImageFont.truetype("arial.ttf", 30)
        self.num_documents = num_documents
        self.det = det     

    def __call__(self):
        # 1. Generate the layout
        layout_manager = LayoutManager()
        self.layout = layout_manager.get_layout()
        # layout_manager.visualize_layout(self.layout, self.drawer, self.font, self.canvas)

        # 2. Generate the fake data
        fake_data_generator = FakeData()
        fake_data = fake_data_generator(self.num_documents, self.det)

        # 3. Initialize the drawers
        table_drawer = Draw_Table()
        recipient_drawer = DrawRecipientField()
        supplier_drawer = DrawSupplierField()
        barcode_drawer = DrawBarcodeField()
        logo_drawer = DrawLogoField()
        date_drawer = DrawDateField()

        # 4. Draw the fake data on the image
        for i, document in enumerate(fake_data):
            labels = []
            # 4.1 Draw the table on the document
            labels = table_drawer(labels, self.canvas, self.layout['T_field'], document['I_Currency'])
            # 4.2 Draw the recipient field
            labels = recipient_drawer(labels, self.drawer, self.font, self.layout['R_field'], fake_data[i])
            # 4.3 Draw supplier field
            labels = supplier_drawer(labels, self.drawer, self.font, self.layout['S_field'], fake_data[i])
            # 4.4 Draw barcode field
            barcode_drawer(self.canvas, self.layout['Q_field'])
            # 4.5 Draw logo field
            logo_drawer(self.canvas, self.layout['L_field'])
            # 4.6 Draw information field
            labels = date_drawer(labels, self.drawer, self.font, self.layout['D_field'], fake_data[i])

            # 5. Save the labels
            with open(self.output_dir+'/Annotations/'+str(i)+'.json', 'w') as fp:
                json.dump(labels, fp)
            # 6. Save the image
            self.canvas.save(self.output_dir+'/Images/'+str(i)+'.tif')