from annotator_de import text_label
import random

class DrawRecipientField():
    def __init__(self) -> None:
        pass

    def __call__(self, labels, draw, font, bbox, data):
        self.labels = labels
        self.draw = draw
        self.font = font
        self.bbox = bbox
        self.data = data

        letter_bbox = self.draw.textbbox((0, 0), 'A', font=self.font)
        self.increment = (letter_bbox[3] - letter_bbox[1])+20    # The distance between the rows

        # Draw the data on the invoice
        self.draw_content()
        self.draw_supplierA_field()

        return self.labels
    
    def get_textwidth(self, text):
        '''
        Returns the width in pixels of a given text.
        Useful when a specific text is inserted in front of an entity and the entity should be shifted
        '''
        bbox = self.draw.textbbox((0, 0), text, font=self.font)
        width = bbox[2] - bbox[0]
        return width
    
    def draw_content(self):
        entities = ['R_Name', 'R_Street', 'R_ZIP', 'R_Country', 'R_VAT']
        x, y, x2, y2 = self.bbox
        
        for entity in entities:
            if entity == 'R_Name':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
                y += self.increment
            # Street - house number, ZIP - City are always show up next to each other
            elif entity == 'R_Street':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
                width = self.get_textwidth(self.data[entity])
                self.labels.append(text_label(self.draw, (x + width + 30, y), self.data['R_HouseNumber'], self.font, 'lm', 'R_HouseNumber'))
                y += self.increment
            elif entity == 'R_ZIP':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
                width = self.get_textwidth(self.data[entity])
                self.labels.append(text_label(self.draw, (x + width + 30, y), self.data['R_City'], self.font, 'lm', 'R_City'))
                y += self.increment
            elif entity == 'R_Country':
                country = {
                    'Germany': 'Deutschland',
                    'Austria': 'Österreich',
                    'Switzerland': 'Schweiz'
                }
                self.labels.append(text_label(self.draw, (x, y), country[self.data[entity]], self.font, 'lm', entity))
                y += self.increment
            elif entity == 'R_VAT':
                y += 1.5*self.increment
                self.labels.append(text_label(self.draw, (x, y), 'USt.-ID Nr.:', self.font, 'lm', 'Other'))
                width = self.get_textwidth('USt.-ID Nr.: \t')
                self.labels.append(text_label(self.draw, (x+width, y), self.data[entity], self.font, 'lm', 'Other'))

    def draw_supplierA_field(self):
        ''' Draws the supplier field on top of the recipient field'''
        entities = ['S_Name', 'S_Street', 'S_HouseNumber', 'S_ZIP', 'S_City']
        x, y, x2, y2 = self.bbox
        y -= 80

        for entity in entities:
            if entity == 'S_Name':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
                x += self.get_textwidth(self.data[entity] + ' ')
                self.labels.append(text_label(self.draw, (x, y), ' | ', self.font, 'lm', 'Other'))
                x += self.get_textwidth(' | ')
            elif entity == 'S_Street':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity] + '  ', self.font, 'lm', entity))
                x += self.get_textwidth(self.data[entity] + '  ')
            elif entity == 'S_HouseNumber':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
                x += self.get_textwidth(self.data[entity] + ' ')
                self.labels.append(text_label(self.draw, (x, y), ' | ', self.font, 'lm', 'Other'))
                x += self.get_textwidth(' | ')
            elif entity == 'S_ZIP':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity] + '  ', self.font, 'lm', entity))
                x += self.get_textwidth(self.data[entity] + '  ')
            elif entity == 'S_City':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))