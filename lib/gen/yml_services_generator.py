import csv
import os
from datetime import datetime, timezone, timedelta
import xml.etree.ElementTree as et
from xml.dom import minidom


class YmlServicesGenerator:
    def __init__(self,
                 source_path: str,
                 name: str,
                 company: str,
                 url: str,
                 platform: str = None):
        self.source_csv = source_path + '/services.csv'

        self.yml_catalog = et.Element('yml_catalog')
        format_string = "%Y-%m-%dT%H:%M%z"
        tz_plus_3 = timezone(timedelta(hours=3))
        now_aware = datetime.now(tz_plus_3)
        formatted_time = now_aware.strftime(format_string)
        self.yml_catalog.set('date', formatted_time[:-2] + ':' + formatted_time[-2:])

        et.SubElement(self.yml_catalog, 'name').text = name
        et.SubElement(self.yml_catalog, 'company').text = company
        et.SubElement(self.yml_catalog, 'url').text = url
        if platform:
            et.SubElement(self.yml_catalog, 'platform').text = platform

        self.categories = et.SubElement(self.yml_catalog, 'categories')
        self.offers = et.SubElement(self.yml_catalog, 'offers')

    @staticmethod
    def _get_reader_and_header(source_path: str):
        csv_file = open(source_path)
        reader = csv.reader(csv_file)
        next(reader)
        header = next(reader)
        csv_reader = csv.DictReader(csv_file, delimiter=',', fieldnames=header)
        return csv_reader, header

    def generate_yml(self):
        csv_reader, header = YmlServicesGenerator._get_reader_and_header(self.source_csv)
        category_ids = []
        for idx, row in enumerate(csv_reader, start=2):
            offer = et.SubElement(self.offers, 'offer')
            offer.set('id', row['offer.id'])
            offer.set('available', 'true' if row['offer.available'] == 'да' else 'false')

            if row['category.id'] not in category_ids:
                category = et.SubElement(self.categories, 'category')
                category.set('id', row['category.id'])
                category_ids.append(row['category.id'])
                category.text = row['category.name']

            et.SubElement(offer, 'name').text = row['offer.name']
            et.SubElement(offer, 'url').text = row['offer.url']
            et.SubElement(offer, 'picture').text = row['offer.picture']
            et.SubElement(offer, 'currencyId').text = 'RUB'
            et.SubElement(offer, 'categoryId').text = row['category.id']
            et.SubElement(offer, 'price').text = row['offer.price']
            et.SubElement(offer, 'description').text = row['offer.description'].replace('\n', ' ')

    def save_yml(self, dir_to_save: str = 'result', name: str = 'yml_services.xml') -> None:
        if not os.path.exists(dir_to_save):
            os.makedirs(dir_to_save)
        with open(f'{dir_to_save}/{name}.xml', 'w') as outfile:
            xml_str = minidom.parseString(et.tostring(self.yml_catalog,'utf-8')).toprettyxml(indent="  ")
            outfile.write(xml_str)
            outfile.close()
