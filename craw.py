import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def parse_flipkart(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    
    name = soup.find('div', class_='KzDlHZ')
        # link = product.find('a', class_='IRpwTa')
    dis_price = soup.find('div', class_='Nx9bqj')
    actual_price = soup.find('div', class_='yRaY8j')
    discount = soup.find('div', class_='UkUFwK')
        
    if dis_price and actual_price and discount:
            products.append({
                'name': name.text,
                'dis_price': dis_price.text,
                'actual_price': actual_price.text,
                'discount': discount.text,
            })
    return products

def parse_amazon(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    for product in soup.find_all('div', class_='s-result-item'):
        name = product.find('span', class_='a-size-medium')
        link = product.find('a', class_='a-link-normal')
        dis_price = product.find('span', class_='a-price-whole')
        actual_price = product.find('span', class_='a-price a-text-price')
        discount = product.find('span', class_='a-letter-space')
        
        if name and link and dis_price and actual_price and discount:
            products.append({
                'name': name.text.strip(),
                'link': 'https://www.amazon.com' + link['href'],
                'dis_price': dis_price.text.strip(),
                'actual_price': actual_price.text.strip(),
                'discount': discount.text.strip(),
            })
    return products

def main():
    flipkart_url = 'https://www.flipkart.com/search?q=macbookpro'
    # amazon_url = 'https://www.amazon.com/s?k=your_product_query'

    flipkart_html = fetch_page(flipkart_url)
    # amazon_html = fetch_page(amazon_url)

    if flipkart_html:
        flipkart_products = parse_flipkart(flipkart_html)
        print("Flipkart Products:")
        for product in flipkart_products:
            print(product)

    # if amazon_html:
    #     amazon_products = parse_amazon(amazon_html)
    #     print("Amazon Products:")
    #     for product in amazon_products:
    #         print(product)

if __name__ == "__main__":
    main()
