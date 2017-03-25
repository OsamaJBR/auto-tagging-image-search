from google.cloud import translate
import os

class Translater():
    def __init__(self,config):
        self.google_credentials=config.get('image-recognition','google-credentials')
        self.google_project=config.get('image-recognition','google-project')
    
    def translate_text(self,target, text):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.google_credentials
        os.environ["GOOGLE_CLOUD_PROJECT"] = self.google_project
        translate_client = translate.Client()
        result = translate_client.translate(
            text,
            target_language=target)
        return result.get('translatedText')
        
    def translate_tags(self,target,tags):
        translated_tags=[]
        for tag in tags: 
            translated_tags.append(self.translate_text(target=target,text=tag))
        return translated_tags
