import marshmallow as ma


class StockDataSchema(ma.Schema):
  status = ma.fields.String(data_key='s')
  next_time = ma.fields.Int(data_key='nextTime')
  open = ma.fields.List(ma.fields.Float(), data_key='o')
  close = ma.fields.List(ma.fields.Float(), data_key='c')
  high = ma.fields.List(ma.fields.Float(), data_key='h')
  low = ma.fields.List(ma.fields.Float(), data_key='l')
  volume = ma.fields.List(ma.fields.Float(), data_key='v')
  day = ma.fields.List(ma.fields.Int(), data_key='t')


class SymbolResolveArgsSchema(ma.Schema):
  s = ma.fields.String(data_key='symbol')


class HistoryArgsSchema(ma.Schema):
  f = ma.fields.Float(data_key='from')
  t = ma.fields.Float(data_key='to')
  s = ma.fields.String(data_key='symbol')
  r = ma.fields.String(data_key='resolution')
  c = ma.fields.Float(data_key='countback')


class SearchArgsSchema(ma.Schema):
  q = ma.fields.String(data_key='query')
  l = ma.fields.Float(data_key='limit')
  t = ma.fields.String(data_key='type')
  e = ma.fields.String(data_key='exchange')


class SearchResultSchema(ma.Schema):
  d = ma.fields.String(data_key='description')
  n = ma.fields.String(data_key='full_name')
  e = ma.fields.String(data_key='exchange')
  s = ma.fields.String(data_key='symbol')
  ti = ma.fields.String(data_key='ticker')
  t = ma.fields.String(data_key='type')
