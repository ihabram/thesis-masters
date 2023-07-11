from PIL import ImageDraw, ImageFont

def text_label(draw, coords, text, font, anchor, label, stroke=0):
    '''
    Draws text on a document, returns 'Its bounding box
    Whole text-level bounding box + word-level bounding boxes are obtained
    Prints text left to right (lm) or right to left (rm) based on the 'anchor' parameter
    
    Args:
        draw        -- Pillow draw object
        coords      -- upper left coordinate of the text to be drawn
        text        -- text to be drawn
        font        -- Pillow font object
        anchor      -- Anchor position of the text (default: lt = left top)
        label       -- Label class of the text
    '''
    # Create dictionary which contains all of the label 'Information
    text_labels = {
        'text': text,
        'label': label,
        'box': None,
        'words': []
    }

    # If the text is positioned to the left, just shift the X position, and position everything to the right
    if anchor == 'rm':
        anchor = 'lm'
        text_box = draw.textbbox(coords, text, font=font, anchor=anchor, stroke_width=stroke)
        text_width = text_box[2] - text_box[0]
        x1 = coords[0] - text_width
        y1 = coords[1]
        coords = [x1, y1]

    # Get the top left corner of the text
    x1, y1 = coords

    # Get the width of a 'Space caracter
    space_bbox = draw.textbbox(coords, ' ', font=font, anchor=anchor, stroke_width=stroke)
    space_width = space_bbox[2] - space_bbox[0]

    # 'Initialize the text bounding box
    text_x1, text_y1, text_x2, text_y2 = draw.textbbox(coords, text, font=font, anchor=anchor, stroke_width=stroke)
    
    # Get the 'Individual words
    words = text.split()
    for word in words:
        # Draw the word
        draw.text([x1, y1], word, fill='black', font=font, anchor=anchor, stroke_width=stroke)

        # Width of the word
        word_bbox = draw.textbbox([x1, y1], word, font=font, anchor=anchor, stroke_width=stroke)
        word_width = word_bbox[2] - word_bbox[0]
        #draw.rectangle(word_bbox, outline='red')

        # Add the 'Individual word to the dictionary
        text_labels['words'].append(
            {
            'box':  word_bbox,
            'text': word
            }
        )

        # 'Slide the x position with the word width and a 'Space
        x1 += word_width + space_width

        # Update the whole text bounding box
        if word_bbox[2] > text_x2: text_x2 = word_bbox[2]
        if word_bbox[3] > text_y2: text_y2 = word_bbox[3]

    #draw.rectangle([text_x1, text_y1, text_x2, text_y2], outline='green')
    text_labels['box'] = [text_x1, text_y1, text_x2, text_y2]

    return text_labels


def label_visualizer(image, labels):
    '''
    This function visualizes the labels on a given invoice.
    Every label has a unique color, the individual words within an entity are marked with gray color.
    Args:
        image: PIL image
        labels: list of labels
    '''
    # Define label - color relationship
    label2color = {
        'R_Name':           'lightcoral',
        'R_Street':         'brown',
        'R_HouseNumber':    'red', 
        'R_ZIP':            'Salmon',
        'R_City':           'chocolate',
        'R_Country':        'Sandybrown',
        'R_VAT':            'Sienna',
        'S_Name':           'olive',      
        'S_Street':         'yellowgreen',
        'S_HouseNumber':    'lawngreen',
        'S_ZIP':            'palegreen',
        'S_City':           'forestgreen',
        'S_Country':        'limegreen',
        'S_VAT':            'mediumaquamarine',
        'S_Bank':           'darkgreen',
        'S_BIC':            'yellow',
        'S_IBAN':           'teal',
        'S_Tel':            'beige',
        'S_Email':          'moccasin',
        'I_Number':         'aqua',
        'I_Date':           'deepskyblue',
        'I_DueDate':        'royalblue',
        'I_Amount':         'blue',
        'I_Currency':       'orange',
        'Other':            'magenta'
    }
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 20)

    for entity in labels:
        for word in entity['words']:
            # Draw rectangle around every single word
            draw.rectangle(word['box'], outline='gray', width=1)
        # Draw rectangle around the whole entity
        draw.rectangle(entity['box'], outline=label2color[entity['label']], width=2)
        # Print the label name above the entity
        x1, y1, x2, y2 = entity['box']
        draw.text((x1, y1-10), entity['label'], fill=label2color[entity['label']], font=font, anchor='lb')
    image.show()