__author__ = 'sergio'

import urllib2
import json
from artwork import Artwork
import random
import os
import csv


def facebook():
    artwork = Artwork()
    backgrounds = os.listdir(os.path.join(artwork.BASE_DIR, 'backgrounds'))
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
            'color_text': (37, 51, 109),
            'name_output': item['id']
        })
    print "Finish"


def by_csv():
    """
    nota 1
        El csv debe estar en la carpeta Artwork
    nota 2
        El csv debe ser:#
           caracteres: unicode(UTF-8)
           Idioma: Espanol mexico
           separado: coma
           delimitador de texto: '
    """
    artwork = Artwork()
    backgrounds = os.listdir(os.path.join(artwork.BASE_DIR, 'backgrounds'))
    csv_name = raw_input("Nombre del csv: ")
    file_path = os.path.join(artwork.BASE_DIR, csv_name)

    with open(file_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for item in spamreader:
            name = item[0].decode('utf-8')
            message = item[1].decode('utf-8')

            artwork.save_picture({
                'background': random.choice(backgrounds),
                'message':message,
                'name': name,
                'color_text': (37, 51, 109),
                'name_output': name
            })


def main():
    by_csv()


if __name__ == '__main__':
    main()



