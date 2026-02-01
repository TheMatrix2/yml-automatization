import csv
import xml.etree.ElementTree as et


def get_categories_from_xml(xml_data: et.Element) -> dict[int, str]:
    categories = dict()
    xml_categories = xml_data.findall('./shop/categories/category')
    for xml_category in xml_categories:
        categories[int(xml_category.attrib['id'])] = xml_category.text
    return categories


def get_shop_info(xml_data: et.Element) -> dict[str, str]:
    clinic = dict()
    clinic['name'] = xml_data.find('./shop/name').text
    clinic['company'] = xml_data.find('./shop/company').text
    clinic['url'] = xml_data.find('./shop/url').text
    return clinic

def get_reader_and_header(source_path: str):
    csv_file = open(source_path)
    reader = csv.reader(csv_file)
    next(reader)
    header = next(reader)
    csv_reader = csv.DictReader(csv_file, delimiter=',', fieldnames=header)
    return csv_reader, header
