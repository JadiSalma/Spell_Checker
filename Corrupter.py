import re
import random

class TextCorruptor:
    def __init__(self, file_path, mistake_probability=0.1):
        self.file_path = file_path
        self.mistake_probability = mistake_probability
        self.corrupted_text = ""

    def corrupt_text(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()

            words = re.findall(r'\b\w+\b', text)
            corrupted_words = [self.introduce_mistakes(word) if random.random() < self.mistake_probability else word for word in words]

            corrupted_text = " ".join(corrupted_words)
            self.corrupted_text = corrupted_text

    def introduce_mistakes(self, word):
        if word.isalpha():  # Process only alphabetical words
            if random.random() < 0.3:  # 30% chance to introduce a mistake
                mistake_type = random.choice(['substitute', 'omit', 'add', 'case'])
                if mistake_type == 'substitute':
                    return self.substitute_letter(word)
                elif mistake_type == 'omit':
                    return self.omit_letter(word)
                elif mistake_type == 'add':
                    return self.add_letter(word)
                elif mistake_type == 'case':
                    return self.change_case(word)

        return word

    def substitute_letter(self, word):
        index = random.randint(0, len(word) - 1)
        return word[:index] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[index + 1:]

    def omit_letter(self, word):
        index = random.randint(0, len(word) - 1)
        return word[:index] + word[index + 1:]

    def add_letter(self, word):
        index = random.randint(0, len(word) - 1)
        return word[:index] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[index:]

    def change_case(self, word):
        return ''.join(random.choice([c.upper(), c.lower()]) for c in word)

    def save_corrupted_text(self, output_file_path):
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(self.corrupted_text)
