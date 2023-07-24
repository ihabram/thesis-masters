from PIL import Image, ImageDraw, ImageFont
from annotator_de import text_label
import random

class LayoutManager():
    def __init__(self) -> None:
        pass

    def __call__(self):
        pass

    def get_layout(self):
        layouts = []

        # Agder
        layouts.append({
            'R_field': [100, 350, 600, 800],    # Recipient
            'S_field': [900, 250, 1538, 650],   # Supplier
            'D_field': [900, 700, 1538, 950],   # Date (and contact)
            'L_field': [1200, 30, 1538, 200],   # Logo
            'T_field': [100, 1100, 1538, 1750], # Table
            'I_field': [100, 2100, 1538, 2250], # Information
            'Q_field': [350, 700, 700, 1000]   # QR code
        })

        # 50 Hertz
        layouts.append({
            'R_field': [190, 360, 500, 620],    # Recipient
            'S_field': [970, 335, 1530, 1033],  # Supplier
            'D_field': [970, 1217, 1530, 1670], # Date (and contact)
            'L_field': [790, 57, 1238, 220],    # Logo
            'T_field': [70, 1410, 861, 1953],   # Table
            'I_field': [50, 2000, 1588, 2250],  # Information
            'Q_field': [637, 737, 869, 929]    # QR code
        })

        # Cursor
        layouts.append({
            'R_field': [153, 341, 617, 609],    # Recipient
            'S_field': [1065, 341, 1465, 817],  # Supplier
            'D_field': [165, 773, 621, 1133], # Date (and contact)
            'L_field': [1089, 65, 1461, 273],    # Logo
            'T_field': [137, 1209, 1577, 2009],   # Table
            'I_field': [97, 2113, 1517, 2277],  # Information
            'Q_field': [693, 501, 969, 729]    # QR code
        })

        # Fiorentini
        layouts.append({
            'R_field': [181, 429, 777, 805],    # Recipient
            'S_field': [941, 261, 1465, 669],  # Supplier
            'D_field': [953, 693, 1501, 945], # Date (and contact)
            'L_field': [45, 65, 193, 213],    # Logo
            'T_field': [181, 1241, 1557, 2197],   # Table
            'I_field': [269, 45, 1105, 205],  # Information
            'Q_field': [1073, 1005, 1449, 1142]    # QR code
        })

        # XING
        layouts.append({
            'R_field': [133, 301, 637, 653],    # Recipient
            'S_field': [521, 1473, 1165, 1821],  # Supplier
            'D_field': [1057, 389, 1529, 661], # Date (and contact)
            'L_field': [1085, 53, 1493, 317],    # Logo
            'T_field': [125, 781, 1481, 1193],   # Table
            'I_field': [81, 1969, 1581, 2181],  # Information
            'Q_field': [537, 45, 821, 213]    # QR code
        })

        return random.choice(layouts)
    
    def visualize_layout(self, layout, drawer, font, canvas):
        for key in layout:
            drawer.rectangle(layout[key], outline='black')
            drawer.text(layout[key], key, font=font, fill='black')
        canvas.show()

