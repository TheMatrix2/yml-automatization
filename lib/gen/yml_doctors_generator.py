import os
import xml.etree.ElementTree as et
from datetime import datetime
from xml.dom import minidom

from lib.helpers.get import get_reader_and_header

SHOP_FIELDS = ['name', 'company', 'url', 'email', 'picture']
DOCTOR_FIELDS = ['internal_id', 'description', 'first_name', 'surname', 'patronymic', 'experience_years',
                 'degree', 'rank']
CLINIC_FIELDS = ['url', 'picture', 'name', 'city', 'address', 'email', 'phone', 'internal_id', 'company_id']
SERVICE_FIELDS = ['name', 'gov_id', 'description', 'internal_id']
OFFER_FIELDS = ['url', 'base_price', 'currency', 'speciality', 'is_base_service']

LOGIC_CONVERTER = {'ИСТИНА': 'true', 'ЛОЖЬ': 'false'}


class YmlGenerator:
    def __init__(self, source_path: str):
        self.source_csv = source_path + '/doctors.csv'
        self.shop = et.Element('shop')
        self._generate_shop_element()
        self.doctors = et.SubElement(self.shop, 'doctors')
        self.clinics = et.SubElement(self.shop, 'clinics')
        self.services = et.SubElement(self.shop, 'services')
        self.offers = et.SubElement(self.shop, 'offers')

    def _generate_shop_element(self):
        csv_reader, header = get_reader_and_header(self.source_csv)
        for idx, row in enumerate(csv_reader, start=2):
            self.shop.set('version', '2.0')
            self.shop.set('date', datetime.now().strftime('%Y-%m-%d %H:%M'))
            for field in SHOP_FIELDS:
                et.SubElement(self.shop, field).text = row['shop.' + field]
            break

    def _get_service_id(self, service_name: str) -> str | None:
        for service in self.services.findall('service'):
            if service.find('name').text == service_name:
                return service.get('id')
        else:
            return None

    def _generate_offers(self):
        csv_reader, header = get_reader_and_header(self.source_csv)
        for idx, row in enumerate(csv_reader, start=2):
            if row['offer.url'] == '':
                continue
            # doctor
            if self.doctors.find(f'doctor[@id="{row["doctor.internal_id"]}"]') is None:
                doctor = et.SubElement(self.doctors, 'doctor')
                doctor.set('id', row['doctor.id'])
                et.SubElement(doctor, 'name').text = ' '.join(
                    [row['doctor.surname'], row['doctor.first_name'], row['doctor.patronymic']])
                for doctor_field in DOCTOR_FIELDS:
                    if row['doctor.' + doctor_field] == '': continue
                    et.SubElement(doctor, doctor_field).text = row['doctor.' + doctor_field]

            # clinic
            if self.clinics.find(f'clinic[@id="{row["clinic.id"]}"]') is None:
                clinic = et.SubElement(self.clinics, 'clinic')
                clinic.set('id', row['clinic.id'])
                for clinic_field in CLINIC_FIELDS:
                    et.SubElement(clinic, clinic_field).text = row['clinic.' + clinic_field]

            # services
            if self.services.find(f'service[@id="{row["service.id"]}"]') is None:
                service = et.SubElement(self.services, 'service')
                service.set('id', row['service.id'])
                for service_field in SERVICE_FIELDS:
                    et.SubElement(service, service_field).text = row['service.' + service_field]

            # offer
            elem = et.SubElement(self.offers, 'offer')
            elem.set('id', str(idx))
            et.SubElement(elem, 'url').text = row['offer.url']
            et.SubElement(elem, 'appointment').text = LOGIC_CONVERTER[row['offer.appointment']]

            price = et.SubElement(elem, 'price')
            et.SubElement(price, 'base_price').text = row['offer.base_price']
            et.SubElement(price, 'currency').text = 'RUR'

            et.SubElement(elem, 'service').set('id', row['service.id'])

            clinic = (et.SubElement(elem, 'clinic'))
            clinic.set('id', row['clinic.id'])
            doctor = et.SubElement(clinic, 'doctor')
            doctor.set('id', row['doctor.id'])
            et.SubElement(doctor, 'speciality').text = row['offer.speciality']
            et.SubElement(doctor, 'is_base_service').text = LOGIC_CONVERTER[row['service.is_base_service']]

    def generate_yml(self) -> None:
        self._generate_offers()

    def save_yml(self, dir_to_save: str = 'result', name: str = 'yml_doctors.xml') -> None:
        if not os.path.exists(dir_to_save):
            os.makedirs(dir_to_save)
        with open(f'{dir_to_save}/{name}.xml', 'w') as outfile:
            xml_str = minidom.parseString(et.tostring(self.shop,'utf-8')).toprettyxml(indent="  ")
            outfile.write(xml_str)
            outfile.close()


if __name__ == "__main__":
    root = et.Element('root')
    tree = et.ElementTree(root)
    et.indent(tree, space="\t", level=0)
    et.SubElement(root, 'tag1').text = ' '
    tree.write('test.xml')

