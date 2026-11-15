# Product Category Project

Реализованы классы `Product` и `Category`.

- `Product` хранит название, описание, цену и количество.
- `Category` хранит название, описание и список товаров.
- В `Category` добавлены атрибуты класса `category_count` и `product_count`,
  которые автоматически увеличиваются при создании новых категорий и товаров.
- приватные атрибуты Product.__price и Category.__products;
- Category.add_product() и класс-атрибут Category.product_count;
- геттер Category.products;
- геттер и сеттер Product.price (с подтверждением понижения);
- класс-метод Product.new_product() с объединением дубликатов;
- Product.__str__, Category.__str__;
- Product.__add__ — полная стоимость двух товаров на складе.
