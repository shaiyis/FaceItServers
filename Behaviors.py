class Behaviors:
    def __init__(self, neutral=0, happy=0, sad=0, surprise=0, angry=0, disgust=0, fear=0, total=0):
        self.neutral = neutral
        self.happy = happy
        self.sad = sad
        self.surprise = surprise
        self.angry = angry
        self.disgust = disgust
        self.fear = fear
        self.total = total

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
