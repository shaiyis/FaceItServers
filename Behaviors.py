class Behaviors:
    def __init__(self, neutral, happy, sad, surprise, angry, disgust, fear):
        self.neutral = neutral
        self.happy = happy
        self.sad = sad
        self.surprise = surprise
        self.angry = angry
        self.disgust = disgust
        self.fear = fear
        self.total = self.neutral + self.happy + self.sad + self.surprise + self.angry \
                        + self.disgust + self.fear
