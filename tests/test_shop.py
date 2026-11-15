import pytest

from product_category_project.shop import Product, Category


# ---------- __str__ Product ----------

def test_product_str():
    product = Product("Телефон", "Смартфон", 80, 15)
    assert str(product) == "Телефон, 80 руб. Остаток: 15 шт."


# ---------- __str__ Category ----------

def test_category_str_empty():
    category = Category("Электроника")
    assert str(category) == "Электроника, количество продуктов: 0 шт."


def test_category_str_with_products():
    category = Category("Электроника")
    category.add_product(Product("Телефон", "Смартфон", 50000, 5))
    category.add_product(Product("Ноутбук", "Игровой", 100000, 2))

    assert str(category) == "Электроника, количество продуктов: 7 шт."


# ---------- products getter использует str(Product) ----------

def test_category_products_getter_uses_product_str():
    category = Category("Электроника")
    category.add_product(Product("Телефон", "Смартфон", 50000, 5))
    category.add_product(Product("Ноутбук", "Игровой", 100000, 2))

    expected = (
        "Телефон, 50000 руб. Остаток: 5 шт.\n"
        "Ноутбук, 100000 руб. Остаток: 2 шт.\n"
    )
    assert category.products == expected


# ---------- __add__ Product ----------

def test_product_add():
    a = Product("Товар A", "Описание", 100, 10)
    b = Product("Товар B", "Описание", 200, 2)

    # 100 * 10 + 200 * 2 = 1400
    assert a + b == 1400
    assert b + a == 1400


def test_product_add_zero_quantity():
    a = Product("Товар A", "Описание", 100, 0)
    b = Product("Товар B", "Описание", 200, 3)

    assert a + b == 600


def test_product_add_returns_int():
    a = Product("Товар A", "Описание", 100, 10)
    b = Product("Товар B", "Описание", 200, 2)

    result = a + b
    assert isinstance(result, int)
    assert result == 1400
