class Product:
    """Класс товара."""

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
    ):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс категории товаров."""

    category_count = 0   # общее количество категорий
    product_count = 0    # общее количество товаров во всех категориях

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = products

        # Автоматическое заполнение атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)
