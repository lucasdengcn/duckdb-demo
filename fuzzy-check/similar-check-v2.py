import duckdb
import time
from thefuzz import fuzz

con = duckdb.connect("data_all.duckdb")

def fuzzy_similarity(str1: str, str2: str) -> int:
    return fuzz.ratio(str1, str2)

con.create_function("fuzzy_similarity", fuzzy_similarity)

def prepare():
    sql = """
    CREATE TABLE data_all as
    select t0.sku as sku_a, t0.description as description_a,
        t1.sku as sku_b, t1.description as description_b,
        0 as similarity
    from
    (select SKU, description, price from generated_data_01.csv) t0,
    (select SKU, description, price from generated_data_02.csv) t1,
    """
    con.sql(sql)

def calculate_similarity():
    sql = """
    update data_all set similarity = fuzzy_similarity(description_a, description_b);
    """
    con.execute(sql).fetchall()

def exported_rank_similarity():
    sql = """
    COPY (
        SELECT * from (
            SELECT sku_a, description_a, sku_b, description_b, similarity, 
                row_number() OVER (PARTITION BY sku_a ORDER BY similarity desc) as rn
            FROM data_all WHERE similarity > 80
        ) WHERE rn < 3
    ) TO 'similarity_matrix_output.csv' (HEADER, DELIMITER ',');
    """
    con.execute(sql)


def main():
    ts0 = time.time()
    prepare()
    calculate_similarity()
    exported_rank_similarity()
    con.close()
    ts0 = time.time() - ts0
    print(f"duration: {ts0} seconds")


if __name__ == '__main__':
    main()