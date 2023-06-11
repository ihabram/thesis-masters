from PIL import Image, ImageDraw

def generate_logo(width, height, background_color, shape_color, pattern_color):
    # Create a new image with the specified dimensions and background color
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Draw a shape on the image
    shape_width = width // 2
    shape_height = height // 2
    shape_x = (width - shape_width) // 2
    shape_y = (height - shape_height) // 2
    draw.rectangle((shape_x, shape_y, shape_x + shape_width, shape_y + shape_height), fill=shape_color)

    # Draw a pattern on the shape
    pattern_width = shape_width // 4
    pattern_height = shape_height // 4
    pattern_x = shape_x + (shape_width - pattern_width) // 2
    pattern_y = shape_y + (shape_height - pattern_height) // 2
    draw.rectangle((pattern_x, pattern_y, pattern_x + pattern_width, pattern_y + pattern_height), fill=pattern_color)

    return image


# Number of logos to generate
num_logos = 1

dir = r'C:\Users\Habram\Documents\Datasets\Company_logos/'

for i in range(num_logos):
    # Generate the logo
    logo = generate_logo(200, 200, "white", "blue", "yellow")

    # Save the logo as an image
    logo.save(dir + str(i) + '.png')