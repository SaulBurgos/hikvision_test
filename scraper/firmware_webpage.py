from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from typing import Dict, List

@dataclass()
class FirmwareNodeHTML:
    container: BeautifulSoup = None
    header: BeautifulSoup = None
    body: BeautifulSoup = None

    def __post_init__(self):
        if self.container is not None:
            self.header, self.body = self.container.find_all(recursive=False)

    def get_info(self) -> Dict:
        info = {
            "model": self.get_model(),
            "status": self.get_status(),
            "last_file_url": self.get_last_file_url(),
            "older_file_url": self.get_older_files(),
            "version": None,
            "date": None
        }

        return info
    
    def get_model(self) -> str:
        return self.header.get_text().strip()
    
    def get_older_files(self) -> List:
        files = []
        label_older = self.body.find('label', text='Older Versions:')

        if label_older is not None:
            for sibling in label_older.find_next_siblings():
                files.append({
                    "file_url": sibling.find('a','firmware')['href'],
                    "file_name": sibling.find('a','firmware').get_text()
                })

        return files
    
    def get_last_file_url(self) -> str:
        parent = self.body.find('label', text='Latest Firmware:').parent
        return parent.find('a','firmware')['href']

    def get_status(self) -> str:
        result = "valid"
        if "is-discontinued-1" in self.container["class"]:
            result = "discontinued"
        
        return result


@dataclass()
class FirmwareWebPage:
    html: BeautifulSoup = None
    #NOTE: Maybe I don't want to do this like property class
    # firmware_nodes: List[FirmwareNodeHTML] = field(default_factory=lambda: [])

    def get_firmware_list(self) -> List[Dict]:
        firmware_list = []

        children = self.get_direct_children_from_parent(
            self.get_parent_container()
        )

        for child in children:
            firmware_node = FirmwareNodeHTML(container=child)
            info = firmware_node.get_info()
            print(info)
            firmware_list.append(info)


        return "I am a dictionary of firmware"
    
    def get_direct_children_from_parent(
        self, parent_element: BeautifulSoup
    ) -> BeautifulSoup | List:
        return parent_element.find('div','view-content').find_all(recursive=False)
    
    def get_parent_container(self) -> BeautifulSoup | List:
        return self.html.select_one('.view-firmware.view-id-firmware')    


    