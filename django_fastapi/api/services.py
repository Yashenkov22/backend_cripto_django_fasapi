import requests
from xml.etree import ElementTree as ET

# # from sqlalchemy.orm import Session

# # from db.queries import get_exchange_url
# # from utils.exc import NoFoundXmlElement, TechServiceWork


def xml_parser(direction_dict: dict):
        # print(direction_dict)
        # try:
        exchange_name = direction_dict.pop('name')
        # except KeyError:
            # exchange_name = direction_dict.pop('exchange').name

        valute_from = direction_dict.pop('valute_from_id')
        valute_to = direction_dict.pop('valute_to_id')

        xml_url = direction_dict.get('xml_url')

        resp = requests.get(xml_url)

        xml_file = resp.text
        root = ET.fromstring(xml_file)

        element = root.find(f'item[from="{valute_from}"][to="{valute_to}"]')

        if element is not None:
            dict_for_addition = {
                #  'exchange_name': exchange_name,
                 'valute_from': valute_from,
                 'valute_to': valute_to,
                #  'direction_name': valute_from + '_' + valute_to,
                
                 'in_count': element.find('in').text,
                 'out_count': element.find('out').text,
                 'min_amount': element.find('minamount').text,
                 'max_amount': element.find('maxamount').text
                }
            return dict_for_addition
        # else:
        #     error_text = root.text
        #     # print(error_element)
        #     if error_text == 'Техническое обслуживание':
        #          raise TechServiceWork(f'Техническое обслуживание по адресу {xml_url}')
        #     else:
        #         raise NoFoundXmlElement(f'Xml элемент не найден, {xml_url}')