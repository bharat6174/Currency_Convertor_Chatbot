from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    print(source_currency)
    print(amount)
    print(target_currency)

    cf = fetch_conversion_factor(source_currency, target_currency, amount)
    final_amount = round(amount*cf,2)
    print(final_amount)
    response = {
        'fulfillmentText': "{} {} is {} {} at a rate of {} {} per {}".format(amount, source_currency, final_amount, target_currency, cf, source_currency, target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target, amo):
    url = "https://anyapi.io/api/v1/exchange/convert?base={}&to={}&amount={}&apiKey=2cisqafqku8ivutqflndk1ugpm5njia8f6bgfgsm3eltsvfckuk3".format(source, target, amo)

    response = requests.get(url)
    response = response.json()
    return response['rate']
if __name__ == "__main__":
    app.run(debug = True)