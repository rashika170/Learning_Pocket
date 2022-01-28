import numpy as np
import utils
import cv2
import detection
import recognition
class Pipeline :
    def __init__(self,scale=2,max_size=2048):
        self.scale=scale
        self.max_size=max_size
        self.detector = detection.Detector()
        self.recognizer = recognition.Recognizer()
        
    def recognize(self,image,detection_kwargs=None, recognition_kwargs=None):
        image = utils.read(image)
        image = utils.resize_image(image, self.scale, self.max_size)
        if detection_kwargs is None:
            detection_kwargs = {}
        if recognition_kwargs is None:
            recognition_kwargs = {}
        box_groups = self.detector.detect(images=image, **detection_kwargs)
