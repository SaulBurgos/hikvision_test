from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from typing import Dict, List

from models import firmware

@dataclass()
class FirmwareNodeHTML:
    html: BeautifulSoup

@dataclass()
class FirmwareWebPage:
    html: BeautifulSoup = None
    firmware_nodes: List[FirmwareNodeHTML] = field(default_factory=lambda: [])

    def get_firmware_list(self) -> List[Dict]:
        firmware_list = []

        children = self.get_direct_children_from_parent(self.get_parent_container())

        for child in children:
            self.firmware_nodes.append(FirmwareNodeHTML(html=child))
        
        return "I am a dictionary of firmware"
    
    def get_direct_children_from_parent(
        self, parent_element: BeautifulSoup
    ) -> BeautifulSoup | List:
        return parent_element.find('div','view-content').find_all(recursive=False)
    
    def get_parent_container(self) -> BeautifulSoup | List:
        return self.html.select_one('.view-firmware.view-id-firmware')    


    