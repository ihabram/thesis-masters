from annotator import text_label

class DrawSupplierField():
    def __init__(self) -> None:
        pass

    def __call__(self, labels, draw, font, bbox, data):
        self.labels = labels    # Big container which includes every word-label-bbox information of the document
        self.draw = draw        # PIL draw object
        self.font = font        # PIL font style
        self.bbox = bbox        # Bounding box of the field
        self.data = data        # Data to print
        self.entities = self.select_entities()      # Select entities to print

        letter_bbox = self.draw.textbbox((0, 0), 'A', font=self.font)   # Get the height of a random capital letter
        self.increment = (letter_bbox[3] - letter_bbox[1])+20    # The distance between the rows

        # Draw the data on the invoice
        self.draw_content()

    def select_entities(self):
        # TODO: Make this function random
        entities = ['S_Name', 'S_Street', 'S_HouseNumber', 'S_ZIP', 'S_City', 'S_Country', 
                    'S_VAT', 'S_Bank', 'S_BIC', 'S_IBAN', 'S_Tel', 'S_Email']
        return entities
    
    def draw_content(self):
        x1, y1, x2, y2 = self.bbox
        
        for entity in self.entities:
            # Street - house number, ZIP - City are always show up next to each other
            if entity == 'S_Street':
                self.labels.append(text_label(self.draw, (x1, y1), self.data[entity], self.font, 'lm', entity))
                bbox = self.draw.textbbox((0, 0), self.data[entity], font=self.font)
                width = bbox[2] - bbox[0]
                self.labels.append(text_label(self.draw, (x1 + width + 30, y1), self.data['R_HouseNumber'], self.font, 'lm', 'R_HouseNumber'))
            if entity == 'S_ZIP':
                self.labels.append(text_label(self.draw, (x1, y1), self.data[entity], self.font, 'lm', entity))
                bbox = self.draw.textbbox((0, 0), self.data[entity], font=self.font)
                width = bbox[2] - bbox[0]
                self.labels.append(text_label(self.draw, (x1 + width + 30, y1), self.data['R_City'], self.font, 'lm', 'R_City'))
            if entity in ['S_HouseNumber', 'S_City']:
                continue
            else:
                self.labels.append(text_label(self.draw, (x1, y1), self.data[entity], self.font, 'lm', entity))
                y1 += self.increment