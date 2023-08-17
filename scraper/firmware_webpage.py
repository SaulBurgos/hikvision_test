from dataclasses import dataclass
from bs4 import BeautifulSoup
from typing import Dict, List
from datetime import datetime

@dataclass()
class FirmwareNodeHTML:
    container: BeautifulSoup = None
    header: BeautifulSoup = None
    body: BeautifulSoup = None

    def __post_init__(self):
        if self.container is not None:
            self.header, self.body = self.container.find_all(recursive=False)

    def get_info(self) -> Dict:
        last_file_url = self.get_last_file_url()
        info = {
            "model": self.get_model(),
            "status": self.get_status(),
            "last_file_url": last_file_url,
            "older_file_url": self.get_older_files(),
            "version": self.get_version(last_file_url),
            "date": self.get_date(last_file_url)
        }

        return info
    
    def get_date(self,file_url: str) -> str:
        final_date: str = "unknown"
        date_string: str = file_url.split("_")[-1]

        if len(date_string) == 0:
            return final_date
        
        date_components = date_string.split(".")

        if len(date_components) == 1:
            return final_date
        
        try:
            date = datetime.strptime(date_components[0], "%y%m%d")
            final_date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            print("incorrect formart of date:", date_components[0])
        
        return final_date
    
    def get_version(self,file_url: str) -> str:
        # assumption that it will be int he same position
        return file_url.split("_")[-2]
    
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

    def get_firmware_list(self) -> List[Dict]:
        firmware_list = []

        children = self.get_direct_children_from_parent(
            self.get_parent_container()
        )

        for child in children:
            firmware_node = FirmwareNodeHTML(container=child)
            info = firmware_node.get_info()
            firmware_list.append(info)

        return firmware_list
    
    def get_direct_children_from_parent(
        self, parent_element: BeautifulSoup
    ) -> BeautifulSoup | List:
        return parent_element.find('div','view-content').find_all(recursive=False)
    
    def get_parent_container(self) -> BeautifulSoup | List:
        return self.html.select_one('.view-firmware.view-id-firmware')    


    