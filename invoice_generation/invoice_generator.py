from fakedata import FakeData
from PIL import Image, ImageDraw, ImageFont
from draw_table_field import LayoutManager, Draw_Table
from draw_recipient_field import DrawRecipientField
from draw_supplier_field import DrawSupplierField, DrawDateField
from draw_graphicals import DrawBarcodeField, DrawLogoField
from draw_information_field import DrawInformationField, DrawTextField
import json

class InvoiceGenerator():
    def __init__(self, num_documents = 1, det = True) -> None:
        self.output_dir = r'C:\Users\Habram\Documents\Datasets\fake-invoices'
        self.font = ImageFont.truetype("arial.ttf", 30)
        self.num_documents = num_documents
        self.det = det

    def get_canvas(self):
        # Open the blank, empty invoice image
        blank_dir = r'blank.tif'
        blank = Image.open(blank_dir)

        return blank

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
        info_drawer = DrawInformationField()
        text_drawer = DrawTextField()

        # 4. Draw the fake data on the image
        for i, document in enumerate(fake_data):
            labels = []
            canvas = self.get_canvas()
            drawer = ImageDraw.Draw(canvas)

            # 4.1 Draw the table on the document
            labels = table_drawer(labels, canvas, self.layout['T_field'], document['I_Currency'])
            # 4.2 Draw the recipient field
            labels = recipient_drawer(labels, drawer, self.font, self.layout['R_field'], fake_data[i])
            # 4.3 Draw supplier field
            labels = supplier_drawer(labels, drawer, self.font, self.layout['S_field'], fake_data[i])
            # 4.4 Draw barcode field
            barcode_drawer(canvas, self.layout['Q_field'])
            # 4.5 Draw logo field
            logo_drawer(canvas, self.layout['L_field'])
            # 4.6 Draw date field
            labels = date_drawer(labels, drawer, self.font, self.layout['D_field'], fake_data[i])
            # 4.7 Draw information field
            labels = info_drawer(labels, drawer, self.font, self.layout['I_field'], fake_data[i])
            # 4.8 Draw text field
            labels = text_drawer(labels, drawer, self.font, self.layout['X_field'], fake_data[i])

            # 5. Save the labels
            with open(self.output_dir+'/Annotations/'+str(i)+'.json', 'w') as fp:
                json.dump(labels, fp)
            # 6. Save the image
            canvas.save(self.output_dir+'/Images/'+str(i)+'.tif')