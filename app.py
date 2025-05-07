from stockx_parser import StockXParser
from configs import write_to_file, extract_urls_from_file

all_data = []


def run_parser():
    product_urls = extract_urls_from_file()
    # parser = StockXParser("https://stockx.com/air-jordan-cut-the-check-tr-travis-scott-mocha")
    parser = StockXParser(products_url=product_urls)
    data_ = parser.run()
    return data_


if __name__ == '__main__':
    data = run_parser()
    write_to_file(data)
