"""
Модуль магазина: базовый класс Product, наследники Smartphone и LawnGrass,
класс Category.

Реализовано:
- приватные атрибуты Product.__price и Category.__products;
- Category.add_product() с проверкой isinstance и класс-атрибут product_count;
- геттер Category.products;
- геттер и сеттер Product.price (с подтверждением понижения);
- класс-метод Product.new_product() с объединением дубликатов;
- Product.__str__, Category.__str__;
- Product.__add__ с ограничением: только объекты одного класса;
- классы-наследники Smartphone и LawnGrass.
"""

from __future__ import annotations


class Product:
    """Базовый товар магазина."""

    def __init__(
        self,
        name: str,
        description: str,
        price: int,
        quantity: int,
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.__price: int = price
        self.quantity: int = quantity

    @property
    def price(self) -> int:
        return self.__price

    @price.setter
    def price(self, new_price: int) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input("Понизить цену? y/n: ")
            if answer.lower() != "y":
                return

        self.__price = new_price

    @classmethod
    def new_product(
        cls,
        product_data: dict,
        products: list[Product] | None = None,
    ) -> Product:
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if products is not None:
            for product in products:
                if product.name == name:
                    product.quantity += quantity
                    if price > product.price:
                        product.price = price
                    return product

        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Product) -> int:
        # Задание 2: складывать можно только товары одного класса.
        if type(self) is not type(other):
            raise TypeError(
                "Складывать можно только товары одного и того же класса"
            )
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Смартфон — наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: int,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency: float = efficiency
        self.model: str = model
        self.memory: int = memory
        self.color: str = color


class LawnGrass(Product):
    """Трава газонная — наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: int,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country: str = country
        self.germination_period: str = germination_period
        self.color: str = color


class Category:
    """Категория товаров."""

    product_count: int = 0

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        # Задание 3: добавлять можно только Product и его наследников.
        if not isinstance(product, Product):
            raise TypeError(
                "В категорию можно добавлять только объекты Product "
                "и его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "".join(f"{product}\n" for product in self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
