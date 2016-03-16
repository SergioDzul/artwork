__author__ = 'sergio'
from PIL import Image, ImageDraw, ImageFont, ImageOps
import StringIO
import textwrap
import os


class Artwork():
    """
    Artwork core
    """

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_text_size(self, message):
        default = 30
        if len(message) > 195:
            return 20

        return default

    def generate_artwork(self, data):
        """
        Generate artwork
        """
        background = data['background']
        message = data['message']
        message = message.capitalize()
        name = data['name']
        color_text = data['color_text']

        ### variables ###

        # icon_size = (125, 70)
        background_size = (640, 453)
        laurel_size = (25, 55)
        margin_laurel = 5
        margin_bottom = 15
        name_static_h = 398
        name_size = 25
        message_size = self.get_text_size(message)

        dir_background = os.path.join(self.BASE_DIR, 'Artwork', 'backgrounds', background)
        dir_font = os.path.join(self.BASE_DIR, 'Artwork', 'fonts', 'ArchitectsDaughter.ttf')
        dir_laurel = os.path.join(self.BASE_DIR, 'Artwork', 'resources', 'laurel-right.png')
        array_of_string = textwrap.wrap(message, width=30)
        font_name = ImageFont.truetype(dir_font, size=name_size)
        font_message = ImageFont.truetype(dir_font, size=message_size)

        ### end variables ###

        ### background ###

        background = Image.open(dir_background)
        background = background.resize(background_size, Image.ANTIALIAS)
        draw = ImageDraw.Draw(background, 'RGBA')
        background_w, background_h = background_size
        name_w, name_h = draw.textsize(name, font=font_name)

        ### end backgrount ###


        ### message process ###

        total_sub_strings = len(array_of_string)
        counter = total_sub_strings
        try:
            temp_w, temp_h = draw.textsize(array_of_string[0], font=font_message)
            temp_w += 2
            temp_h += 2
            not_problem = True
        except Exception:
            print(Exception)
            temp_w, temp_h = draw.textsize(message, font=font_message)
            temp_w += 2
            temp_h += 2
            not_problem = False


        message_h = ((background_h - (temp_h * (total_sub_strings)))/2) - temp_h
        message_h -= name_h

        if not_problem:

            for substring in array_of_string:
                sub_w, sub_h = draw.textsize(substring, font=font_message)
                message_h += temp_h
                position = (
                    (background_w-sub_w)/2,
                    message_h
                )
                draw.text(position, substring, fill=color_text, font=font_message)
                counter -= 1
        else:

            position = (
                    (background_w-temp_w)/2,
                    message_h
                )
            draw.text(position, message, fill=color_text, font=font_message)

        ### end message process ###

        ### name process ###

        name_position = (
            (background_w-name_w)/2,
            message_h+temp_h+margin_bottom)

        draw.text(name_position, name, fill=color_text, font=font_name)

        ### end name process ###

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
        name_output = data['name_output']
        image = self.generate_artwork(data)
        name_of_file = name_output.replace(' ', '_')
        dir_save = os.path.join(self.BASE_DIR, 'Artwork', 'outputs', name_of_file+'.png')
        image.save(dir_save)
        print(dir_save)