from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch, NotFoundError
from currency_data import exchange_rates
from elasticsearch_data import idForCloud, password
from flask_cors import CORS
# Initialize the Elasticsearch client for your Elasticsearch Cloud instance
def init_elasticsearch():
    return Elasticsearch(
        cloud_id=idForCloud,
        basic_auth=('elastic', password)
    )

# Initialize Elasticsearch client
es = init_elasticsearch()

# Index name for your data
index_name = 'search-currency'

# Define the data to be indexed
data_to_index = [
    {"id": 1, "base_currency": "USD", "target_currency": "EUR", "rate": 0.86},
    {"id": 2, "base_currency": "USD", "target_currency": "GBP", "rate": 0.75},
    {"id": 3, "base_currency": "USD", "target_currency": "JPY", "rate": 109.63},
    {"id": 4, "base_currency": "USD", "target_currency": "AUD", "rate": 1.32},
    {"id": 5, "base_currency": "USD", "target_currency": "CAD", "rate": 1.26},
    {"id": 6, "base_currency": "USD", "target_currency": "CHF", "rate": 0.92},
    {"id": 7, "base_currency": "USD", "target_currency": "CNY", "rate": 6.48},
    {"id": 8, "base_currency": "USD", "target_currency": "INR", "rate": 74.82},
    {"id": 9, "base_currency": "USD", "target_currency": "BRL", "rate": 5.23},
    {"id": 10, "base_currency": "EUR", "target_currency": "USD", "rate": 1.16},
    {"id": 11, "base_currency": "EUR", "target_currency": "GBP", "rate": 0.87},
    {"id": 12, "base_currency": "EUR", "target_currency": "JPY", "rate": 133.53},
    {"id": 13, "base_currency": "EUR", "target_currency": "AUD", "rate": 1.54},
    {"id": 14, "base_currency": "EUR", "target_currency": "CAD", "rate": 1.47},
    {"id": 15, "base_currency": "EUR", "target_currency": "CHF", "rate": 1.07},
    {"id": 16, "base_currency": "EUR", "target_currency": "CNY", "rate": 7.56},
    {"id": 17, "base_currency": "EUR", "target_currency": "INR", "rate": 86.91},
    {"id": 18, "base_currency": "EUR", "target_currency": "BRL", "rate": 6.03},
    {"id": 19, "base_currency": "GBP", "target_currency": "USD", "rate": 1.34},
    {"id": 20, "base_currency": "GBP", "target_currency": "EUR", "rate": 1.15},
    {"id": 21, "base_currency": "GBP", "target_currency": "JPY", "rate": 149.83},
    {"id": 22, "base_currency": "GBP", "target_currency": "AUD", "rate": 1.73},
    {"id": 23, "base_currency": "GBP", "target_currency": "CAD", "rate": 1.65},
    {"id": 24, "base_currency": "GBP", "target_currency": "CHF", "rate": 1.20},
    {"id": 25, "base_currency": "GBP", "target_currency": "CNY", "rate": 8.48},
    {"id": 26, "base_currency": "GBP", "target_currency": "INR", "rate": 97.31},
    {"id": 27, "base_currency": "GBP", "target_currency": "BRL", "rate": 6.75},
]

# Index the data
for document in data_to_index:
    doc_id = document["id"]
    es.index(index=index_name, id=doc_id, body=document)

print("Data indexed successfully.")
