"""Тесты для product_category_project.shop."""

import pytest

from product_category_project.shop import (
    Category,
    LawnGrass,
    Product,
    Smartphone,
)


# ---------------------------------------------------------------------------
# Фикстуры и фабрики
# ---------------------------------------------------------------------------

@pytest.fixture
def reset_product_count():
    original = Category.product_count
    Category.product_count = 0
    yield
    Category.product_count = original


def make_product(name="Телефон", description="Смартфон", price=50000, quantity=5):
    return Product(name, description, price, quantity)


def make_smartphone(
    name="iPhone",
    description="Смартфон",
    price=80000,
    quantity=3,
    efficiency=9.5,
    model="15 Pro",
    memory=256,
    color="Чёрный",
):
    return Smartphone(
        name, description, price, quantity,
        efficiency=efficiency, model=model, memory=memory, color=color,
    )


def make_lawn_grass(
    name="Газон",
    description="Трава газонная",
    price=500,
    quantity=100,
    country="Россия",
    germination_period="10 дней",
    color="Зелёный",
):
    return LawnGrass(
        name, description, price, quantity,
        country=country,
        germination_period=germination_period,
        color=color,
    )


# ---------------------------------------------------------------------------
# Приватные атрибуты
# ---------------------------------------------------------------------------

def test_product_price_is_private():
    with pytest.raises(AttributeError):
        _ = make_product().__price


def test_category_products_is_private():
    with pytest.raises(AttributeError):
        _ = Category("Электроника").__products


# ---------------------------------------------------------------------------
# Category.add_product и product_count
# ---------------------------------------------------------------------------

def test_add_product_returns_none(reset_product_count):
    category = Category("Электроника")
    assert category.add_product(make_product()) is None


def test_add_product_increments_product_count(reset_product_count):
    category = Category("Электроника")
    category.add_product(make_product("Телефон"))
    category.add_product(make_product("Ноутбук"))
    assert Category.product_count == 2


def test_product_count_shared_between_instances(reset_product_count):
    a = Category("A")
    b = Category("B")
    a.add_product(make_product("Телефон"))
    b.add_product(make_product("Чайник"))
    assert Category.product_count == 2


def test_add_product_accepts_smartphone(reset_product_count):
    category = Category("Электроника")
    category.add_product(make_smartphone())
    assert Category.product_count == 1


def test_add_product_accepts_lawn_grass(reset_product_count):
    category = Category("Сад")
    category.add_product(make_lawn_grass())
    assert Category.product_count == 1


@pytest.mark.parametrize("bad_value", [42, "строка", None, 3.14, [1, 2], object()])
def test_add_product_rejects_non_product(reset_product_count, bad_value):
    category = Category("Электроника")
    with pytest.raises(TypeError):
        category.add_product(bad_value)
    assert Category.product_count == 0


# ---------------------------------------------------------------------------
# Category.products и Category.__str__
# ---------------------------------------------------------------------------

def test_products_getter_empty():
    assert Category("Электроника").products == ""


def test_products_getter_multiple_products():
    category = Category("Электроника")
    category.add_product(make_product("Телефон", price=50000, quantity=5))
    category.add_product(make_product("Ноутбук", price=100000, quantity=2))

    expected = (
        "Телефон, 50000 руб. Остаток: 5 шт.\n"
        "Ноутбук, 100000 руб. Остаток: 2 шт.\n"
    )
    assert category.products == expected


def test_products_getter_uses_product_str():
    category = Category("Электроника")
    product = make_product("Телефон", price=50000, quantity=5)
    category.add_product(product)
    assert category.products == f"{product}\n"


def test_category_str_empty():
    assert str(Category("Электроника")) == "Электроника, количество продуктов: 0 шт."


def test_category_str_sums_quantities_not_positions():
    category = Category("Электроника")
    category.add_product(make_product("Телефон", quantity=5))
    category.add_product(make_product("Ноутбук", quantity=2))
    assert str(category) == "Электроника, количество продуктов: 7 шт."


# ---------------------------------------------------------------------------
# Product.price — геттер и сеттер
# ---------------------------------------------------------------------------

def test_price_getter_returns_initial_value():
    assert make_product(price=50000).price == 50000


def test_price_setter_accepts_positive(monkeypatch):
    product = make_product(price=50000)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 55000
    assert product.price == 55000


@pytest.mark.parametrize("bad_price", [0, -1, -100])
def test_price_setter_rejects_non_positive(capsys, bad_price):
    product = make_product(price=50000)
    product.price = bad_price
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 50000


def test_price_setter_lower_price_confirmed(monkeypatch):
    product = make_product(price=50000)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 40000
    assert product.price == 40000


def test_price_setter_lower_price_declined(monkeypatch):
    product = make_product(price=50000)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    product.price = 40000
    assert product.price == 50000


def test_price_setter_equal_price_no_prompt(monkeypatch):
    product = make_product(price=50000)

    def fail_input(_):
        raise AssertionError("input не должен вызываться при равной цене")

    monkeypatch.setattr("builtins.input", fail_input)
    product.price = 50000
    assert product.price == 50000


# ---------------------------------------------------------------------------
# Product.new_product
# ---------------------------------------------------------------------------

def test_new_product_creates_instance():
    data = {
        "name": "Телефон", "description": "Смартфон",
        "price": 50000, "quantity": 5,
    }
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert (product.name, product.description, product.price, product.quantity) == (
        "Телефон", "Смартфон", 50000, 5,
    )


