from paz.applications import HaarCascadeFrontalFace, MiniXceptionFER
import paz.processors as pr
import numpy as np
import cv2
import socket


class EmotionDetector(pr.Processor):
    def __init__(self):
        super(EmotionDetector, self).__init__()
        self.detect = HaarCascadeFrontalFace(draw=False)
        self.crop = pr.CropBoxes2D()
        self.classify = MiniXceptionFER()
        self.draw = pr.DrawBoxes2D(self.classify.class_names)

    def call(self, image):
        predictions = []
        boxes2D = self.detect(image)['boxes2D']
        cropped_images = self.crop(image, boxes2D)
        for cropped_image, box2D in zip(cropped_images, boxes2D):
            box2D.class_name = self.classify(cropped_image)['class_name']
            predictions.append(box2D.class_name)
            # print(box2D.class_name)
        if len(predictions) > 0:
            return predictions[0]
        # got more than 1 face?
        # return self.draw(image, boxes2D)


# detect = EmotionDetector()
# image = cv2.imread("images/photo_2021-04-21_21-11-51.jpg")
# detect.call(image)

