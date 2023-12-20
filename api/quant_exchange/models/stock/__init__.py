import marshmallow as ma


class StockSchema(ma.Schema):
    id = ma.fields.String()
    name = ma.fields.String()
    attrs = ma.fields.List(ma.fields.String())


class StocksQueryArgsSchema(ma.Schema):
    attrs = ma.fields.List(ma.fields.String())

class StockQueryArgsSchema(ma.Schema):
    start_date=ma.fields.Date()
    end_date=ma.fields.Date()
