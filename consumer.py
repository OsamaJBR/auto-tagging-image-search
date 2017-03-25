#!/usr/bin/python
from ConfigParser import SafeConfigParser
from queue import Queue
from tagging import Tagging
from translate import Translater
from searchengine import SEngine
import datetime
import logging
import sys
import os
import time

def get_image_content(image_path):
    image = open(image_path, 'r')
    return image.read() 

# logger
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.debug("logging started")
logger = logging.getLogger(__name__)

# Config Parsing
config = SafeConfigParser()
config.read('config.ini')

# Queue 
queue = Queue(config)
tagging = Tagging(config)
translater = Translater(config)
es_engine = SEngine(config)
# consuming forever
while True:
    # ensure all arrays are empy
    doc={}
    tags=[]
    translated_tags=[]
    
    # get image to process
    image = queue.pop_from_queue()
    if not image : 
        time.sleep(0.25)
        continue
    logger.info('recieved image=%s',image)
    image_content = get_image_content(image)
    logger.info('getting tags for image=%s',image)
    tags = tagging.get_tags(image_binary=image_content)
    if config.get('translation','enabled') == 'true' :
        logger.info('translating tags for image=%s',image)
        translated_tags=translater.translate_tags(target=config.get('translation','target'),tags=tags)
    
    # Prepare ElasticSearch Document
    doc['image_type']=os.path.splitext(image)[1]
    doc['image_fname']=os.path.basename(image)
    doc['image_path']=image
    doc['uploaded_at']=datetime.datetime.fromtimestamp( 
        int(os.path.getmtime(image))
        ).strftime('%Y-%m-%d %H:%M:%S')
    doc['timestamp']=int(time.time())
    doc['en_lables']=tags
    if translated_tags :
        target_lang=config.get('translation','target')
        doc['%s_lables'%target_lang]=translated_tags
    logger.info('pusing all details to elasticsearch for image=%s',image)
    if not es_engine.push_to_es(doc=doc) :
        queue.add_to_queue(queue_name='failed_queue',image=image)
    