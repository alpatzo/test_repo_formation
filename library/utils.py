def promo(price):
    # price = price - ((price / 100) * 25)
    price = round(price - ((price / 100) * 25), 2) # return 2digit after ,
    return price