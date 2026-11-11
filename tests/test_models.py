import pytest
from product_category_project.models import Product, Category


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасывает счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_init():
    product = Product("Телефон", "Смартфон", 50000.0, 10)
    assert product.name == "Телефон"
    assert product.description == "Смартфон"
    assert product.price == 50000.0
    assert product.quantity == 10


def test_category_init():
    products = [
        Product("Товар 1", "Описание 1", 100.0, 5),
        Product("Товар 2", "Описание 2", 200.0, 3),
    ]
    category = Category("Электроника", "Разные товары", products)

    assert category.name == "Электроника"
    assert category.description == "Разные товары"
    assert category.products == products


def test_category_count():
    Category("Категория 1", "Описание", [])
    Category("Категория 2", "Описание", [])
    Category("Категория 3", "Описание", [])

    assert Category.category_count == 3


def test_product_count():
    products_1 = [
        Product("Товар 1", "Описание", 100.0, 1),
        Product("Товар 2", "Описание", 200.0, 2),
    ]
    products_2 = [
        Product("Товар 3", "Описание", 300.0, 3),
    ]

    Category("Категория 1", "Описание", products_1)
    Category("Категория 2", "Описание", products_2)

    # 2 товара в первой категории + 1 во второй = 3
    assert Category.product_count == 3
