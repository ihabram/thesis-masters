from annotator import text_label

class DrawRecipientField():
    def __init__(self) -> None:
        pass

    def __call__(self, labels, draw, font, bbox, data):
        self.labels = labels
        self.draw = draw
        self.font = font
        self.bbox = bbox
        self.data = data
        self.entities = self.select_entities()

        letter_bbox = self.draw.textbbox((0, 0), 'A', font=self.font)
        self.increment = (letter_bbox[3] - letter_bbox[1])+20    # The distance between the rows

        # Draw the data on the invoice
        self.draw_content()

        return self.labels

    def select_entities(self):
        # TODO: Make this function random
        entities = ['R_Name', 'R_Street', 'R_HouseNumber', 'R_ZIP', 'R_City', 'R_Country', 'R_VAT']
        return entities
    
    def draw_content(self):
        x1, y1, x2, y2 = self.bbox
        
        for entity in self.entities:
            # Street - house number, ZIP - City are always show up next to each other
            if entity == 'R_Street':
                self.labels.append(text_label(self.draw, (x1, y1), self.data[entity], self.font, 'lm', entity))
                bbox = self.draw.textbbox((0, 0), self.data[entity], font=self.font)
                width = bbox[2] - bbox[0]
                self.labels.append(text_label(self.draw, (x1 + width + 30, y1), self.data['R_HouseNumber'], self.font, 'lm', 'R_HouseNumber'))
            if entity == 'R_ZIP':
                self.labels.append(text_label(self.draw, (x1, y1), self.data[entity], self.font, 'lm', entity))
                bbox = self.draw.textbbox((0, 0), self.data[entity], font=self.font)
                width = bbox[2] - bbox[0]
                self.labels.append(text_label(self.draw, (x1 + width + 30, y1), self.data['R_City'], self.font, 'lm', 'R_City'))
            if entity in ['R_HouseNumber', 'R_City']:
                continue
            if entity == 'R_VAT':
                y1 += 1.5*self.increment
                self.labels.append(text_label(self.draw, (x1, y1), 'Tax ID: \t', self.font, 'lm', 'Other'))
                bbox = self.draw.textbbox((0, 0), 'Tax ID: \t', font=self.font)
                width = bbox[2] - bbox[0]
                self.labels.append(text_label(self.draw, (x1+width, y1), self.data[entity], self.font, 'lm', entity))

            else:
                self.labels.append(text_label(self.draw, (x1, y1), self.data[entity], self.font, 'lm', entity))
                y1 += self.increment