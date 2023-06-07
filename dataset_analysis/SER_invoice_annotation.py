from PIL import Image, ImageDraw, ImageFont

class CleanInvoice():
    def __init__(self, image_loc, output_loc) -> None:
        self.image = Image.open(image_loc)
        self.draw = ImageDraw.Draw(self.image)
        self.output_loc = output_loc

    def clear_entity(self, coords):
        top_x = coords[0][0]
        top_y = coords[0][1]
        bot_x = coords[1][0]
        bot_y = coords[1][1]
        self.draw.rectangle([(top_x, top_y), (bot_x, bot_y)], fill='white')

    def clean_invoice(self, labels):
        for l in labels:
            for coord in labels[l]:
                self.clear_entity(coord)
        self.image.save(self.output_loc)


class FillInvoice():
    def __init__(self, empty_image_loc, output_loc) -> None:
        self.empty_image = empty_image_loc
        self.output_loc = output_loc

    def get_font_size(self, bounding_box):
        # TODO: More sophisticated function which is universal for every invoice
        height = bounding_box[1][1] - bounding_box[0][1]
        if height > 25:
            return 23
        else:
            return 18
    
    def fill_invoice(self, labels, fake_data, show, save, type):
        for i, document in enumerate(fake_data):
            invoice = Image.open(self.empty_image)
            draw = ImageDraw.Draw(invoice)
            # Iterate through the entities in a document
            for entity in document:
                # If the same label is presented on the document, iterate through the positions
                for entity_instance in labels[entity]:
                    
                    font_size = self.get_font_size(entity_instance)
                    font = ImageFont.truetype("arial.ttf", font_size)
                    draw.text(tuple(entity_instance[0]), document[entity], fill='black', font=font)

            if show == True:
                invoice.show()
            if save == True:
                invoice.save(self.output_loc + type + '_' + str(i) + '.tif')