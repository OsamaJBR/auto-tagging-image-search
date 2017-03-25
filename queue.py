from ConfigParser import SafeConfigParser
import redis
import logging
import sys

# logger
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.debug("logging started")
logger = logging.getLogger(__name__)


class Queue():
    def __init__(self,config):
        self.redis_host=config.get('redis','host')
        self.redis_port=int(config.get('redis','port'))
        self.redis_db=int(config.get('redis','db'))
        
    def add_to_queue(self,queue_name,image):
        redis_sess = redis.StrictRedis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db
            )
        try : 
            redis_sess.rpush(queue_name,image)
            return True
        except Exception as e :
            logger.error('Error while trying to adding image to queue : %s',str(e))
            return False

    def pop_from_queue(self):
        redis_sess = redis.StrictRedis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db
            )
        try : 
            return redis_sess.lpop('images')
        except Exception as e :
            logger.error('Error while trying to pop image from the queue : %s',str(e))
            return False