class Draw_Table():
    '''
    This class is used to print tables on invoices
    The table always has a 'Description' column as the first column and 'Brutto' as the last column.
    The 'Quantity', 'Tax %' and 'Netto' columns are optional. The number of rows is between 3 and 10.
    The user has to define the bounding box of the table and the currency.
    '''
    def __init__(self) -> None:
        # Possible column names
        self.column_names = ['Beschreibung', 'Menge', 'Steuer %', 'Netto', 'Brutto']
        # List of possible items in the table
        self.items = [
             'Elektrizität',
             'Wasser',
             'Gas',
             'Drucker',
             'Wartungsgebühr',
             'Desktop-Monitor',
             'Entwurfskosten',
             'Bürostuhl',
             'Handy',
             'Laptop',
             'Netzwerkzugangspunkt',
             'Netzwerkschalter',
             'Professioneller Beamer',
             'Intelligentes Whiteboard',
             'Thermostat',
             'Büropflanzen',
             'Professionelle Software',
             'Druckertinte',
             'Reinigungsmittel',
             'Klaviatur',
             'Netzwerkkabel',
             'Überwachungskamera',
             'Teppich',
             'Waschmaschine',
             'Spülbecken',
             'Mülleimer',
             'Üblicher Service',
             'Reinigung',
             'Servergebühr',
             'Versicherung',
             'Möbel',
             'Sicherheitskosten',
             'Powerbank',
             'Datentransfer',
             'Isolation',
             'Werbung',
             'Kühlung',
             'Parteiorganisation',
             'Premium-Kosten',
             'Kaution',
             'Umkleidekosten',
             'Registrierungsgebühr'
         ]

    def __call__(self, labels, draw, font, bbox, data):
        self.draw = draw
        self.bbox = bbox                            # Bounding box of the table [x1, y1, x2, y2]
        self.currency = data['I_Currency']          # Currency to use in the table
        self.font = font                            # Font of the document
        self.increment = self.get_increment()       # Height of a row in pixels
        self.num_items = self.get_num_rows()        # How many rows does the table have (number of items)
        self.num_cols = self.get_num_cols()         # How many columns does the table have
        self.margin = self.get_margin()             # Distance between the table lines and text
        self.labels = labels                        # Store the labels of the words

        if random.random() < 0.6:
            self.draw_horizontal_lines()
            if random.random() < 0.6:
                self.draw_vertical_lines()
        self.draw_content()

        return self.labels
    
    def get_num_rows(self):
        '''
        The height of the table should be smaller than the height of the bounding box
        '''
        height_bbox = self.bbox[3] - self.bbox[1]
        max_num = int(height_bbox / self.increment)

        return random.randint(3, max_num)

    def get_num_cols(self):
        '''
        The width of the table should be smaller than the width of the bounding box
        '''
        width_bbox = self.bbox[2] - self.bbox[0]
        bbox = self.draw.textbbox((0, 0), 'Washing machine', font=self.font)
        width_text = bbox[2] - bbox[0]
        max_num = int(width_bbox / width_text)
        if max_num > 5: max_num = 5

        return random.randint(2, max_num)

    def get_increment(self):
        '''
        The height of a row depends on the font size.
        '''
        bbox = self.draw.textbbox((0, 0), 'A', font=self.font)
        height = bbox[3] - bbox[1]

        return int(0.6*height + height)
    
    def get_margin(self):
        '''
        Get the distance between the text and the table grid
        '''
        bbox = self.draw.textbbox((0, 0), 'A', font=self.font)
        height = bbox[3] - bbox[1]
        
        return int(0.4*height)


    def get_x_positions(self):
        '''
        Calculates the horizontal positions where the table is getting divided (column boundaries)
        Only the table width is defined, the column positions depend on the number of the columns

        Return
            List of column boundaries
        '''
        # Width of the table x2 - x1
        full_width = self.bbox[2] - self.bbox[0]
        # Width of one column
        col_width = int(full_width / self.num_cols)
        # X coordinate of the beginning of the columns
        col_positions = []
        # The table has an offset, add this offset to the columns too
        # (The table doesn't begins at the very left of the invoice)
        pos = self.bbox[0]

        for _ in range(self.num_cols):
            col_positions.append(pos)
            pos += col_width
        col_positions.append(pos)
        col_positions[1] = int(col_positions[1] + col_positions[1]*0.15)   # Make the first column 15% wider

        return col_positions

    def draw_horizontal_lines(self):
        '''
        Draws the horizontal lines of the table
        '''
        # Get the XY positions of the first horizontal line
        left_x, left_y, right_x, right_y = self.bbox
        right_y = self.bbox[1]

        for _ in range(self.num_items):
            # Increase the Y value by the defined row height
            left_y += self.increment
            right_y += self.increment
            self.draw.line([(left_x, left_y), (right_x, right_y)], fill ="black", width = 2)

    def draw_vertical_lines(self):
        '''
        Draws the vertical lines of the table
        '''
        # Get the Y values of the vertical lines
        top_y = self.bbox[1] + self.increment
        bot_y = self.bbox[1] + (self.increment * self.num_items)

        # Get the X values of the vertical lines
        positions = self.get_x_positions()

        # Draw the lines one-by-one
        for pos_x in positions:  
            self.draw.line([(pos_x, top_y), (pos_x, bot_y)], fill ="black", width = 2)

    def draw_header(self):
        '''
        Draw the header of the table 
        The header is always bold and above the table
        '''
        # Get the X coordinate of the beginning of the columns
        positions = self.get_x_positions()
        
        # Print the first column header (description) to the left
        self.labels.append(text_label(self.draw, (positions[0] + self.margin, self.bbox[1]), self.column_names[0], self.font, anchor='lm', label='Other', stroke=1))
        # Print the rest of the columns to the right
        for col in range(self.num_cols - 2):
            self.labels.append(text_label(self.draw, (positions[col+2] - self.margin, self.bbox[1]), self.column_names[col+1], self.font, anchor='rm', label='Other', stroke=1))

        # Print the last column header (brutto) to the right
        self.labels.append(text_label(self.draw, (positions[-1] - self.margin, self.bbox[1]), self.column_names[-1], self.font, anchor='rm', label='Other', stroke=1))

    def draw_content(self):
        '''
        Populates the table with content
        '''
        # Draw the header part
        self.draw_header()
        # Sample random fake data
        descriptions = random.sample(self.items, self.num_items-1)  # Random items from the predefined list
        quantities = random.sample(range(1, 10+self.num_items), self.num_items-1)  # Random quantity between 1 and 20
        taxes = random.sample(range(5, 10+self.num_items), self.num_items-1)       # Tax rate between 5 and 20
        nettos = random.sample(range(5000), self.num_items-1)       # Netto price
        bruttos = [round(a+a*b*0.01, 1) for a,b in zip(nettos,taxes)]   # Brutto price based on netto and tax (rounded to 2 decimals)
        
        # Organize the generated data in a list (already a 2d table format)
        data = [descriptions, quantities, taxes, nettos, bruttos]

        # Get the X coordinate of the beginning of the columns
        positions = self.get_x_positions()

        # Print the data into the table
        for row in range(self.num_items -1):
            # Print the description separately (aligned to the left)
            self.labels.append(text_label(self.draw, (positions[0] + self.margin, self.bbox[1]+row*self.increment+self.increment+self.increment/2), str(data[0][row]), font=self.font, anchor='lm', label='Other'))
            for col in range(self.num_cols -2):
                self.labels.append(text_label(self.draw, (positions[col +2] - self.margin, self.bbox[1]+row*self.increment+self.increment+self.increment/2), str(data[col+1][row]), font=self.font, anchor='rm', label='Other'))
            # Print the brutto separately (currency has different label)
            # Print the currency
            self.labels.append(text_label(self.draw, (positions[-1] - self.margin, self.bbox[1]+row*self.increment+self.increment+self.increment/2), self.currency, font=self.font, anchor='rm', label='Other'))
            # Print the brutto amount (shift by the width of the currency)
            space_bbox = self.draw.textbbox((0, 0), ' ' + self.currency, font=self.font)
            space_width = space_bbox[2] - space_bbox[0]
            self.labels.append(text_label(self.draw, (positions[-1] - self.margin - space_width, self.bbox[1]+row*self.increment+self.increment+self.increment/2), str(data[-1][row]), font=self.font, anchor='rm', label='Other'))

        # Print the sum field
        summa = sum(bruttos)
        summa = round(summa, 2)
        self.draw_sum_field(str(summa))

    def draw_sum_field(self, summa):
        # Print the currency
        self.labels.append(text_label(self.draw, (self.bbox[2] - self.margin, self.bbox[1] + self.increment*self.num_items + self.margin*4), self.currency, self.font, 'rm', 'Other'))
        # Print the sum amount
        space_bbox = self.draw.textbbox((0, 0), ' ' + self.currency, font=self.font)
        space_width = space_bbox[2] - space_bbox[0]
        self.labels.append(text_label(self.draw, (self.bbox[2] - self.margin - space_width, self.bbox[1] + self.increment*self.num_items + self.margin*4), summa, self.font, 'rm', 'I_Amount', stroke=1))
        # Print the 'Sum' word
        space_bbox = self.draw.textbbox((0, 0), '  '+self.currency+summa, font=self.font)
        space_width = space_bbox[2] - space_bbox[0]
        possible_words = ['Gesamtbetrag:', 'Summe Brutto', 'Endbetrag', 'Rechnungsbetrag:', 'Summe:', 'Bruttobetrag', 'Brutto']
        self.labels.append(text_label(self.draw, (self.bbox[2] - self.margin - space_width*2, self.bbox[1] + self.increment*self.num_items + self.margin*4), random.choice(possible_words), self.font, 'rm', 'Other', stroke=1))