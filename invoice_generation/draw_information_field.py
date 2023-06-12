from PIL import ImageFont
from annotator import text_label
import random

class DrawInformationField():
    def __init__(self) -> None:
        pass

    def __call__(self, labels, draw, font, bbox, data):
        self.labels = labels
        self.draw = draw
        self.font = self.font = ImageFont.truetype("arial.ttf", 20)
        self.bbox = bbox
        self.data = data

        letter_bbox = self.draw.textbbox((0, 0), 'A', font=self.font)
        self.increment = (letter_bbox[3] - letter_bbox[1])+20    # The distance between the rows

        # Draw the data on the invoice
        self.draw_content()

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
        '''
        Information field has 4 sub-fields: 
        - Supplier address: Name, street + house number, zip + country
        - Supplier contact: tel, fax, email
        - Supplier bank details: bank name, iban, bic
        - Supplier personal contact: contact person name, tax id
        '''
        # Select random sub-fields
        fields = ['Address_field', 'Contact_field', 'Bank_field', 'Personal_field']
        num_fields = random.randint(1, 4)
        fields = random.sample(fields, num_fields)

        x1, y1, x2, y2 = self.bbox
        width_bbox = x2 - x1
        hor_increment = int(width_bbox / num_fields)

        x_positions = [x1]
        for i in range(num_fields - 1):
            x_positions.append(x_positions[i] + hor_increment)

        for i, field in enumerate(fields):
            x = x_positions[i]
            y = y1
            if field == 'Address_field':
                self.labels.append(text_label(self.draw, (x, y), self.data['S_Name'], self.font, 'lm', 'S_Name'))
                y += self.increment
                self.labels.append(text_label(self.draw, (x, y), self.data['S_Street'], self.font, 'lm', 'S_Street'))
                width = self.get_textwidth(self.data['S_Street'] + ' ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['S_HouseNumber'], self.font, 'lm', 'S_HouseNumber'))
                y += self.increment
                self.labels.append(text_label(self.draw, (x, y), self.data['S_ZIP'], self.font, 'lm', 'S_ZIP'))
                width = self.get_textwidth(self.data['S_ZIP'] + ' ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['S_City'], self.font, 'lm', 'S_City'))

            elif field == 'Contact_field':
                self.labels.append(text_label(self.draw, (x, y), 'Telefon:', self.font, 'lm', 'Other'))
                width = self.get_textwidth('Telefon: ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['S_Tel'], self.font, 'lm', 'S_Tel'))
                y += self.increment
                self.labels.append(text_label(self.draw, (x, y), 'Fax:', self.font, 'lm', 'Other'))
                width = self.get_textwidth('Fax: ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['Fax'], self.font, 'lm', 'Other'))
                y += self.increment
                self.labels.append(text_label(self.draw, (x, y), 'Website:', self.font, 'lm', 'Other'))
                width = self.get_textwidth('Website: ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['Website'], self.font, 'lm', 'Other'))

            elif field == 'Bank_field':
                self.labels.append(text_label(self.draw, (x, y), self.data['S_Bank'], self.font, 'lm', 'S_Bank'))
                y += self.increment
                self.labels.append(text_label(self.draw, (x, y), 'IBAN:', self.font, 'lm', 'Other'))
                width = self.get_textwidth('IBAN: ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['S_IBAN'], self.font, 'lm', 'S_IBAN'))
                y += self.increment
                self.labels.append(text_label(self.draw, (x, y), 'BIC:', self.font, 'lm', 'Other'))
                width = self.get_textwidth('BIC: ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['S_BIC'], self.font, 'lm', 'S_BIC'))

            elif field == 'Personal_field':
                self.labels.append(text_label(self.draw, (x, y), 'Contact:', self.font, 'lm', 'Other'))
                width = self.get_textwidth('Contact: ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['Contact_Name'], self.font, 'lm', 'Other'))
                y += self.increment
                self.labels.append(text_label(self.draw, (x, y), 'Tax ID:', self.font, 'lm', 'Other'))
                width = self.get_textwidth('Tax ID: ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data['S_VAT'], self.font, 'lm', 'S_VAT'))