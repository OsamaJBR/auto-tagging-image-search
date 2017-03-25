import io
import os

class Tagging():
    def __init__(self,config):
        self.google_credentials=config.get('image-recognition','google-credentials')
        self.google_project=config.get('image-recognition','google-project')
        self.tags_backend=config.get('image-recognition','backend')

    def get_tags(self,image_binary):
        if self.tags_backend == 'google-vision' : 
            tags = self.google_vision(image_binary=image_binary)
        elif self.tags_backend == 'aws-rekognition':
            tags = self.aws_rekognition(image_binary=image_binary)
        return tags

    def google_vision(self,image_binary):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.google_credentials
        os.environ["GOOGLE_CLOUD_PROJECT"] = self.google_project
        from google.cloud import vision
        vision_client = vision.Client()
        # Loads the image into memory
        image = vision_client.image(content=image_binary)
        # Performs label detection on the image file
        labels = image.detect_labels()
        tags = []
        for label in labels:
            tags.append(label.description)
        return tags

    def aws_rekognition():
        return True 