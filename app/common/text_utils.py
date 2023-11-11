import  string, random

class TextUtils:

    def generate_random_string(length):
        characters = string.ascii_letters + string.digits
        text = ''.join(random.choice(characters) for i in range(length))
        return text