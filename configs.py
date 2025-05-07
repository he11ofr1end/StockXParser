import json
import logging


def write_to_file(product_data: list[dict[str:str, str:str]]) -> None:
    """Write size and price to file

    :return: None
    """
    with open("products.json", "a") as file:
        json.dump(product_data, file)


def extract_urls_from_file():
    """Extracts product urls from json file

    :return:
    """
    filename = "product_urls.txt"
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/stockx_parser.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
