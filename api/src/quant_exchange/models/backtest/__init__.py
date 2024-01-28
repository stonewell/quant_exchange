import marshmallow as ma


class RunBackTestSchema(ma.Schema):
    initialCapital = ma.fields.Float()
    timeRangeFrom = ma.fields.Int()
    timeRangeTo = ma.fields.Int()
    frequent = ma.fields.String()
    baseline = ma.fields.String()
    stockSelectMethod = ma.fields.Int()
    manualSelectedStocks = ma.fields.List(ma.fields.String())
    tradingMethod = ma.fields.Int()
    tradingInterval = ma.fields.Int()
    stockCount = ma.fields.Int()
    buyMethod = ma.fields.Int()
    sellStockWillBuy = ma.fields.Int()
    singleStockStopLoss = ma.fields.Int()
    indexStopLoss = ma.fields.Int()
