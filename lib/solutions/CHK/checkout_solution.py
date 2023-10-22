from collections import namedtuple
from math import floor

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

    for item in items:
        if item not in AVAILABLE_ITEMS.keys():
            return -1

def _extract_price(item, amount) -> int:
    """
    Returns price for a given item in a given amount
    
    >>> _extract_price("A", 2)
    100
    """
    if item not in AVAILABLE_ITEMS.keys():
        return -1
    
    discounted_price = 0
    for offer in ALL_OFFERS:
        if item == offer.item:
            if amount >= offer.amount:
                # Divide to find out how many offers are possible
                number_offers = floor(amount / offer.amount)
                discounted_price += offer.new_price * number_offers
                amount -= number_offers * offer.amount

    return amount * AVAILABLE_ITEMS[item] + discounted_price
    
    

if __name__ == "__main__":
    checkout("A B B A A A")

