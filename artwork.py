__author__ = 'sergio'
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os.path
import StringIO
import textwrap
import os

class Artwork():
    """
    Artwork core
    """

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def generate_artwork(self, data):
        """
        Generate artwork
        """
        background = data['background']
        message = data['message']
        name = data['name']
        color_text = data['color_text']

        ### variables ###

        # icon_size = (125, 70)
        background_size = (640, 453)
        laurel_size = (25, 45)
        margin_laurel = 5
        margin_bottom = 15
        dir_background = os.path.join(self.BASE_DIR, 'Artwork', 'backgrounds', background)
        dir_font = os.path.join(self.BASE_DIR, 'Artwork', 'fonts', 'ArchitectsDaughter.ttf')
        dir_laurel = os.path.join(self.BASE_DIR, 'Artwork', 'resources', 'laurel-right.png')
        array_of_string = textwrap.wrap(message, width=30)
        font_name = ImageFont.truetype(dir_font, size=25)
        font_message = ImageFont.truetype(dir_font, size=20)

        ### end variables ###

        ### background ###

        background = Image.open(dir_background)
        background = background.resize(background_size, Image.ANTIALIAS)
        draw = ImageDraw.Draw(background, 'RGBA')
        background_w, background_h = background_size
        name_w, name_h = draw.textsize(name, font=font_name)

        ### end backgrount ###

        ### name process ###

        name_position = (
            (background_w-name_w)/2,
            (background_h-name_h)-margin_bottom)
        draw.text(name_position, name, fill=color_text, font=font_name)

        ### end name process ###

        ### message process ###

        total_sub_strings = len(array_of_string) + 1
        counter = total_sub_strings

        sub_w, sub_h = draw.textsize(array_of_string[0], font=font_message)
        message_h = (name_position[1] - (sub_h * total_sub_strings)) - sub_h


        for substring in array_of_string:
            position = (
                (background_w-sub_w)/2,
                (
                   message_h + (sub_h*counter)
                )
            )
            draw.text(position, substring, fill=color_text, font=font_message)
            counter -= 1

        ### end message process ###

        ### laurels ###

        laurel = Image.open(dir_laurel)
        laurel_w, laurel_h = laurel_size
        laurel = laurel.resize(laurel_size, Image.ANTIALIAS)
        laurel = laurel.convert("RGBA")
        laurel_mirror = ImageOps.mirror(laurel)
        laurel_position = (
            ((name_position[0]+name_w)-(laurel_w/2))+margin_bottom,
            name_position[1]-margin_laurel
        )

        mirror_position = (
            (name_position[0]-(laurel_w/2))-margin_bottom,
            name_position[1]-margin_laurel
        )

        background.paste(laurel_mirror, mirror_position, mask=laurel_mirror)
        background.paste(laurel, laurel_position, mask=laurel)
        ### end laurel ###

        return background

    def generate_picture_64(self, data):
        artwork = self.generate_artwork(data)
        output = StringIO.StringIO()
        artwork.save(output, 'PNG')
        content = output.getvalue().encode("base64")
        output.close()
        return content

    def save_picture(self, data):
        image = self.generate_artwork(data)
        name_of_file = data['name'].replace(' ', '_')
        dir_save = os.path.join(self.BASE_DIR, 'Artwork', 'outputs', name_of_file+'.png')
        image.save(dir_save)
        print(dir_save)