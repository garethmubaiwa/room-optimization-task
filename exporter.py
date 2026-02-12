'''
This module defines the Exporter class and related file format strategies for exporting data.
The Exporter class takes a description of the data, the rows of data, and a strategy for how to save the data (e.g., JSON or XML).
The FileFormat class is an abstract base class that defines the interface for saving data, and the JSONFormat and XMLFormat classes implement this interface for their respective formats.
The Exporter class uses the strategy pattern to allow for flexible exporting of data in different formats without changing the core logic of how the data is structured.
'''


import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from decimal import Decimal  

class FileFormat(ABC):
    @abstractmethod
    def save(self, data, path):
        pass

class JSONFormat(FileFormat):
    def save(self, data, path):
        # Custom converter for Decimal types
        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return float(obj) # Convert Decimal to float
            raise TypeError

        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=decimal_default)

class XMLFormat(FileFormat):
    def save(self, data, path):
        root = ET.Element("results")
        for item in data:
            item_element = ET.SubElement(root, "item")
            for key, value in item.items():
                child = ET.SubElement(item_element, key)
                child.text = str(value)

        tree = ET.ElementTree(root)
        tree.write(path, encoding="utf-8", xml_declaration=True)

class Exporter:
    def __init__(self, description, rows, strategy: FileFormat):
        self.columns = [col[0] for col in description]
        self.rows = rows
        self.strategy = strategy

    def export(self, path):
        data = self._build_data()
        self.strategy.save(data, path)

    def _build_data(self):
        return [dict(zip(self.columns, row)) for row in self.rows]