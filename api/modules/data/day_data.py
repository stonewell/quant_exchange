class DayData(object):
    def __init__(self):
        self.stock_id = ""
        self.amount = 0
        self.date = 0
        self.open_price = 0
        self.close_price = 0
        self.highest_price = 0
        self.lowest_price = 0
        self.vol = 0
        self.reserved = 0

    def __repr__(self):
        return 'date:{} open:{} close:{} high:{} low:{} amount:{} vol:{} '.format(self.date,
                                                                                        self.open_price,
                                                                                        self.close_price,
                                                                                        self.highest_price,
                                                                                        self.lowest_price,
                                                                                        self.amount,
                                                                                        self.vol)
