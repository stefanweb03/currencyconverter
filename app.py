import json
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch, NotFoundError
from currency_data import exchange_rates
from elasticsearch_data import idForCloud, password
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Initialize the Elasticsearch client with a function
def init_elasticsearch():
    return Elasticsearch(
        cloud_id=idForCloud,
        basic_auth=('elastic', password)
    )

# Initialize Elasticsearch client
es = init_elasticsearch()

# Specify the index name for currency conversion rates
index_name = 'search-currency'
conversions_index_name = 'conversions_made'


# Create the index if it doesn't exist (move to a separate setup script)
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

if not es.indices.exists(index=conversions_index_name):
    es.indices.create(index=conversions_index_name)


def index_exchange_rates():
    for rate in exchange_rates:
        es.index(index=index_name, body=rate)


if not es.indices.exists(index=index_name):
    index_exchange_rates()

@app.route('/api/convert', methods=['POST'])
def convert_currency():
    try:
        data = request.json
        from_currency = data.get('from', 'USD')
        to_currency = data.get('to', 'EUR')
        amount = data.get('amount', 100)  # Default amount adjusted as needed

        # Query Elasticsearch for the conversion rate
        es_query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"base_currency": from_currency}},
                        {"match": {"target_currency": to_currency}}
                    ]
                }
            }
        }

        result = es.search(index=index_name, body=es_query)
        hits = result['hits']['hits']

        if hits:
            conversion_rate = hits[0]['_source']['rate']
            converted_amount = amount * conversion_rate

            response_data = {
                "fromCurrency": from_currency,
                "toCurrency": to_currency,
                "originalAmount": amount,
                "convertedAmount": round(converted_amount, 2)
            }

            # Save the conversion data to the 'conversions_made' index
            es.index(index=conversions_index_name, body=response_data)

            return jsonify(response_data)
        else:
            return jsonify({"error": "Conversion rate not found"}), 404

    except NotFoundError:
        return jsonify({"error": "Conversion rate not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversion-rates', methods=['GET'])
def get_conversion_rates():
    try:
        # Retrieve conversion rates from Elasticsearch
        es_query = {
            "query": {
                "match_all": {}
            }
        }
        result = es.search(index=index_name, body=es_query)
        hits = result['hits']['hits']

        # Extract conversion rates data
        conversion_rates = []
        for hit in hits:
            rate = {
                "base_currency": hit['_source']['base_currency'],
                "target_currency": hit['_source']['target_currency'],
                "rate": hit['_source']['rate']
            }
            conversion_rates.append(rate)

        return jsonify(conversion_rates)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversions', methods=['GET'])
def get_conversions():
    try:
        # Retrieve all documents from the 'conversions_made' index
        result = es.search(index=conversions_index_name, body={"query": {"match_all": {}}})
        hits = result['hits']['hits']

        if hits:
            conversion_data = [hit['_source'] for hit in hits]
            return jsonify(conversion_data)
        else:
            return jsonify([])  # Return an empty list if no conversions found

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
