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

        letter_bbox = self.draw.textbbox((0, 0), 'A', font=self.font)   # Get the height of a random capital letter
        self.increment = (letter_bbox[3] - letter_bbox[1])+20    # The distance between the rows

        # Draw the data on the invoice
        self.draw_content()
    
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
        The supplier field has two subfields: company field, bank field.
        This function manages to print them
        '''
        x, y, x2, y2 = self.bbox
        
        # TODO: Make the order random
        y = self.draw_company_field(x, y)
        y += self.increment
        self.draw_bank_field(x, y)


    def draw_company_field(self, x, y):
        entities = ['S_Name', 'S_Street', 'S_HouseNumber', 'S_ZIP', 'S_City', 'S_Country', 'S_VAT']
        
        for entity in entities:
            # Street - house number, ZIP - City are always show up next to each other
            if entity == 'S_Street':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
                width = self.get_textwidth(self.data[entity])
                self.labels.append(text_label(self.draw, (x + width + 30, y), self.data['R_HouseNumber'], self.font, 'lm', 'R_HouseNumber'))
            elif entity == 'S_ZIP':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
                width = self.get_textwidth(self.data[entity])
                self.labels.append(text_label(self.draw, (x + width + 30, y), self.data['R_City'], self.font, 'lm', 'R_City'))
            elif entity in ['S_HouseNumber', 'S_City']:
                continue
            elif entity == 'S_VAT':
                self.labels.append(text_label(self.draw, (x, y), 'Tax ID: \t', self.font, 'lm', 'Other'))
                width = self.get_textwidth('Tax ID: \t')
                self.labels.append(text_label(self.draw, (x+width, y), self.data[entity], self.font, 'lm', entity))

            else:
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
            y += self.increment

        return y
    
    def draw_bank_field(self, x, y):
        entities = ['S_Bank', 'S_BIC', 'S_IBAN']

        for entity in entities:
            if entity == 'S_Bank':
                self.labels.append(text_label(self.draw, (x, y), self.data[entity], self.font, 'lm', entity))
            elif entity == 'S_BIC':
                self.labels.append(text_label(self.draw, (x, y), 'Swift: \t', self.font, 'lm', 'Other'))
                width = self.get_textwidth('Swift: \t ')
                self.labels.append(text_label(self.draw, (x+width, y), self.data[entity], self.font, 'lm', entity))
            elif entity == 'S_IBAN':
                self.labels.append(text_label(self.draw, (x, y), 'IBAN: \t', self.font, 'lm', 'Other'))
                width = self.get_textwidth('IBAN: \t')
                self.labels.append(text_label(self.draw, (x+width, y), self.data[entity], self.font, 'lm', entity))
            y += self.increment

        return y
    

class DrawInformationField():
    def __init__(self) -> None:
        pass

    def __call__(self, labels, draw, font, bbox, data):
        self.labels = labels    # Big container which includes every word-label-bbox information of the document
        self.draw = draw        # PIL draw object
        self.font = font        # PIL font style
        self.bbox = bbox        # Bounding box of the field
        self.data = data        # Data to print

        letter_bbox = self.draw.textbbox((0, 0), 'A', font=self.font)   # Get the height of a random capital letter
        self.increment = (letter_bbox[3] - letter_bbox[1])+20    # The distance between the rows

        # Draw the data on the invoice
        self.draw_content()

    def draw_content(self):
        '''
        The information field has two subfields: date field, contact field.
        This function manages to print them
        '''
        x, y, x2, y2 = self.bbox
        
        # TODO: Make the order random
        y = self.draw_date_field(x, y)
        self.draw_contact_field(x, y)
    
    def get_textwidth(self, text):
        '''
        Returns the width in pixels of a given text.
        Useful when a specific text is inserted in front of an entity and the entity should be shifted
        '''
        bbox = self.draw.textbbox((0, 0), text, font=self.font)
        width = bbox[2] - bbox[0]
        return width

    def draw_date_field(self, x, y):
        entities = ['I_Number', 'Start_Date', 'I_Date', 'I_DueDate']
        width = self.get_textwidth('Invoice number: \t')
        
        for entity in entities:
            if entity == 'I_Number':
                self.labels.append(text_label(self.draw, (x, y), 'Invoice number:', self.font, 'lm', 'Other'))
                self.labels.append(text_label(self.draw, (x+width, y), self.data[entity], self.font, 'lm', entity))
            elif entity == 'Start_Date':
                self.labels.append(text_label(self.draw, (x, y), 'Period:', self.font, 'lm', 'Other'))
                self.labels.append(text_label(self.draw, (x+width, y), self.data[entity], self.font, 'lm', 'Other'))
                width_date = self.get_textwidth(self.data[entity] + '  ')
                self.labels.append(text_label(self.draw, (x+width+width_date, y), ' - ', self.font, 'lm', 'Other'))
                width_ = self.get_textwidth(' - ')
                self.labels.append(text_label(self.draw, (x+width+width_date+width_, y), self.data['End_Date'], self.font, 'lm', 'Other'))
            elif entity == 'I_Date':
                self.labels.append(text_label(self.draw, (x, y), 'Invoice date:', self.font, 'lm', 'Other'))
                self.labels.append(text_label(self.draw, (x+width, y), self.data[entity], self.font, 'lm', entity))
            y += self.increment

        return y

    def draw_contact_field(self, x, y):
        entities = ['S_Tel', 'S_Email']
        width = self.get_textwidth('Invoice number: \t')

        self.labels.append(text_label(self.draw, (x, y), 'Our reference:', self.font, 'lm', 'Other'))
        self.labels.append(text_label(self.draw, (x+width, y), self.data['S_Tel'], self.font, 'lm', 'S_Tel'))
        y += self.increment
        self.labels.append(text_label(self.draw, (x+width, y), self.data['S_Email'], self.font, 'lm', 'S_Email'))
        y += self.increment

        return y