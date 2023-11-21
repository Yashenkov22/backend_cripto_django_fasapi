import requests
from xml.etree import ElementTree as ET

from .exc import NoFoundXmlElement, TechServiceWork, RobotCheckError


def xml_parser(dict_for_parser: dict):
        direction_dict = dict_for_parser.copy()
        valute_from = direction_dict.pop('valute_from_id')
        valute_to = direction_dict.pop('valute_to_id')

        xml_url = direction_dict.get('xml_url')

        resp = requests.get(xml_url)
        headers = resp.headers

        if headers['Content-Type'] != 'text/xml; charset=UTF-8':
            raise RobotCheckError(f'{xml_url} требует проверку на робота')
        else:
            xml_file = resp.text
            print(xml_url)
            root = ET.fromstring(xml_file)

            element = root.find(f'item[from="{valute_from}"][to="{valute_to}"]')

            if element is not None:
                dict_for_addition = {
                    'valute_from': valute_from,
                    'valute_to': valute_to,
                    'in_count': element.find('in').text,
                    'out_count': element.find('out').text,
                    'min_amount': element.find('minamount').text,
                    'max_amount': element.find('maxamount').text
                    }
                return dict_for_addition
            else:
                error_text = root.text
                if error_text == 'Техническое обслуживание':
                    raise TechServiceWork(f'Техническое обслуживание по адресу {xml_url}')
                else:
                    raise NoFoundXmlElement(f'Xml элемент не найден, {xml_url}')