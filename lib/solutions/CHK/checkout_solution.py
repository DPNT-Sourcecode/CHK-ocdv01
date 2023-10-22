from collections import namedtuple, Counter
from typing import Tuple
from math import floor

AVAILABLE_ITEMS = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
    "F": 10,
    "G": 20,
    "H": 10,
    "I": 35,
    "J": 60,
    "K": 70,
    "L": 90,
    "M": 15,
    "N": 40,
    "O": 10,
    "P": 50,
    "Q": 30,
    "R": 50,
    "S": 30,
    "T": 20,
    "U": 40,
    "V": 50,
    "W": 20,
    "X": 17,
    "Y": 20,
    "Z": 21,

}

OFFERS = namedtuple("OFFERS",["item", "amount", "new_price"])

offer1 = OFFERS("A", 3, 130)
offer3 = OFFERS("A", 5, 200)

offer2 = OFFERS("B", 2, 45)

offerh = OFFERS("H", 5, 45)
offerh2 = OFFERS("H", 10, 80)

offerk = OFFERS("K", 2, 120)

offerp = OFFERS("P", 5, 200)

offerq = OFFERS("Q", 3, 80)

offerv = OFFERS("V", 2, 90)
offerv2 = OFFERS("V", 3, 130)


WHOLE_CART_OFFERS = namedtuple("WCOFFERS",["item", "amount", "free_item"])
offer4 = WHOLE_CART_OFFERS("E", 2, "B")
offer5 = WHOLE_CART_OFFERS("F", 2, "F")
offern = WHOLE_CART_OFFERS("N", 3, "M")
offerr = WHOLE_CART_OFFERS("R", 3, "Q")
offeru = WHOLE_CART_OFFERS("U", 3, "U")


SPECIAL_DISCOUNT_PRIORITY = {
    "top": {"Z"}, 
    "medium": {"S", "T", "Y"},
    "low": {"X"}
    }

# APPEND OFFERS HERE
SINGLE_OFFERS = [offer3, offer2, offer1, offerh, offerh2, offerp, offerq, offerv2, offerv, offerk]
WHOLE_OFFERS = [offer4, offer5, offern, offerr, offeru]


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

	Complex multioffer
    >>> checkout("AAAAAEEBAAABB")
    455

	Complex multioffer + 3 Fs - 2 should be paid for
    >>> checkout("AAAAAEEBAAABBFFF")
    475

    New offers work
    >>> checkout("KK")
    120

    >>> checkout("KKNNNM")
    240

    >>> checkout("KKNNNMM")
    255

    >>> checkout("UUUU")
    120

    >>> checkout("VVVVV")
    220

    >>> checkout("STXS")
    65

    """
    total_price = 0
    item_counter = Counter(skus)
    
    for item in item_counter:
        if item not in AVAILABLE_ITEMS.keys():
            return -1
        
    # item_counter = _apply_special_cart_offers(item_counter)
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
    offers = [offer for offer in SINGLE_OFFERS if offer.item == item and offer.amount <= total_amount]
    
    if offers != []:
        for index, offer in enumerate(offers):
            if index == 0:
                best_offer = offer
            else:
                if ( offer.amount >= best_offer.amount):
                    best_offer = offer
    
    return best_offer

def _find_all_possible_offers(item, total_amount):
    """
    >>> _find_all_possible_offers("A", 8)
    [OFFERS(item='A', amount=5, new_price=200), OFFERS(item='A', amount=3, new_price=130)]
    """
    offers = []
    while total_amount > 0:
        offer = _find_best_offer(item,total_amount)
        if offer != None:
            offers.append(offer)
            total_amount -= offer.amount
        else:
            break

    return offers

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
    discounted_price = 0
    if (offers := _find_all_possible_offers(item, amount)):
        for offer in offers:
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

    Discounts Fs correctly
    >>> _apply_whole_cart_offers(Counter({'F': 3}))
    Counter({'F': 2})

    Does not discount from 2 Fs:
    >>> _apply_whole_cart_offers(Counter({'F': 2}))
    Counter({'F': 2})

	4 Fs
    >>> _apply_whole_cart_offers(Counter({'F': 4}))
    Counter({'F': 3})


	6 Fs
    >>> _apply_whole_cart_offers(Counter({'F': 6}))
    Counter({'F': 4})
    """

    for item_in_cart in item_counter:
        for offer in WHOLE_OFFERS:
            if item_in_cart == offer.item and offer.free_item in item_counter:
                
                if offer.item != offer.free_item:
                    # Handles same-item offers by updating
                    n_discounted_items = floor(item_counter[item_in_cart] / offer.amount)
                else:
                    items_for_promotion = item_counter[item_in_cart] - 1
                    n_discounted_items = floor(items_for_promotion / offer.amount )

                if n_discounted_items >= item_counter[offer.free_item]:
                    item_counter[offer.free_item] = 0
                else:
                    item_counter[offer.free_item] -= n_discounted_items
                    

    return item_counter

def _apply_special_cart_offers(item_counter) -> Tuple[Counter, int]:
    """
    Removes items in sets of 3 if they are inside SPECIAL_OFFER_ITEMS
    >>> _apply_special_cart_offers(Counter({'X': 3, 'Y': 2, 'Z': 3}))
    (Counter({'X': 2}), 90)

    >>> _apply_special_cart_offers(Counter({'Z': 2, 'A': 1}))
    (Counter({'Z': 2, 'A': 1}), 0)
    """
    # Set a discount priority based on price
    special_offer_costs = 0
    
    total_relevant_items = (
        item_counter["S"] +
        item_counter["T"] +
        item_counter["X"] +
        item_counter["Y"] +
        item_counter["Z"] 
    )
    original_total = total_relevant_items
    
    # Return immediately if too few items
    if total_relevant_items < 3:
        return item_counter, special_offer_costs

    def discount_total_relevant_items(item_counter, priority, total_relevant_items):
        for item_label in item_counter:
            if (item_label in SPECIAL_DISCOUNT_PRIORITY[priority] and 
                item_counter[item_label] > 0
                ):
                num_max_discounts = floor(item_counter[item_label])
                print(f"Discounting {num_max_discounts} {item_label}")
                item_counter[item_label] -= num_max_discounts
                total_relevant_items -= num_max_discounts

        return (item_counter, total_relevant_items)
    
    # While we have some items
    while total_relevant_items >= 3:
        # For each of the priorities
        for priority in ["top", "medium", "low"]:
            item_counter, total_relevant_items = discount_total_relevant_items(item_counter, priority, total_relevant_items)


    special_offer_costs = (original_total - total_relevant_items) * 45

    return (item_counter, special_offer_costs)



    breakpoint()
    return item_counter, special_offer_costs

if __name__ == "__main__":
    checkout("A B B A A A")
