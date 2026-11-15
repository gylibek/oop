class Product:
    def __init__(self, name: str, description: str, price: int, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price: int):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Дополнительное задание к заданию 4:
        # если цена понижается, спрашиваем подтверждение.
        if new_price < self.__price:
            answer = input("Понизить цену? y/n: ")
            if answer.lower() != "y":
                return

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, products: list | None = None):
        """
        Создаёт товар из словаря.
        Дополнительно: если передан список products и в нём есть товар
        с таким же именем, суммирует количество и выбирает большую цену.
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

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

class Category:
    product_count: int = 0

    def __init__(self, name: str):
            self.name = name
            self.__products: list[Product] = []

    def add_product(self, product: Product):
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        result = ""
        for product in self.__products:
            result += (
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт.\n"
            )
        return result
