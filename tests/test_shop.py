import pytest
from product_category_project.shop import Product, Category


def test_category_add_product_and_counter():
    category = Category("Электроника")
    product = Product("Телефон", "Смартфон", 50000, 5)

    before = Category.product_count
    result = category.add_product(product)

    assert result is None
    assert Category.product_count == before + 1
    assert category.products == "Телефон, 50000 руб. Остаток: 5 шт.\n"


def test_category_products_private():
    category = Category("Электроника")

    with pytest.raises(AttributeError):
        category.__products


def test_category_products_getter_multiple_products():
    category = Category("Электроника")
    category.add_product(Product("Телефон", "Смартфон", 50000, 5))
    category.add_product(Product("Ноутбук", "Игровой", 100000, 2))

    expected = (
        "Телефон, 50000 руб. Остаток: 5 шт.\n"
        "Ноутбук, 100000 руб. Остаток: 2 шт.\n"
    )
    assert category.products == expected


def test_product_price_getter_and_setter():
    product = Product("Телефон", "Смартфон", 50000, 5)

    assert product.price == 50000

    product.price = 55000
    assert product.price == 55000


def test_product_price_setter_rejects_non_positive(capsys):
    product = Product("Телефон", "Смартфон", 50000, 5)

    product.price = 0
    captured = capsys.readouterr()

    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 50000


def test_product_price_setter_lower_price_confirmation(monkeypatch):
    product = Product("Телефон", "Смартфон", 50000, 5)

    monkeypatch.setattr("builtins.input", lambda _: "n")
    product.price = 40000
    assert product.price == 50000

    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 40000
    assert product.price == 40000


def test_new_product_creates_product():
    data = {
        "name": "Телефон",
        "description": "Смартфон",
        "price": 50000,
        "quantity": 5,
    }

    product = Product.new_product(data)

    assert isinstance(product, Product)
    assert product.name == "Телефон"
    assert product.description == "Смартфон"
    assert product.price == 50000
    assert product.quantity == 5


def test_new_product_merges_duplicate():
    old_product = Product("Телефон", "Смартфон", 50000, 5)
    products = [old_product]

    data = {
        "name": "Телефон",
        "description": "Новый смартфон",
        "price": 60000,
        "quantity": 3,
    }

    result = Product.new_product(data, products)

    assert result is old_product
    assert old_product.quantity == 8
    assert old_product.price == 60000


def test_new_product_keeps_higher_price_on_duplicate():
    old_product = Product("Телефон", "Смартфон", 70000, 5)
    products = [old_product]

    data = {
        "name": "Телефон",
        "description": "Новый смартфон",
        "price": 60000,
        "quantity": 3,
    }

    result = Product.new_product(data, products)

    assert result is old_product
    assert old_product.quantity == 8
    assert old_product.price == 70000
