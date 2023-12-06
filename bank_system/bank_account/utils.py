from random import choice, choices
from string import digits

# visa
cardPrefixList = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
]

def generate_card_number() -> int:
    cc_digits = choice(cardPrefixList) + choices(digits, k=12)
    # cc_digits = list("4624748233249780")

    while True:
        items = list((map(lambda x: str(int(x) * 2), cc_digits[:-1:2])))
        checksum = 0
        for item in items:
            if len(item) > 1:
                checksum += int(item[0]) + int(item[1])
            else:
                checksum += int(item[0])

        other_items = []
        for i, val in enumerate(cc_digits):
            if i % 2 == 1:
                other_items.append(val)
        other_items_sum = sum(map(lambda x: int(x), other_items))
        if (checksum + other_items_sum) % 10 == 0:
            break
        else:
            cc_digits = choice(cardPrefixList) + choices(digits, k=12)

    cc_number = "".join(cc_digits)  
    
    return cc_number