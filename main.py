from flask import Flask, request, jsonify, render_template
from cryptos import *
from blockcypher import get_address_details
import threading
import time

app = Flask(__name__)

# set testnet
btc_testnet = Bitcoin("testnet")

def generate_address(sha256_string):
    priv_key = sha256(sha256_string)
    pub_key = btc_testnet.privtopub(priv_key)
    address = btc_testnet.pubtoaddr(pub_key)
    return priv_key, pub_key, address

# Generate address
priv_key, pub_key, shop_address = generate_address("privatekey")

# product details
product = {
    'name': 'Hypothetical Digital Product',
    'price': 0.001,  # Price in BTC
    'description': 'This is a hypothetical digital product for educational purposes.'
}

payment_status = {
    'received': False,
    'tx_hash': None
}

def check_payment():
    while not payment_status['received']:
        address_details = get_address_details(shop_address, coin_symbol='btc-testnet')
        balance = address_details['final_balance']
        if balance >= product['price'] * 1e8:  # Convert BTC to Satoshis
            payment_status['received'] = True
            payment_status['tx_hash'] = address_details['unconfirmed_txrefs'][0]['tx_hash']
        time.sleep(10)

@app.route('/')
def index():
    return render_template('index.html', product=product, shop_address=shop_address, payment_status=payment_status)

@app.route('/check_payment_status', methods=['GET'])
def check_payment_status():
    return jsonify(payment_status)

@app.route('/trigger_payment', methods=['POST'])
def trigger_payment():
    payment_status['received'] = True
    payment_status['tx_hash'] = 'simulated_tx_hash'
    return jsonify({'status': 'Payment triggered'})

if __name__ == '__main__':
    # Start the payment checking thread
    payment_thread = threading.Thread(target=check_payment)
    payment_thread.start()
    app.run(debug=True, port=5050)