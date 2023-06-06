
def text_label(draw, coords, text, font, anchor, label):
    '''
    Draws text on a document, returns its bounding box
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
    # Create dictionary which contains all of the label information
    text_labels = {
        'text': text,
        'label': label,
        'box': None,
        'words': []
    }

    # If the text is positioned to the left, just shift the X position, and position everything to the right
    if anchor == 'rm':
        anchor = 'lm'
        text_box = draw.textbbox(coords, text, font=font, anchor=anchor)
        text_width = text_box[2] - text_box[0]
        x1 = coords[0] - text_width
        y1 = coords[1]
        coords = [x1, y1]

    # Get the top left corner of the text
    x1, y1 = coords

    # Get the width of a space caracter
    space_bbox = draw.textbbox(coords, ' ', font=font, anchor=anchor)
    space_width = space_bbox[2] - space_bbox[0]

    # Initialize the text bounding box
    text_x1, text_y1, text_x2, text_y2 = draw.textbbox(coords, text, font=font, anchor=anchor)
    
    # Get the individual words
    words = text.split()
    for word in words:
        # Draw the word
        draw.text([x1, y1], word, fill='black', font=font, anchor=anchor)

        # Width of the word
        word_bbox = draw.textbbox([x1, y1], word, font=font, anchor=anchor)
        word_width = word_bbox[2] - word_bbox[0]
        draw.rectangle(word_bbox, outline='red')

        # Add the individual word to the dictionary
        text_labels['words'].append(
            {
            'box':  word_bbox,
            'text': word
            }
        )

        # Slide the x position with the word width and a space
        x1 += word_width + space_width

        # Update the whole text bounding box
        if word_bbox[2] > text_x2: text_x2 = word_bbox[2]
        if word_bbox[3] > text_y2: text_y2 = word_bbox[3]

    draw.rectangle([text_x1, text_y1, text_x2, text_y2], outline='green')
    text_labels['box'] = [text_x1, text_y1, text_x2, text_y2]

    return text_labels