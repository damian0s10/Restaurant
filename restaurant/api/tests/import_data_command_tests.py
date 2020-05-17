from api.management.commands import import_data
from django.test import TestCase


class ImportDataCommandTestCase(TestCase):
    def setUp(self) -> None:
        self.command = import_data.Command()
        self.sections = self.command.get_sections_list()

    def test_import_data_from_url(self):
        section = self.sections[0]
        parsed_section = self.command.parse_section(section)

        expected = {
            'category': 'Fast Brooklyn',
            'products': [
                {
                    'name': 'Tortilla z plackiem pszennym',
                    'description': 'Mięso wieprzowe bądź drobiowe, warzywa, sos, placek',
                    'price': '15.90'
                },
                {
                    'name': 'Skrzydełka Brooklyn',
                    'description': '6 skrzydełek z kurczaka, frytki, surówka wiosenna z sosem vinegret',
                    'price': '20.90'
                },
                {
                    'name': 'Stripsy',
                    'description': '5 kawałków z piersi kurczaka, frytki, surówka wiosenna z sosem vinegret, sos',
                    'price': '24.90'
                }
            ]
        }
        self.assertDictEqual(expected, parsed_section)
