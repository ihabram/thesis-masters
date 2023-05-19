from PIL import Image, ImageDraw

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