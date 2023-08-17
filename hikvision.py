
# import json
# from pydoc import HTMLDoc
# import re
# from urllib import response
# from datetime import datetime
# import requests
# from bs4 import BeautifulSoup
from typing import List, Dict, Union, Any
from models import firmware
from models.firmware import Firmware
from models.vendor_metadata import VendorMetadata
from scraper.hikvision import get_all_firmwares

MANIFEST_URL = "https://us.hikvision.com/en/support-resources/firmware/"

# Complete the 'get_manifest' function below
def get_manifest(manifest_url: str) -> List[VendorMetadata]:
    vendor_list: list = []
    
    return vendor_list


def output_firmware(manifest: List[VendorMetadata]) -> List[Firmware]:
    vendor_firmwares = []
    url_to_fw: Dict[Any, Any] = {}

    for m in manifest:
        if m.landing_urls == None or m.landing_urls == []:
            continue
        um: Union[List[str], Any] = m.landing_urls
        if url_to_fw.get(um[0]) == None:
            url_to_fw[um[0]] = [m]
        else:
            url_to_fw[um[0]].append(m)

    for fw_url in url_to_fw.keys():
        vendor = url_to_fw[fw_url][0]
        firmware = Firmware(
            version=vendor.version,
            models=vendor.models,
            filename=vendor.filename,
            url=fw_url,
            release_date=vendor.release_date,
            release_notes=vendor.release_notes,
            discontinued=vendor.discontinued,
        )
        vendor_firmwares.append(firmware)
    return vendor_firmwares


def main():
    firmwares_raw = get_all_firmwares(MANIFEST_URL)

    if firmwares_raw is None:
        print("Error fetching firmware from manifest url")
        return

    # firmwares = output_firmware(get_manifest(MANIFEST_URL))
    # for firmware in firmwares:
    #     print(firmware.to_json())


if __name__ == "__main__":
    main()
