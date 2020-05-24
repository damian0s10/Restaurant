import datetime

from experta import KnowledgeEngine, DefFacts, Fact, Field, Rule, MATCH, AS, TEST, NOT


class Recipe(Fact):
    name = Field(str, mandatory=True)
    price = Field(float, mandatory=True)
    category = Field(str, mandatory=True)
    size = Field(int, default=2)
    count = Field(int, default=1)


class TotalPrice(Fact):
    total_price = Field(float, default=0.0)


class Product(Fact):
    name = Field(str, mandatory=True)
    price = Field(float, mandatory=True)
    category = Field(str, mandatory=True)
    size = Field(int, default=2)
    count = Field(int, default=1)


class ProductDiscount(KnowledgeEngine):
    DISCOUNT_TWO_PIZZAS_ONE_PRICE = 'znizka.dwie_duze_w_cenie_jednej'
    DISCOUNT_FREE_DELIVERY = 'znizka.dostawa'
    DISCOUNT_FREE_COLA = 'znizka.darmowa_cola'
    DISCOUNT_SALAD_20_PERCENT = 'znizka.saladka_20_procent_taniej'
    DISCOUNT_PIZZA_15_PERCENT = 'znizka.pizza_duza_15_procent_taniej'

    def __init__(self, product_list):
        super(ProductDiscount, self).__init__()
        self.product_list = product_list

    @DefFacts()
    def startup(self):
        yield Product(name='Koszt dostawy', price=10.0, category='dostawa')

        for product in self.product_list:
            yield Product(name=product['name'], price=product['price'], category=product['category'],
                          size=product['size'])

    @Rule()
    def default_values(self):
        self.declare(TotalPrice(total_price=0.0))

    @Rule(AS.product << Product(name=MATCH.name, price=MATCH.price, category=MATCH.category, size=MATCH.size),
          AS.sum_price << TotalPrice(total_price=MATCH.total_price))
    def add_to_recipe(self, product, name, price, category, size, sum_price, total_price):
        self.retract(product)
        self.declare(Recipe(name=name, price=price, category=category, size=size))
        self.modify(sum_price, total_price=total_price + price)

    @Rule(NOT(Recipe(category=DISCOUNT_TWO_PIZZAS_ONE_PRICE)),
          Recipe(price=MATCH.price1, category='pizza', size=2),
          Recipe(price=MATCH.price2, category='pizza', size=2))
    def two_big_pizzas_one_price(self, price1, price2):
        """
        2 duże pizze w cenie 1 (tej droższej)
        :param price1:
        :param price2:
        :return:
        """
        price = price1 if price1 < price2 else price2
        self.declare(Product(name='Promocja 2 duze pizze w cenie 1 drozszej', price=-price,
                             category=ProductDiscount.DISCOUNT_TWO_PIZZAS_ONE_PRICE))

    @Rule(NOT(Recipe(category=DISCOUNT_FREE_COLA)),
          Recipe(category='pizza'))
    def free_cola(self):
        """
        Cola 0.5l gratis przy zamowienie pizzy.
        :return:
        """
        self.declare(Product(name='Darmowa cola 0.5l przy zamowieniu pizzy', price=0.0,
                             category=ProductDiscount.DISCOUNT_FREE_COLA))

    @Rule(NOT(Recipe(category=DISCOUNT_FREE_DELIVERY)),
          AS.sum_price << TotalPrice(total_price=MATCH.total_price),
          TEST(lambda total_price: total_price >= 50.0))
    def apply_free_delivery(self, sum_price):
        """
        Zamówienie powyżej 50 zł - darmowa dostawa
        :param sum_price:
        :return:
        """
        self.declare(Product(name='Zamowienie powyzej 50 zl (Darmowa dostawa)', price=-10.0,
                             category=ProductDiscount.DISCOUNT_FREE_DELIVERY))
        self.modify(sum_price)

    @Rule(Recipe(price=MATCH.price, category='salatka'),
          TEST(lambda _: datetime.datetime.today().weekday() == 1))
    def discount_salad(self, price):
        """
        Wtorek zniżka na sałatki 20%
        :param price:
        :return:
        """
        self.declare(Product(name='Wtorek znizka na salatki 20%', price=-(price * 0.2),
                             category=ProductDiscount.DISCOUNT_SALAD_20_PERCENT))

    @Rule(Recipe(price=MATCH.price, category='pizza', size=2),
          TEST(lambda _: datetime.datetime.today().weekday() == 5))
    def discount_big_pizza(self, price):
        """
        Sobota kazda pizza duża -15%
        :param price:
        :return:
        """
        self.declare(Product(name='Sobota znizka na duza pizze 15%', price=-(price * 0.2),
                             category=ProductDiscount.DISCOUNT_PIZZA_15_PERCENT))


# TODO 1. Kody rabatowe ( np. x% znizki na zamowienie, darmowa dostawa, sprawdzenie czy łącza się z innymi promocjami)
# TODO 2. Środa do zamowienia z oferty sniadaniowej do godziny 12, kawa gratis.
# TODO 3. Czwartek od godz 20 alkohol -20%.
# TODO 4. Piątek makarony -15%.
# TODO 5. Piątek w godz 16-20, 3 piwa w cenie 2.
# TODO 6. Sobota i niedziela desery -10%.
# TODO 7. Niedziela w zestawie dowolne danie i napojem, -15% na zestaw
# TODO 8. Od poniedziału do czwartku do każdej pizzy 2 sosy gratis.


if __name__ == '__main__':
    # TODO dummy data, can be removed later
    products = [
        {'name': 'duza pizza', 'price': 12.5, 'category': 'pizza', 'size': 2},
        {'name': 'duza pizza2', 'price': 32.5, 'category': 'pizza', 'size': 2},
        {'name': 'duza pizza3', 'price': 12.5, 'category': 'pizza', 'size': 1},
        {'name': 'duza pizza4', 'price': 12.5, 'category': 'pizza', 'size': 1},
        {'name': 'duza pizza5', 'price': 12.5, 'category': 'pizza', 'size': 2},
        {'name': 'duza pizza6', 'price': 12.5, 'category': 'pizza', 'size': 2},
        {'name': 'Salatka 1', 'price': 15.0, 'category': 'salatka', 'size': 2},
    ]

    product_discount = ProductDiscount(products)
    product_discount.reset()
    product_discount.run()
    print(product_discount.facts)
