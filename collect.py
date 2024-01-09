import pandas as pd
from sqlalchemy import create_engine, exc
from db_secrets import *
import psycopg


def create_connections():
    connection_list = []

    for name in DB_NAME_LIST:
        url = DB_HOST.replace("ZZZ", name)
        engine = create_engine(
            f"postgresql+psycopg://{DB_USERNAME}:{DB_PASSWORD}@{url}/{name}"
        )
        connection = engine.connect()
        connection_list.append(connection)
    return connection_list

def postgres_upsert(table, conn, keys, data_iter):
    from sqlalchemy.dialects.postgresql import insert

    data = [dict(zip(keys, row)) for row in data_iter]

    insert_statement = insert(table.table).values(data)
    upsert_statement = insert_statement.on_conflict_do_update(
        constraint=f"{table.table.name}_pkey",
        set_={c.key: c for c in insert_statement.excluded},
    )
    conn.execute(upsert_statement)

def populate(connections):
    engine = create_engine(f"postgresql+psycopg://benhurst@127.0.0.1/postgres")
    local_connection = engine.connect()
    connections_length = len(connections)

    select_ids_query = "SELECT id FROM all_data"
    ids_df = pd.read_sql(select_ids_query, local_connection)
    # print(ids_df['id'])
    for index, connection in enumerate(connections):
        select_query = "SELECT * FROM responses"
        df = pd.read_sql(select_query, connection)
        print(len(df))
        new_df = df[~df['id'].isin(ids_df['id'])]
        print(len(new_df))
        # print(new_df)
        # new_df.to_sql(f"all_data", local_connection, if_exists="append", index=False)
        # new_df.to_sql('all_data', 
        #       local_connection,
        #       if_exists='append',
        #       index=False,
        #       method=postgres_upsert)
    #     print(f'{index} of {connections_length}')
        for i in range(len(new_df)):
            try:
                new_df.iloc[i : i + 1].to_sql(
                    name="all_data", if_exists="append", con=local_connection, index=False
                )
                print(f"Inserted row {i} in connection {index + 1} of {connections_length}")
            except exc.IntegrityError:
                print(f"Duplicated row {i} in connection {index + 1} of {connections_length}")
                pass  # or any other action


connections = create_connections()
populate(connections)
# print(connections)

# for i in range(len(df)):
#     try:
#         df.iloc[i:i+1].to_sql(name="Table_Name",if_exists='append',con = Engine)
#     except IntegrityError:
#         pass #or any other action
