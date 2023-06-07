from PIL import Image, ImageDraw, ImageFont
from annotator import text_label
import random

class Draw_Table():
    '''
    This class is used to print tables on invoices
    The table always has a 'Description' column as the first column and 'Brutto' as the last column.
    The 'Quantity', 'Tax %' and 'Netto' columns are optional. The number of rows is between 3 and 10.
    The user has to define the bounding box of the table and the currency.
    '''
    def __init__(self) -> None:
        # Possible column names
        self.column_names = ['Description', 'Quantity', 'Tax %', 'Netto', 'Brutto']
        # List of possible items in the table
        self.items = [
            'Electricity',
            'Water',
            'Gas',
            'Printer',
            'Maintenance fee',
            'Desktop monitor',
            'Designing cost',
            'Office chair',
            'Cell phone',
            'Laptop',
            'Network access point',
            'Network switch',
            'Professional beamer',
            'Smart white board',
            'Thermostat',
            'Office plants',
            'Professional software',
            'Printer ink',
            'Cleaning material',
            'Keyboard',
            'Network cable',
            'Security camera',
            'Carpet',
            'Washing machine',
            'Kitchen sink',
            'Garbage can'
        ]

    def __call__(self, drawer, bbox, currency):
        self.draw = ImageDraw.Draw(drawer)
        self.bbox = bbox                            # Bounding box of the table [x1, y1, x2, y2]
        self.currency = currency                    # CUrrency to use in the table
        self.font = ImageFont.truetype("arial.ttf", 30)
        self.num_items = random.randint(3, 10)      # How many rows does the table have (number of items)
        self.num_cols = random.randint(2, 5)        # How many columns does the table have
        self.increment = 50                         # Height of a row in pixels
        self.margin = 12                            # Distance between the table lines and text
        self.labels = []                            # Store the labels of the words

        self.draw_horizontal_lines()
        self.draw_vertical_lines()
        self.draw_content()

        return self.labels

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
        self.draw.text((positions[0] + self.margin, self.bbox[1]), self.column_names[0], fill='black', font=self.font, anchor='lm', stroke_width=1)

        # Print the rest of the columns to the right
        for col in range(self.num_cols - 2):
            self.draw.text((positions[col+2] - self.margin, self.bbox[1]), self.column_names[col+1], fill='black', font=self.font, anchor='rm', stroke_width=1)

        # Print the last column header (brutto) to the right
        self.draw.text((positions[-1] - self.margin, self.bbox[1]), self.column_names[-1], fill='black', font=self.font, anchor='rm', stroke_width=1)

    def draw_content(self):
        '''
        Populates the table with content
        '''
        # Draw the header part
        self.draw_header()

        # Sample random fake data
        descriptions = random.sample(self.items, self.num_items-1)  # Random items from the predefined list
        quantities = random.sample(range(1, 20), self.num_items-1)  # Random quantity between 1 and 20
        taxes = random.sample(range(5, 20), self.num_items-1)       # Tax rate between 5 and 20
        nettos = random.sample(range(5000), self.num_items-1)       # Netto price
        bruttos = [round(a+a*b*0.01, 1) for a,b in zip(nettos,taxes)]   # Brutto price based on netto and tax (rounded to 2 decimals)
        
        # Organize the generated data in a list (already a 2d table format)
        data = [descriptions, quantities, taxes, nettos, bruttos]

        # Get the X coordinate of the beginning of the columns
        positions = self.get_x_positions()

        # Print the data into the table
        for row in range(self.num_items -1):
            for col in range(self.num_cols -1):
                self.draw.text((positions[col +1] - self.margin, self.bbox[1]+row*self.increment+self.increment+self.margin), str(data[col][row]), fill='black', font=self.font, anchor='rt')
            # Print the brutto separately (currency has to be added)
            self.draw.text((positions[-1] - self.margin, self.bbox[1]+row*self.increment+self.increment+self.margin), str(data[-1][row])+' '+self.currency, fill='black', font=self.font, anchor='rt')

        # Print the sum field
        summa = sum(bruttos)
        summa = round(summa, 2)
        self.draw_sum_field(str(summa))

    def draw_sum_field(self, summa):
        x = self.bbox[2] - self.margin
        self.draw.text((x, self.bbox[1] + self.increment*self.num_items + self.margin), summa + ' ' + self.currency, fill='black', font=self.font, anchor='rt')
        text_width, text_height = self.draw.textsize(summa + ' ' + self.currency, font=self.font)
        self.draw.text((x - text_width - 8, self.bbox[1] + self.increment*self.num_items + self.margin), 'Sum: ', fill='black', font=self.font, anchor='rt', stroke_width=1)