def test_new_product_merges_duplicate():
    existing = make_product("Телефон", price=50000, quantity=5)
    data = {
        "name": "Телефон", "description": "Смартфон",
        "price": 60000, "quantity": 3,
    }
    result = Product.new_product(data, [existing])
    assert result is existing
    assert existing.quantity == 8
    assert existing.price == 60000


def test_new_product_keeps_higher_price_on_duplicate(monkeypatch):
    existing = make_product("Телефон", price=70000, quantity=5)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    data = {
        "name": "Телефон", "description": "Смартфон",
        "price": 60000, "quantity": 3,
    }
    result = Product.new_product(data, [existing])
    assert result is existing
    assert existing.quantity == 8
    assert existing.price == 70000


def test_new_product_no_duplicate_adds_new():
    existing = make_product("Телефон")
    data = {
        "name": "Ноутбук", "description": "Игровой",
        "price": 100000, "quantity": 2,
    }
    result = Product.new_product(data, [existing])
    assert result is not existing
    assert result.name == "Ноутбук"
    assert existing.quantity == 5


# ---------------------------------------------------------------------------
# Product.__str__
# ---------------------------------------------------------------------------

def test_product_str():
    product = make_product("Телефон", price=80, quantity=15)
    assert str(product) == "Телефон, 80 руб. Остаток: 15 шт."


def test_product_str_reflects_current_price():
    product = make_product("Телефон", price=80, quantity=15)
    product.price = 100
    assert str(product) == "Телефон, 100 руб. Остаток: 15 шт."


# ---------------------------------------------------------------------------
# Наследники: поля
# ---------------------------------------------------------------------------

def test_smartphone_is_product_subclass():
    assert issubclass(Smartphone, Product)


def test_lawn_grass_is_product_subclass():
    assert issubclass(LawnGrass, Product)


def test_smartphone_extra_attributes():
    phone = make_smartphone(efficiency=9.5, model="15 Pro", memory=256, color="Чёрный")
    assert phone.efficiency == 9.5
    assert phone.model == "15 Pro"
    assert phone.memory == 256
    assert phone.color == "Чёрный"


def test_smartphone_inherits_base_attributes():
    phone = make_smartphone(name="iPhone", price=80000, quantity=3)
    assert phone.name == "iPhone"
    assert phone.price == 80000
    assert phone.quantity == 3


def test_lawn_grass_extra_attributes():
    grass = make_lawn_grass(
        country="Россия", germination_period="10 дней", color="Зелёный"
    )
    assert grass.country == "Россия"
    assert grass.germination_period == "10 дней"
    assert grass.color == "Зелёный"


def test_lawn_grass_inherits_base_attributes():
    grass = make_lawn_grass(name="Газон", price=500, quantity=100)
    assert grass.name == "Газон"
    assert grass.price == 500
    assert grass.quantity == 100


# ---------------------------------------------------------------------------
# Product.__add__ — базовая арифметика и ограничения по типу
# ---------------------------------------------------------------------------

def test_product_add():
    a = Product("A", "o", 100, 10)
    b = Product("B", "o", 200, 2)
    assert a + b == 1400


def test_product_add_is_commutative():
    a = Product("A", "o", 100, 10)
    b = Product("B", "o", 200, 2)
    assert a + b == b + a == 1400


def test_product_add_returns_int():
    a = Product("A", "o", 100, 10)
    b = Product("B", "o", 200, 2)
    assert isinstance(a + b, int)


def test_product_add_zero_quantity():
    a = Product("A", "o", 100, 0)
    b = Product("B", "o", 200, 3)
    assert a + b == 600


def test_product_add_with_itself():
    a = Product("A", "o", 100, 10)
    assert a + a == 1000


def test_smartphone_add_smartphone():
    a = make_smartphone(price=80000, quantity=3)
    b = make_smartphone(name="Samsung", price=60000, quantity=2)
    assert a + b == 80000 * 3 + 60000 * 2


def test_lawn_grass_add_lawn_grass():
    a = make_lawn_grass(price=500, quantity=100)
    b = make_lawn_grass(name="Газон 2", price=700, quantity=50)
    assert a + b == 500 * 100 + 700 * 50


def test_smartphone_plus_lawn_grass_raises():
    phone = make_smartphone()
    grass = make_lawn_grass()
    with pytest.raises(TypeError):
        _ = phone + grass


def test_lawn_grass_plus_smartphone_raises():
    phone = make_smartphone()
    grass = make_lawn_grass()
    with pytest.raises(TypeError):
        _ = grass + phone


def test_product_plus_smartphone_raises():
    product = make_product()
    phone = make_smartphone()
    with pytest.raises(TypeError):
        _ = product + phone


def test_smartphone_plus_product_raises():
    product = make_product()
    phone = make_smartphone()
    with pytest.raises(TypeError):
        _ = phone + product


def test_product_plus_lawn_grass_raises():
    product = make_product()
    grass = make_lawn_grass()
    with pytest.raises(TypeError):
        _ = product + grass


# ---------------------------------------------------------------------------
# Интеграционный сценарий
# ---------------------------------------------------------------------------

def test_full_scenario(reset_product_count):
    category = Category("Электроника")
    phone = make_smartphone(price=80000, quantity=3)
    laptop = Product("Ноутбук", "Игровой", 100000, 2)

    category.add_product(phone)
    category.add_product(laptop)

    assert Category.product_count == 2
    assert str(category) == "Электроника, количество продуктов: 5 шт."
    assert "iPhone, 80000 руб. Остаток: 3 шт." in category.products
    assert "Ноутбук, 100000 руб. Остаток: 2 шт." in category.products
    assert phone + phone == 80000 * 3 * 2
