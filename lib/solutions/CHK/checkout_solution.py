from collections import namedtuple, Counter
from math import floor

AVAILABLE_ITEMS = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
}

OFFERS = namedtuple("OFFERS",["item", "amount", "new_price", "free_item"])

offer1 = OFFERS("A", 3, 130, None)
offer2 = OFFERS("B", 2, 45, None)

SINGLE_OFFERS = [offer1, offer2]

WHOLE_CART_OFFERS = namedtuple("WCOFFERS",["item", "amount", "free_item"])
offer3 = WHOLE_CART_OFFERS("E", 2, "B")
WHOLE_OFFERS = [offer3]


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    """
    Perform checkout

    >>> checkout("AABA")
    160

    Should break
    >>> checkout("ABCa")
    -1

    Offers from whole cart work
    >>> checkout("EEB")
    80

    # Discount twice at whole cart level
    # >>> checkout("EEEEBB")
    # 160
    """
    total_price = 0
    item_counter = Counter(skus)
    item_counter = _apply_whole_cart_offers(item_counter)

    try:
        for item in item_counter:
            for offer in WHOLE_OFFERS:
                if item == offer.item and offer.free_item in item_counter:
                    # depending on how many
                    pass
                

            total_price += _extract_price(item, item_counter[item])

        return total_price
    except ValueError:
        return -1
        

def _extract_price(item, amount) -> int:
    """
    Returns price for a given item in a given amount
    
    Some random item is correct
    >>> _extract_price("A", 2)
    100

    Offers work
    >>> _extract_price("A", 3)
    130

    Offers with remainders work
    >>> _extract_price("A", 4)
    180

    """
    if item not in AVAILABLE_ITEMS.keys():
        raise ValueError("Item not available, breaking cart")
    
    discounted_price = 0
    for offer in SINGLE_OFFERS:
        if item == offer.item:
            if amount >= offer.amount:
                # Divide to find out how many offers are possible
                number_offers = floor(amount / offer.amount)
                discounted_price += offer.new_price * number_offers
                amount -= number_offers * offer.amount

    return amount * AVAILABLE_ITEMS[item] + discounted_price
    
    
def _apply_whole_cart_offers(item_counter) -> Counter:
    """
    Offer can work N times
    _apply_whole_cart_offers(Counter({'E': 4, 'B': 2}))
    """
    for item_in_cart in item_counter:
        for offer in WHOLE_OFFERS:
            if item_in_cart == offer.item and offer.free_item in item_counter:
                breakpoint()
                n_discounted_items = floor(item_counter[item_in_cart] / offer.amount)
                item_counter[offer.free_item] -= n_discounted_items
    return item_counter

if __name__ == "__main__":
    checkout("A B B A A A")



