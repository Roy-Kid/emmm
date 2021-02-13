# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-02-10
# version: 0.0.1

from . import InputBase
import xml.etree.ElementTree as ET


class INxml(InputBase):

    def read_data(self, file, inputdata=None):

        tree = ET.parse(file)
        
        if inputdata:
            self.data = None
        else:
            self.data = inputdata

        