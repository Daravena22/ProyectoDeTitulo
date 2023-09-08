import sqlalchemy
from datetime import datetime

class SqlUtils:

    def rows_to_dict(obj):
        if type(obj) == list:
            data = []
            for row in obj:
                data.append(SqlUtils.rows_to_dict(row))
            return data
        elif type(obj) == sqlalchemy.engine.row.Row:
            index = 0
            data = {}
            while index < len(obj._fields):
                data[obj._fields[index]] = obj._data[index]
                index += 1
            return data