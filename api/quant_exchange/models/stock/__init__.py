import marshmallow as ma


class StockSchema(ma.Schema):
    id = ma.fields.String()
    name = ma.fields.String()
    attrs = ma.fields.List(ma.fields.String())


class StockQueryArgsSchema(ma.Schema):
    attrs = ma.fields.List(ma.fields.String())
