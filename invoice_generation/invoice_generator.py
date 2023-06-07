from fakedata import FakeData
from PIL import Image, ImageDraw, ImageFont
from draw_table_field import LayoutManager, Draw_Table
from draw_recipient_field import DrawRecipientField
import json

class InvoiceGenerator():
    def __init__(self, canvas, output_dir, num_documents = 1, det = True) -> None:
        self.canvas = canvas
        self.output_dir = output_dir
        self.drawer = ImageDraw.Draw(self.canvas)
        self.font = ImageFont.truetype("arial.ttf", 30)
        self.num_documents = num_documents
        self.det = det
        self.labels = []     

    def __call__(self):
        # 1. Generate the layout
        layout_manager = LayoutManager()
        self.layout = layout_manager.get_layout()
        # layout_manager.visualize_layout(self.layout, self.drawer, self.font, self.canvas)

        # 2. Generate the fake data
        fake_data_generator = FakeData()
        fake_data = fake_data_generator(self.num_documents, self.det)

        # 3. Draw the fake data on the image
        table_drawer = Draw_Table()
        recipient_drawer = DrawRecipientField()
        for i, document in enumerate(fake_data):
            # Draw the table on the document
            self.labels = table_drawer(self.labels, self.canvas, self.layout['T_field'], document['I_Currency'])
            # Draw the recipient field
            self.labels.append(recipient_drawer(self.labels, self.drawer, self.font, self.layout['R_field'], fake_data[i]))

            # Save the labels
            with open(self.output_dir+'/Annotations/'+str(i)+'.json', 'w') as fp:
                json.dump(self.labels, fp)
            # Save the image
            self.canvas.save(self.output_dir+'/Images/'+str(i)+'.tif')


# Open the blank, empty invoice image
blank_dir = r'blank.tif'
blank = Image.open(blank_dir)

# Define the output directory
output_dir = r'C:\Users\Habram\Documents\Datasets\fake-invoices'

# Initialize and call the invoice generator
invoice_generator = InvoiceGenerator(blank, output_dir, 1, False)
invoice_generator()