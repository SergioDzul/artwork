__author__ = 'sergio'

import urllib2
import json
from artwork import Artwork
import random
import os


def main():
    artwork = Artwork()
    backgrounds = os.listdir(os.path.join(artwork.BASE_DIR, 'Artwork', 'backgrounds'))
    url = raw_input("Ingresa la url para optener los mensajes: ")

    request = urllib2.urlopen(url)
    raw_data = request.read()
    json_comments = json.loads(raw_data)
    messages = json_comments['data']
    for item in messages:
        artwork.save_picture({
            'background': random.choice(backgrounds),
            'message': item['message'],
            'name': item['from']['name'],
            'color_text': (80, 0, 229),
            'name_output': item['id']
        })
    print "Finish"


if __name__ == '__main__':
    main()



