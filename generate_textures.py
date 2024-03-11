import os
import csv
from PIL import Image, ImageDraw, ImageFont

IMAGE_SIZE = 128
SYMBOL_MARGIN_BOTTOM = IMAGE_SIZE // 5
NUMBER_MARGIN_TOP = IMAGE_SIZE // 20

FONT_PATH = "./font.otf"
SYMBOL_FONT_SIZE = IMAGE_SIZE // 2
SYMBOL_NUMBER_FONT_SIZE = IMAGE_SIZE // 6
TEXT_COLOR = "black"
BORDER_COLOR = "black"
BORDER_WIDTH = 2

group_colors = {
    "Nonmetal": "#4E79A7",  # Blue
    "Noble Gas": "#F28E2B",  # Orange
    "Alkali Metal": "#E15759",  # Red
    "Alkaline Earth Metal": "#76B7B2",  # Cyan
    "Metalloid": "#59A14F",  # Green
    "Post-Transition Metal": "#EDC948",  # Yellow
    "Halogen": "#B07AA1",  # Purple
    "Transition Metal": "#FF9DA7",  # Pink
    "Lanthanide": "#9C755F",  # Brown
    "Actinide": "#BAB0AC",  # Grey
}


def create_element_texture(number, symbol, group):
    color = group_colors.get(group, "#ffffff")  # Default to white if group not found
    image = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), color)
    draw = ImageDraw.Draw(image)

    for i in range(BORDER_WIDTH):
        draw.rectangle(
            [
                i,
                i,
                IMAGE_SIZE - i - 1,
                IMAGE_SIZE - i - 1,
            ],  # Adjusted coordinates
            outline=BORDER_COLOR,
        )

    symbol_font = ImageFont.truetype(FONT_PATH, SYMBOL_FONT_SIZE)
    number_font = ImageFont.truetype(FONT_PATH, SYMBOL_NUMBER_FONT_SIZE)

    # Position the symbol at the bottom half of the image
    symbol_bbox = draw.textbbox((0, 0), symbol, font=symbol_font)
    symbol_width = symbol_bbox[2] - symbol_bbox[0]
    symbol_height = symbol_bbox[3] - symbol_bbox[1]
    symbol_position = (
        (IMAGE_SIZE - symbol_width) / 2,
        IMAGE_SIZE - symbol_height - SYMBOL_MARGIN_BOTTOM,
    )

    # Position the element number at the upper left-hand corner
    number_position = (NUMBER_MARGIN_TOP, NUMBER_MARGIN_TOP)

    # Draw the symbol and element number
    draw.text(
        symbol_position,
        symbol,
        fill=TEXT_COLOR,
        font=symbol_font,
    )
    draw.text(
        number_position,
        number,
        fill=TEXT_COLOR,
        font=number_font,
    )

    # Save the image
    image.save(f"textures/{symbol}.png", "PNG")


# Ensure the textures directory exists
textures_directory = "textures"
if not os.path.exists(textures_directory):
    os.makedirs(textures_directory)

# Read the CSV and generate textures
with open("elements.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        create_element_texture(
            row["Number"],
            row["Symbol"],
            row["Group"],
        )
