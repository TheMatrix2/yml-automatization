import pandas as pd
import requests
import json
import xml.etree.ElementTree as et
from typing import Generator

from lib.get import get_shop_info, get_categories_from_xml


def get_xml_url_from_csv(path_to_csv: str) -> Generator[et.Element, None, None]:
    df = pd.read_csv(path_to_csv)
    target_row = df.iloc[1]
    for cell in target_row:
        if str(cell) != 'nan':
            try:
                xml = requests.get(str(cell))
                xml_data = xml.content
                yield et.fromstring(xml_data)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")


def create_csv_from_xml(xml_data: et.Element,
                        output_csv: str,
                        output_json: str) -> None:
    offers = xml_data.findall('./shop/offers/offer')
    if not offers:
        return
    fieldnames = set()
    for offer in offers:
        fieldnames.update(child.tag for child in offer)

    df = pd.DataFrame(columns=list(fieldnames))

    for offer in offers:
        row = []
        for field in fieldnames:
            element = offer.find(field)
            row.append(element.text if element is not None else '')
        df.loc[len(df)] = row
    df.to_excel(output_csv, index=False)

    with open(output_json, 'w', encoding='utf-8') as f:
        clinic = get_shop_info(xml_data)
        categories = get_categories_from_xml(xml_data)
        summary = {'clinic': clinic, 'categories': categories}
        json.dump(summary, f, ensure_ascii=False, indent=4)
        f.close()

