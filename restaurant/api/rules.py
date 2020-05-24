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
    DISCOUNT_BURGER_15_PERCET = 'znizka.burger_15_procent_taniej'
    DISCOUNT_FREE_COFFEA = 'znizka.darmowa_kawa'
    DISCOUNT_ALKOHOL_20_PERCENT = 'znizka.alkohol_20_procent_taniej'
    DISCOUNT_FREE_SAUCE = 'znizka.sos_gratis'
    DISCOUNT_DESSERT_10_PERCENT = 'znizka.deser_10_procent_taniej'
    DISCOUNT_BEER_ONE_FREE = 'znizka.dwa_piwa_trzecie_gratis'
    DISCOUNT_BURGER_AND_DRING_15_PERCENT = 'znizka.burger_z_napojem_15_procent_taniej'

    PACKAGE_SMALL_PIZZA = 'opakowanie.mala_pizza'
    PACKAGE_BIG_PIZZA = 'opakowanie.duza_pizza'

    def __init__(self, product_list):
        super(ProductDiscount, self).__init__()
        self.product_list = product_list

    @DefFacts()
    def startup(self):
        yield Product(name='Koszt dostawy', price=10.0, category='dostawa')

        for product in self.product_list:
            yield Product(name=product['name'], price=product['price'], category=product['category'],
                          size=product['size'], count=product['count'])

    @Rule()
    def default_values(self):
        self.declare(TotalPrice(total_price=0.0))

    @Rule(AS.product << Product(name=MATCH.name, price=MATCH.price, category=MATCH.category, size=MATCH.size, count=MATCH.count),
          AS.sum_price << TotalPrice(total_price=MATCH.total_price))
    def add_to_recipe(self, product, name, price, category, size, count, sum_price, total_price):
        self.retract(product)
        self.declare(Recipe(name=name, price=price, category=category, size=size ,count=count))
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

    @Rule(Recipe(price=MATCH.price, category='burgery'),
          TEST(lambda _: datetime.datetime.today().weekday() == 2))
    def discount_burger(self, price):
        """
        Środa zniżka na burgery -15%
        :param price:
        :return:
        """
        self.declare(Product(name='Sroda znizka na burgery 15%', price=-(price * 0.15),
                             category=ProductDiscount.DISCOUNT_BURGER_15_PERCET))

    @Rule(Recipe(price=MATCH.price, category='sniadanie'),
          TEST(lambda _: datetime.datetime.today().weekday() == 2 and datetime.datetime.today().hour < 13))
    def free_coffea(self):
        """
        Środa darmowa kawa przy zamówieniu oferty śniadaniowej, do godziny 13
        :return:
        """
        self.declare(Product(name='Środa darmowa kawa przy zamówieniu oferty śniadaniowej', price=0.0,
                             category=ProductDiscount.DISCOUNT_FREE_COFFEA))

    @Rule(Recipe(price=MATCH.price, category='alkohol'),
          TEST(lambda _: datetime.datetime.today().weekday() == 3 and datetime.datetime.today().hour >= 20))
    def discount_alkohol(self, price):
        """
        Czwartek od godz. 20 alkohol - 20%
        :param price:
        :return:
        """
        self.declare(Product(name='Czwartek zniżka na alkohol 20%', price=-(price * 0.2),
                             category=ProductDiscount.DISCOUNT_ALKOHOL_20_PERCENT))

    @Rule(Recipe(category='pizza', size=MATCH.size))
    def add_package(self, size):
        """
        Dodanie opakowanie do każdej pizzy
        :param size:
        :return:
        """
        if size == 1:
            self.declare(Product(name='Małe opakowanie do pizza', price=1.0,
                                category=ProductDiscount.PACKAGE_SMALL_PIZZA))
        else:
            self.declare(Product(name='Duże opakowanie do pizza', price=1.5,
                                category=ProductDiscount.PACKAGE_BIG_PIZZA))

    @Rule(Recipe(category='pizza'),
          TEST(lambda _: 0 < datetime.datetime.today().weekday() <= 3))
    def free_sauce(self):
        """
        Sos gratis do każdej pizzy (od poniedziałku do czwartku)
        :return:
        """
        self.declare(Product(name='Sos gratis', price=0.0,
                             category=ProductDiscount.DISCOUNT_FREE_SAUCE))

    @Rule(Recipe(price=MATCH.price, category='desery'),
          TEST(lambda _: datetime.datetime.today().weekday() == 6))
    def discount_desserts(self, price):
        """
        Niedziela znizka na desery 10%
        :param price:
        :return:
        """
        self.declare(Product(name='Niedziela zniżka na desery 10%', price=-(price * 0.1),
                             category=ProductDiscount.DISCOUNT_DESSERT_10_PERCENT))

    
    @Rule(NOT(Recipe(category=DISCOUNT_BEER_ONE_FREE)),
          Recipe(name=MATCH.name, category='alkohol', count=MATCH.count),
          TEST(lambda _: datetime.datetime.today().weekday() == 4 and 16 <= datetime.datetime.today().hour < 20))
    def free_beer(self,name,count):
        """
        Piątek w godz 16-20, 3 takie same piwa w cenie 2
        :param name:
        :param count:
        :return:
        """
        for _ in range(count//2):
            self.declare(Product(name='Piątek w godz. 16-20 darmowe piwo ' + name, price=0.0,
                                 category=ProductDiscount.DISCOUNT_BEER_ONE_FREE))


    @Rule(Recipe(category='burgery', price=MATCH.price1),
          Recipe(category='napoje', price=MATCH.price2),
          TEST(lambda _: datetime.datetime.today().weekday() == 6))
    def discount_set_burger_drink(self,price1,price2):
        """
        Niedziela w bruger i napój w zestawie taniej o 15%
        :param price1
        :param price2
        :return:
        """
        self.declare(Product(name='Niedziela zniżka na burger i napój w zestawie', price=round(-((price1+price2)*0.15),2),
                                 category=ProductDiscount.DISCOUNT_BURGER_AND_DRING_15_PERCENT))

# TODO 1. Kody rabatowe ( np. x% znizki na zamowienie, darmowa dostawa, sprawdzenie czy łącza się z innymi promocjami)




if __name__ == '__main__':
    # TODO dummy data, can be removed later
    products = [
        {'name': 'duza pizza', 'price': 12.5, 'category': 'pizza', 'size': 2, 'count': 1},
        {'name': 'duza pizza2', 'price': 32.5, 'category': 'pizza', 'size': 2, 'count': 1},
        {'name': 'duza pizza3', 'price': 12.5, 'category': 'pizza', 'size': 1, 'count': 1},
        {'name': 'duza pizza4', 'price': 12.5, 'category': 'pizza', 'size': 1, 'count': 1},
        {'name': 'duza pizza5', 'price': 12.5, 'category': 'pizza', 'size': 2, 'count': 1},
        {'name': 'duza pizza6', 'price': 12.5, 'category': 'pizza', 'size': 2, 'count': 1},
        {'name': 'Salatka 1', 'price': 15.0, 'category': 'salatka', 'size': 2, 'count': 1},
        {'name': 'Salatka 1', 'price': 15.0, 'category': 'salatka', 'size': 2, 'count': 1},
        {'name': 'Burger 1', 'price': 19.0, 'category': 'burgery', 'size': 2, 'count': 1},
        {'name': 'Jajecznica', 'price': 12.0, 'category': 'sniadanie', 'size': 2, 'count': 1},
        {'name': 'Nalesniki', 'price': 13.0, 'category': 'sniadanie', 'size': 2, 'count': 1},
        {'name': 'Piwo', 'price': 6.50, 'category': 'alkohol', 'size': 2, 'count': 1},
        {'name': 'Piwo2', 'price': 6.50, 'category': 'alkohol', 'size': 2, 'count': 1},
        {'name': 'Piwo3', 'price': 6.50, 'category': 'alkohol', 'size': 2, 'count': 1},
        {'name': 'Lody', 'price': 9.00, 'category': 'desery', 'size': 2, 'count': 1},
        {'name': 'Piwo4', 'price': 6.70, 'category': 'alkohol', 'size': 2, 'count': 5},
        {'name': 'Sok', 'price': 4.00, 'category': 'napoje', 'size': 2, 'count': 1},
        

    ]

    product_discount = ProductDiscount(products)
    product_discount.reset()
    product_discount.run()
    print(product_discount.facts)
