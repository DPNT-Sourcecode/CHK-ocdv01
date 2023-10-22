from collections import namedtuple, Counter
from math import floor

AVAILABLE_ITEMS = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
}

OFFERS = namedtuple("OFFERS",["item", "amount", "new_price"])

offer1 = OFFERS("A", 3, 130)
offer2 = OFFERS("B", 2, 45)
offer3 = OFFERS("A", 5, 200)

SINGLE_OFFERS = [offer3, offer2, offer1]

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

    Discount twice at whole cart level
    >>> checkout("EEEEBB")
    160

    >>> checkout("AAAAAEEBAAABB")
    455
    """
    total_price = 0
    item_counter = Counter(skus)
    
    for item in item_counter:
        if item not in AVAILABLE_ITEMS.keys():
            return -1

    item_counter = _apply_whole_cart_offers(item_counter)

    for item in item_counter:
        total_price += _extract_price(item, item_counter[item])

    return total_price
        

# Find best offer for a particular amount:
def _find_best_offer(item, total_amount):
    """
    >>> _find_best_offer("A", 5)
    OFFERS(item='A', amount=5, new_price=200)
    """
    best_offer = None
    offers = [offer for offer in SINGLE_OFFERS if offer.item == item and offer.amount < total_amount]
    
    if offers != []:
        for index, offer in enumerate(offers):
            if index == 0:
                best_offer = offer
            else:
                if (
                    offer.amount > best_offer.amount
                    ):
                    best_offer = offer
    
    return best_offer

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

	New kind of discount which is a better offer
    >>> _extract_price("A", 5)
    200

    """


    def __find_all_posible_offers(item, total_amount):
        pass

    discounted_price = 0
    if (offer := _find_best_offer(item, amount)):
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
    >>> _apply_whole_cart_offers(Counter({'E': 4, 'B': 2}))
    Counter({'E': 4, 'B': 0})

	Does not go below 0
    >>> _apply_whole_cart_offers(Counter({'E': 4, 'B': 1}))
    Counter({'E': 4, 'B': 0})
    """
    for item_in_cart in item_counter:
        for offer in WHOLE_OFFERS:
            if item_in_cart == offer.item and offer.free_item in item_counter:
                n_discounted_items = floor(item_counter[item_in_cart] / offer.amount)

                if n_discounted_items > item_counter[offer.free_item]:
                    item_counter[offer.free_item] = 0
                else:
                    item_counter[offer.free_item] -= n_discounted_items
    return item_counter

if __name__ == "__main__":
    checkout("A B B A A A")







