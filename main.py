#!/usr/bin/python
import sys
from bottle import Bottle,run, route, request, default_app, HTTPResponse, response
from ConfigParser import SafeConfigParser
from queue import Queue
import magic
import logging
import json
import os

# logger
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.debug("logging started")
logger = logging.getLogger(__name__)

# current working directory
here = os.path.dirname(__file__)

# Config Parsing
config = SafeConfigParser()
config.read('config.ini')

# uWSGI
app = application = Bottle()

# Consumer Queue
queue = Queue(config)

# Search Engine
from searchengine import SEngine
search_engine = SEngine(config)

# routes 
@route('/upload',method='POST')
def upload_image():
    name = request.forms.get('name')
    data = request.files.get('data')
    if name and data and data.file:
        raw = data.file.read()
        filename = data.filename
        save_path="{path}/{file}".format(
                path=config.get('storage','imagesdir'),
                file=filename
                )
        if not os.path.exists(config.get('storage','imagesdir')):
            os.makedirs(save_path)
        if 'image' not in magic.from_buffer(raw):
            return HTTPResponse(status=400,body=json.dumps({'error' : 'file type is not allowed'}))
        with open(save_path,'w') as open_file:
            open_file.write(raw)
        if queue.add_to_queue(queue_name='images',image=save_path):
            return HTTPResponse(status=200,body=json.dumps({'status' : 'Image Stored'}))
        else:
            return HTTPResponse(status=500,body=json.dumps({'error' : 'Internal Server Error'}))
    else:
        return HTTPResponse(status=400,body=json.dumps({'error' : 'missing fields'}))

@route('/search')
def search():
    words = request.query.get('words')
    operator = request.query.get('op','OR')
    return search_engine.search_for_words(op=operator,words=words)

@route('/image')
def get_images():
    image_path = request.query.get('path',None)
    if os.path.exists(image_path):
        data = open(image_path,'rb').read()
        response.set_header('Content-type', 'image/jpeg')
        return data
    else:
        HTTPResponse(status=404,body=json.dumps({'error' : 'image not found'}))

#------------------
# MAIN
#------------------

if __name__ == "__main__" :
	run(host=config.get('http','bind'), port=config.get('http','port'), debug=True)
else:
	application = default_app()