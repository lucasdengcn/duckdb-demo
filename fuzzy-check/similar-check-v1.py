import duckdb
import time
from thefuzz import fuzz

con = duckdb.connect("products.duckdb")
BATCH_SIZE = 10000
SM_THRESHOLD = 80

def fuzzy_similarity(str1: str, str2: str) -> int:
    return fuzz.ratio(str1, str2)

duckdb.create_function("fuzzy_similarity", fuzzy_similarity)

def prepare():
    sql = "CREATE TABLE similarity_matrix (sku_a TEXT, description_a TEXT, sku_b TEXT, description_b TEXT, similar_ratio FLOAT);"
    con.execute(sql)

def load_data(table_name, csv_file_name):
    sql = f"""
    CREATE TABLE {table_name} AS (select SKU, description, price from {csv_file_name})
    """
    con.sql(sql)

def calculate_similarity(rs, rs2):
    sm = []
    for row in rs:
        for row2 in rs2:
            sr = fuzz.ratio(row[1], row2[1])
            if sr > SM_THRESHOLD:
                #print(f"{row[1]}, {row2[1]}, {sr}")
                sm.append((row[0], row[1], row2[0], row2[1], sr))
    #
    sql = "insert into similarity_matrix (sku_a, description_a, sku_b, description_b, similar_ratio) values (?, ?, ?, ?, ?);"
    con.executemany(sql, sm)

def get_rows(table_name, batch_size, offset):
    sql = f"select sku, description from {table_name} limit {batch_size} offset {offset};"
    rs = con.execute(sql).fetchall()
    return rs

def process_data():
    start_time = time.time()
    offsets = [0, 0]
    while True:
        #
        rs = get_rows("data_01", BATCH_SIZE, offsets[0])
        if len(rs) == 0:
            break
        while True:
            print(f"processing offset={offsets[0]}, check with offset={offsets[1]}")
            rs2 = get_rows("data_02", BATCH_SIZE, offsets[1])
            if len(rs2) == 0:
                break
            calculate_similarity(rs, rs2)
            offsets[1] += BATCH_SIZE
        #
        offsets[0] += BATCH_SIZE
    ts = time.time() - start_time
    print(f"process DONE. duration={ts} seconds")


def exported_rank_similarity():
    sql = """
    COPY (
        select * from (
        SELECT sku_a, description_a, sku_b, description_b, similar_ratio, 
                row_number() OVER (PARTITION BY sku_a ORDER BY similar_ratio desc) as rn
        FROM similarity_matrix
        ) where rn < 3
    ) TO 'similarity_matrix_output.csv' (HEADER, DELIMITER ',');
    """
    con.execute(sql)


def main():
    prepare()
    load_data("data_01", "generated_data_01.csv")
    load_data("data_02", "generated_data_02.csv")
    process_data()
    exported_rank_similarity()
    con.close()


if __name__ == '__main__':
    main()