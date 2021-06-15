class Behaviors:
    def __init__(self):
        self.neutral = 0
        self.happy = 0
        self.sad = 0
        self.surprise = 0
        self.angry = 0
        self.disgust = 0
        self.fear = 0
        self.total = 0

    def update_total(self):
        self.total = self.neutral + self.happy + self.sad + self.surprise + self.angry \
                        + self.disgust + self.fear

    def update_behaviors(self, prediction):
        if prediction == "neutral":
            self.neutral += 1
        elif prediction == "happy":
            self.happy += 1
        elif prediction == "sad":
            self.sad += 1
        elif prediction == "surprise":
            self.surprise += 1
        elif prediction == "angry":
            self.angry += 1
        elif prediction == "disgust":
            self.disgust += 1
        elif prediction == "fear":
            self.fear += 1
