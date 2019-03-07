from .base import Module

SOCK_PRICE = 9.98
SOCK_URL = "https://yale.bncollege.com/webapp/wcs/stores/servlet/TCK_Quarter_Sock/ProductDisplay?imageId=1359086&level=&graphicId=YAL2ROYAL-WHT-DKGREY&categoryId=40481&catalogId=10001&langId=-1&storeId=16556&productId=400000354407"

class Price(Module):
    DESCRIPTION = "Convert USD to YSK"
    ARGC = 1
    def response(self, query, message):
        query = query.strip().strip('$')
        price = float(query)
        return "For $%.2f, you could purchase %.2f pairs of socks from the Yale Bookstore. Make the right choice here: %s" % (price, price / SOCK_PRICE, SOCK_URL)
