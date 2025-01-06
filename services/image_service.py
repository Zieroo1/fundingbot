from PIL import Image, ImageDraw, ImageFont
from config import BACKGROUND_PATHS, FONT_PATH, CRYPTO_LIST

class ImageService:
    @staticmethod
    def create_image(rates):
        """
        Создает изображение с текущими рыночными данными криптовалют.
        
        Args:
            rates (dict): Словарь с курсами криптовалют.
        
        Returns:
            str: Путь к сгенерированному изображению.
        """
        if not rates:
            print("Нет данных для создания изображения.")
            return None

        # Убираем монеты, для которых нет данных
        valid_rates = {
            coin: data for coin, data in rates.items() 
            if isinstance(data, dict) and 'change_24h' in data and coin in CRYPTO_LIST
        }

        if not valid_rates:
            print("Нет данных о изменениях за 24 часа.")
            return None

        # Определяем монету с наибольшим изменением за 24 часа
        max_change_coin = max(valid_rates, key=lambda coin: valid_rates[coin]['change_24h'])

        try:
            background = Image.open(BACKGROUND_PATHS[max_change_coin])
            width, height = background.size
        except Exception as e:
            print(f"Ошибка при загрузке фона: {e}")
            return None

        image = background.copy()
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(FONT_PATH, 20)
        except IOError:
            font = ImageFont.load_default()
            print("Шрифт не найден, используется стандартный шрифт.")

        # Функция для выбора цвета текста в зависимости от изменения курса
        def get_text_color(change_24h):
            return "#ccffd1" if change_24h >= 0 else "#ffcccc"

        # Начальная позиция текста
        y_offset = 5

        draw.text((10, y_offset), "Market Stats:", fill="white", font=font)
        y_offset += 30

        # Добавляем данные по каждой монете с цветом
        for coin in CRYPTO_LIST:
            coin_price = f"${rates[coin]['price']:.2f}"
            coin_change = f"({rates[coin]['change_24h']:+.2f}%)"
            color = get_text_color(rates[coin]['change_24h'])

            draw.text((20, y_offset), f"{coin}: {coin_price} {coin_change}", fill=color, font=font)
            y_offset += 30

        image_path = 'crypto_rates.png'
        image.save(image_path)
        return image_path