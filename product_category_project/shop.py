from __future__ import annotations


class Product:
    """Товар магазина."""

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

    # price: геттер и сеттер

    @property
    def price(self) -> int:
        return self.__price

    @price.setter
    def price(self, new_price: int) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Если цена понижается — спрашиваем подтверждение.
        if new_price < self.__price:
            answer = input("Понизить цену? y/n: ")
            if answer.lower() != "y":
                return

        self.__price = new_price

    # Класс-метод создания товара

    @classmethod
    def new_product(
        cls,
        product_data: dict,
        products: list[Product] | None = None,
    ) -> Product:
        """
        Создаёт товар из словаря.

        Если передан список ``products`` и в нём уже есть товар
        с таким же именем — суммирует количество и выбирает
        более высокую цену. Возвращает существующий объект.
        """
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
        return self.price * self.quantity + other.price * other.quantity


class Category:
    """Категория товаров."""

    product_count: int = 0

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.__products: list[Product] = []

    # Добавление товара

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        Category.product_count += 1

    # Геттер списка товаров

    @property
    def products(self) -> str:
        return "".join(f"{product}\n" for product in self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
