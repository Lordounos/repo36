# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AV9gmNhFK-BDSDSSzg9IpimdrWHNMFh9
"""

!pip install pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, rand, floor
import random
from datetime import datetime, timedelta

# Создание SparkSession
spark = SparkSession.builder \
    .appName("Synthetic E-commerce Data Generation") \
    .getOrCreate()
    # Параметры генерации данных
num_rows = 1000  # Количество строк, можно изменить
products = ["Product_A", "Product_B", "Product_C", "Product_D", "Product_E"]
min_quantity = 1
max_quantity = 10
min_price = 10.0
max_price = 100.0

# Функция для генерации случайной даты в пределах последнего года
def random_date():
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    return start_date + (end_date - start_date) * random.random()

# Генерация данных
data = [(random_date().strftime("%Y-%m-%d"),
         random.randint(1, 1000),
         random.choice(products),
         random.randint(min_quantity, max_quantity),
         round(random.uniform(min_price, max_price), 2)) for _ in range(num_rows)]

# Создание DataFrame
columns = ["Дата", "UserID", "Продукт", "Количество", "Цена"]
df = spark.createDataFrame(data, columns)

# Объединение всех партиций в одну и сохранение DataFrame в формате CSV
output_path = "synthetic_ecommerce_data.csv"
df.coalesce(1).write.csv(output_path, header=True, mode="overwrite")

print(f"Data saved to {output_path}")