from matplotlib import table


def check_date(date, mouse_code, cursor):
    # TODO query if an entry of a trial exists using the composite primary key
    pass

def add_column(table_name, column_name, data_type):
    query = '''
        ALTER TABLE %s
        ADD %s %s''' % (table_name, column_name, data_type)
    return query

# !!!!! be careful with this command!!!
def delete_table(table_name):
    query = '''
    DROP TABLE %s''' % table_name
    return query