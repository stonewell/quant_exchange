import marshmallow as ma


class StockSchema(ma.Schema):
    id = ma.fields.String()
    name = ma.fields.String()
    attrs = ma.fields.List(ma.fields.String())

class StockDataSchema(ma.Schema):
  open = ma.fields.Float(data_key='o')
  close = ma.fields.Float(data_key='c')
  high = ma.fields.Float(data_key='h')
  low = ma.fields.Float(data_key='l')
  volume = ma.fields.Float(data_key='v')
  day = ma.fields.Date(data_key='d')

class StocksQueryArgsSchema(ma.Schema):
    attrs = ma.fields.List(ma.fields.String())

class StockQueryArgsSchema(ma.Schema):
    start_date=ma.fields.Date()
    end_date=ma.fields.Date()
