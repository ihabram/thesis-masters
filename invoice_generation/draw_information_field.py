from PIL import ImageFont
from annotator import text_label
from faker import Faker
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
    
    def get_num_cols(self):
        '''
        If the bounding box is not wide enough, the number of columns should be limited
        '''
        width_bbox = self.bbox[2] - self.bbox[0]
        width_col = self.get_textwidth('IBAN: DE68108345214389224539')

        max_num = int(width_bbox / width_col)
        if max_num > 4: max_num = 4

        return random.randint(1, max_num)
    
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
        num_fields = self.get_num_cols()
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


class DrawTextField():
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
        fake = Faker(random.randint(0, 5000))
        text = fake.paragraph(10, True)

        text_labels = {
            'text': text,
            'label': 'Other',
            'box': None,
            'words': []
        }

        x1, y1, x2, y2 = self.bbox

        y = y1
        x = x1
        text_x2 = 0 # x2 position of the whole text
        text_y2 = 0 # y2 position of the whole text

        for word in text.split():
            if y > y2: break    # If the text is over the bottom boundary, stop printing

            # Check the position of the next word
            word_bbox = self.draw.textbbox([x, y], word, font=self.font)

            # If the word would be out of the bounding box, jump to the next line
            if word_bbox[2] > x2:
                y += self.increment
                x = x1
            
            # Draw the word
            self.draw.text([x, y], word, fill='black', font=self.font)

            # Add the word to the label
            word_bbox = self.draw.textbbox([x, y], word, font=self.font)
            word_width = word_bbox[2] - word_bbox[0]
            text_labels['words'].append(
                {
                'box':  word_bbox,
                'text': word
                }
            )

            # Get the width of a 'Space' caracter
            space_bbox = self.draw.textbbox([0,0], ' ', font=self.font)
            space_width = space_bbox[2] - space_bbox[0]

            # 'Slide the x position with the word width and a 'Space
            x += word_width + space_width

            # Update the whole text bounding box
            if word_bbox[2] > text_x2: text_x2 = word_bbox[2]
            if word_bbox[3] > text_y2: text_y2 = word_bbox[3]

        text_labels['box'] = [x1, y1, text_x2, text_y2]

        self.labels.append(text_labels)