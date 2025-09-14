import csv
import os
import xml.etree.ElementTree as et
from datetime import datetime
from xml.dom import minidom


def generate_xml_feed(csv_file_path, output_file_path):
    """
    Generate an XML feed for Yandex from a CSV file containing doctor information,
    following the format specified at https://yastatic.net/s3/doc-binary/src/support/ru/webmaster/files/doctors.xml

    Args:
        csv_file_path (str): Path to the CSV file with doctor data
        output_file_path (str): Path where the XML file will be saved
    """
    # Create the root element with date attribute
    yml_catalog = et.Element('yml_catalog')
    yml_catalog.set('date', datetime.now().strftime('%Y-%m-%d %H:%M'))

    # Create shop element
    shop = et.SubElement(yml_catalog, 'shop')

    name = et.SubElement(shop, 'name')
    name.text = 'Аксиома'
    company = et.SubElement(shop, 'company')
    company.text = 'ООО Медицинский центр «Аксиома»'
    url = et.SubElement(shop, 'url')
    url.text = 'https://axioma.clinic'
    picture = et.SubElement(shop, 'picture')
    picture.text = 'https://static.tildacdn.com/tild3666-3634-4836-b131-656234653138/noroot.png'
    currency = et.SubElement(et.SubElement(shop, 'currencies'), 'currency')
    currency.set('id', 'RUR')
    currency.set('rate', '1')
    category = et.SubElement(et.SubElement(shop, 'categories'), 'category')
    category.set('id', '1')
    category.text = 'Врач'


    # Create categories element
    sets = et.SubElement(shop, 'sets')

    # Create offers element
    offers = et.SubElement(shop, 'offers')

    const_param_names = {'Город': 'Пермь', 'Город клиники': 'Пермь', 'Адрес клиники': 'ул. Н. Островского, 64, Пермь',
                         'Название клиники': 'Аксиома'}

    param_names = ['Фамилия', 'Имя', 'Отчество', 'Годы опыта', 'Взрослый врач',
                   'Детский врач', 'Возможность записи', 'Образование - 1', 'Степень', 'Звание', 'Категория']

    # Dictionary to store unique specialties for categories
    specialties = {}
    speciality_id = 1

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')

        # Process each doctor
        for idx, row in enumerate(reader, start=1):
            # Skip rows with empty specialties or links
            if not row['Специальность'] or not row['url']:
                continue

            # Process specialties for categories
            spec_list = [s.lower().strip() for s in row['Специальность'].split(',')]

            for specialty in spec_list:
                if specialty not in specialties:
                    specialties[specialty] = speciality_id
                    spec = et.SubElement(sets, 'set')
                    spec.set('id', str(speciality_id))
                    name = et.SubElement(spec, 'name')
                    name.text = specialty
                    speciality_id += 1

            # Create full name
            full_name = f"{row['Фамилия']} {row['Имя']} {row['Отчество']}"

            # Create the doctor offer
            offer = et.SubElement(offers, 'offer')
            offer.set('id', str(idx))

            # Add name
            name_elem = et.SubElement(offer, 'name')
            name_elem.text = full_name

            # Add URL
            url_elem = et.SubElement(offer, 'url')
            url_elem.text = row['url']

            # Add price (default to 0 if not provided)
            price = et.SubElement(offer, 'price')
            price.text = str(row['Цена']) if row['Цена'] else str(0)

            # Add currency
            currency_id = et.SubElement(offer, 'currencyId')
            currency_id.text = 'RUR'

            set_ids = et.SubElement(offer, 'set-ids')
            set_ids.text = ','.join([str(specialties[specialty]) for specialty in spec_list])

            # Add category ID
            cat_id = et.SubElement(offer, 'categoryId')
            cat_id.text = str(1)

            # Add photo if available
            if row.get('Фото'):
                picture = et.SubElement(offer, 'picture')
                picture.text = row['Фото']

            # Add description
            if row.get('Описание'):
                description = et.SubElement(offer, 'description')
                description.text = row['Описание']

            # Add params
            for param_name in param_names:
                if row.get(param_name):
                    param = et.SubElement(offer, 'param')
                    param.set('name', param_name)
                    param.text = row[param_name] if param_name not in ['Взрослый врач',
                                                                       'Детский врач',
                                                                       'Возможность записи'] else row[param_name].lower()
            for param_name in const_param_names:
                param = et.SubElement(offer, 'param')
                param.set('name', param_name)
                param.text = const_param_names[param_name]


    # Convert to string with pretty formatting
    xml_str = minidom.parseString(et.tostring(yml_catalog, 'utf-8')).toprettyxml(indent="  ")

    # Write to file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)

    print(f"XML feed has been generated and saved to {output_file_path}")
    print(f"Total doctors processed: {sum(1 for _ in offers.findall('offer'))}")
    print(f"Total categories: {sum(1 for _ in sets.findall('category'))}")


if __name__ == "__main__":
    # Define input and output file paths
    input_csv = "doctors.csv"  # Path to your CSV file
    output_xml = "axioma_doctors_feed.xml"  # Path to save the XML feed

    # Check if the CSV file exists
    if not os.path.exists(input_csv):
        print(f"Error: File {input_csv} not found.")
    else:
        # Generate the XML feed
        generate_xml_feed(input_csv, output_xml)