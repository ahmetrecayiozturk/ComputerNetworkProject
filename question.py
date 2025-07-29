class Question:
    def __init__(self, question, options, correct_answer, joker_type_s, joker_type_y):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.joker_type_s = joker_type_s
        self.joker_type_y = joker_type_y

    def __str__(self):
        return f"Soru: {self.question}\nSeçenekler: {self.options}\nDoğru Cevap: {self.correct_answer}"
