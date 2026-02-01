import os
import xml.etree.ElementTree as et
from datetime import datetime
from xml.dom import minidom

from lib.helpers.constants import CURRENCIES, ProductOfferFields, VENDOR_MODEL_TYPE
from lib.helpers.get import get_reader_and_header

AVAILABILITY = {"да": "true", "нет": "false"}

class YmlProductsGenerator:
    def __init__(self, source_path: str = "source/products.csv"):
        self.source_file = source_path
        self.root = et.Element("yml_catalog")
        self.currencies = et.SubElement(self.root, "currencies")
        self.categories = et.SubElement(self.root, "categories")
        self.offers = et.SubElement(self.root, "offers")
        self.dict_categories = dict()

    def _generate_root(self):
        self.root.set('version', '2.0')
        self.root.set('date', datetime.now().strftime('%Y-%m-%d %H:%M'))

    def _generate_currencies(self):
        for i, currency in CURRENCIES.items():
            child = et.SubElement(self.currencies, "currency")
            child.set("id", str(i))
            child.text = currency

    def _generate_categories(self):
        reader, header = get_reader_and_header(self.source_file)
        added_categories = set()
        for idx, row in enumerate(reader, start=2):
            if row["category"] not in added_categories:
                child = et.SubElement(self.categories, "category")
                child.set("id", str(idx))
                child.text = row["category"]
                added_categories.add(row["category"])
                self.dict_categories[child.text] = str(idx)

    def _generate_offers(self):
        reader, header = get_reader_and_header(self.source_file)
        for _, row in enumerate(reader, start=2):
            offer = et.SubElement(self.offers, "offer")
            offer.set("id", row["id"])
            offer.set("type", VENDOR_MODEL_TYPE)
            offer.set("available", AVAILABILITY[row["available"]])

            et.SubElement(offer, "currencyId").text = CURRENCIES["RUB"]
            et.SubElement(offer, "categoryId").text = self.dict_categories[row["category"]]

            for _, field in enumerate(ProductOfferFields):
                child = et.SubElement(offer, field)
                child.text = row[field]

    def create_yml(self):
        self._generate_root()
        self._generate_currencies()
        self._generate_categories()
        self._generate_offers()

    def save_yml(self, dir_to_save: str = 'result', name: str = 'yml_doctors.xml') -> None:
        if not os.path.exists(dir_to_save):
            os.makedirs(dir_to_save)
        with open(f'{dir_to_save}/{name}.xml', 'w') as outfile:
            xml_str = minidom.parseString(et.tostring(self.root,'utf-8')).toprettyxml(indent="  ")
            outfile.write(xml_str)
            outfile.close()
