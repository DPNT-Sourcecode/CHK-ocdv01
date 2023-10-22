from collections import namedtuple

AVAILABLE_ITEMS = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15
}

OFFERS = namedtuple("OFFERS",["item", "amount", "new_price"])

offer1 = OFFERS("A", 3, 130)
offer2 = OFFERS("B", 2, 45)

ALL_OFFERS = [offer1, offer2]

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    print(skus)
    items = skus.split(" ")


if __name__ == "__main__":
    checkout("A B B A A A")

