import csv
import os
import xml.etree.ElementTree as et
from dataclasses import fields
from datetime import datetime
from xml.dom import minidom

OFFER_FIELDS = ['name', 'description', 'url', 'picture', 'category', 'currency', 'price', 'oldprice', 'store',
          'pickup', 'delivery']
CLINIC_FIELDS = ['']
DOCTOR_FIELDS = ['internal_id', 'name', 'description', 'first_name', 'surname', 'patronymic', 'experience_years',
                 'career_start_date', 'degree', 'rank']
SHOP_FIELDS = ['name', 'company', 'url', 'email', 'picture', 'description']


class YmlGenerator:
    def __init__(self, name, company, url, picture):
        self.name = name
        self.company = company
        self.url = url
        self.picture = picture

    # def check_fields_csv():

