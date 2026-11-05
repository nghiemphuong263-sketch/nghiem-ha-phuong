"""Regression checks for SVG charts passing through localization."""
import unittest
import xml.etree.ElementTree as ET
from i18n import Localizer

class ChartLocalizationTest(unittest.TestCase):
    def test_self_closing_chart_marks_remain_siblings(self):
        source = ('<svg xmlns="http://www.w3.org/2000/svg"><g>'
                  '<line x1="0" y1="100" x2="300" y2="100"/>'
                  '<text x="0" y="104">0</text>'
                  '<rect x="40" y="25" width="30" height="75">'
                  '<title>NDC: low</title></rect>'
                  '<circle cx="150" cy="25" r="4"/>'
                  '<polyline points="40,25 150,25"/>'
                  '<text x="40" y="120">NDC: low</text></g></svg>')
        parser = Localizer({'NDC: low': 'NDC thấp'}, 'https://example.com')
        parser.feed(source)
        root = ET.fromstring(''.join(parser.out))
        ns = '{http://www.w3.org/2000/svg}'
        group = root.find(ns+'g')
        self.assertEqual([n.tag.removeprefix(ns) for n in group],
                         ['line', 'text', 'rect', 'circle', 'polyline', 'text'])
        self.assertEqual(group.find(ns+'rect').attrib,
                         {'x':'40', 'y':'25', 'width':'30', 'height':'75'})
        self.assertEqual(group.find(ns+'rect').find(ns+'title').text, 'NDC thấp')
        self.assertEqual(group.findall(ns+'text')[1].text, 'NDC thấp')

    def test_html_void_elements_remain_valid(self):
        parser = Localizer({'Home':'Trang chủ'}, 'https://example.com')
        parser.feed('<p>Home<br/><img src="/image.png"/></p>')
        self.assertEqual(''.join(parser.out),
                         '<p>Trang chủ<br><img src="/image.png"></p>')

if __name__ == '__main__':
    unittest.main()
