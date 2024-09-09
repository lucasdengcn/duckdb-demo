from faker import Faker
import pandas as pd
import random

# Initialize Faker to generate fake data
fake = Faker()

# Define the number of products to generate
num_products = 10000  # Adjust this number as needed

# Generate random product data
products = []
for _ in range(num_products):
    product = {
        'SKU': fake.unique.ssn(),
        'description': fake.catch_phrase(),
        'price': round(random.uniform(10.0, 1000.0), 2)
    }
    products.append(product)

# Create a DataFrame from the generated product data
products_df = pd.DataFrame(products)

# Save the generated product data to a CSV file
products_df.to_csv('generated_data_01.csv', index=False)