import twder
def currencysearch(search):
	dollarTuple = twder.now_all()[search]
    reply = '{}\n即期賣出價:{}'.format(dollarTuple[0],dollarTuple[4])
    return reply
    