import random
import string

class PasswordService:
    @staticmethod
    def generate_password(length=12):
        """
        Генерирует надежный пароль с заданной длиной.
        
        Args:
            length (int): Длина пароля (по умолчанию 12).
        
        Returns:
            str: Сгенерированный пароль.
        """
        if length < 12:  # Минимальная длина для выполнения всех условий
            length = 12

        # Наборы символов
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        special = "!."

        # Гарантируем, что пароль будет содержать хотя бы один символ из каждого набора
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(special)
        ]

        # Заполняем оставшуюся длину случайными символами из всех наборов
        all_characters = lower + upper + digits + special
        password += random.choices(all_characters, k=length - len(password))

        # Перемешиваем символы в пароле
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def check_password_strength(password):
        """
        Проверяет стойкость сгенерированного пароля.
        
        Args:
            password (str): Пароль для проверки.
        
        Returns:
            dict: Результаты проверки стойкости пароля.
        """
        strength = {
            'length': len(password) >= 12,
            'lowercase': any(c.islower() for c in password),
            'uppercase': any(c.isupper() for c in password),
            'digit': any(c.isdigit() for c in password),
            'special_char': any(c in "!." for c in password)
        }
        
        strength['overall'] = all(strength.values())
        return strength