from flask import Flask,request,jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def fetch_page(url):
    try:
        response = requests.get(url)
        print(response.status_code)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def parse_flipkart(html_content,productName):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    
    if soup.find('div', class_='KzDlHZ'):
        name = soup.find('div', class_='KzDlHZ').text
    else:
        name = productName
    # link = product.find('a', class_='IRpwTa')
    dis_price = soup.find('div', class_='Nx9bqj')
    actual_price = soup.find('div', class_='yRaY8j')
    discount = soup.find('div', class_='UkUFwK')
        
    if dis_price and actual_price and discount:
            products.append({
                'name': name,
                'dis_price': dis_price.text,
                'actual_price': actual_price.text,
                'discount': discount.text,
            })
    return products

def parse_amazon(html_content,productName):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    if soup.find('span', class_='a-size-medium a-color-base a-text-normal'):
        print ("inside name")
        name = soup.find('span', class_='a-size-medium a-color-base a-text-normal').text
    else:
        name = productName
    dis_price = soup.find('span', class_='a-price-whole')
    actual_price = soup.find('span', class_='a-offscreen')
    discount = soup.find('span', class_='a-letter-space')
    
        
    if name and dis_price and actual_price and discount:
            products.append({
                'name': name,
                'dis_price': dis_price.text.strip(),
                'actual_price': actual_price.text.strip(),
                'discount': discount.text,
            })
    return products

@app.route('/search', methods=['GET'])
def scrap():
    name = request.args.get('name')
    flipkart_product, amazon_product = None, None
    if not name:
        return jsonify({'error': 'Missing Product Name'}), 400
    
    flipkart_url = f"https://www.flipkart.com/search?q={name}"
    amazon_url = f'https://www.amazon.in/s?k={name}'
    
    if flipkart_url:
        print("inside flipkart")
        flipkart_html = fetch_page(flipkart_url)
        if flipkart_html:
            flipkart_product = parse_flipkart(flipkart_html,name)
    
    if amazon_url:
        print("inside amazon")
        amazon_html = fetch_page(amazon_url)
        if amazon_html:
            amazon_product = parse_amazon(amazon_html,name)
            

    return jsonify({'flipkart': flipkart_product,'amazon':amazon_product}), 200


if __name__ == "__main__":
    app.run(debug=True)
