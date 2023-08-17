
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
from itertools import groupby

MANIFEST_URL = "https://us.hikvision.com/en/support-resources/firmware/"

# Complete the 'get_manifest' function below
def get_manifest(pages_with_firmwares_raw: List) -> List[VendorMetadata]:
    vendor_list: list = []

    for page_firmware in pages_with_firmwares_raw:

        for current_firmware in page_firmware.get('firmwares',[]):

            vendor = VendorMetadata(
                product_family=page_firmware.get("category",""),
                models=current_firmware.get("model",""),
                status=current_firmware.get("status",""),
                os="",
                version=current_firmware.get("version",""),
                filename=""

                # models=firmware["models"],
                # status=firmware["status"],
                # os=firmware["os"],
                # version=firmware["version"],
                # filename=firmware["filename"],
                # landing_urls=firmware["landing_urls"],
                # firmware_urls=firmware["firmware_urls"],
                # bootloader_url=firmware["bootloader_url"],
                # release_notes=firmware["release_notes"],
                # release_date=firmware["release_date"],
                # device_picture_urls=firmware["device_picture_urls"],
                # user_manual=firmware["user_manual"],
                # fixed_cves=firmware["fixed_cves"],
                # vendor_metadata=firmware["vendor_metadata"],
                # description=firmware["description"],
                # discontinued=firmware["discontinued"],
            )
            vendor_list.append(vendor)
    
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


def reorganize_firmwares(pages_with_firmwares_raw: List[Dict]) -> List[Dict]:
    result = []
    all_models = []

    for page_firmware in pages_with_firmwares_raw:
        for current_firmware in page_firmware.get('firmwares',[]):
            all_models.append({
                "file_url": current_firmware.get("last_file_url",""),
                "file_name": current_firmware.get("last_file_name",""),
                "model": current_firmware.get("model",""),
                "category": page_firmware.get("category",""),
                "version": current_firmware.get("version",""),
                "date": current_firmware.get("date",""),
                "discontinued": current_firmware.get("discontinued")
            })

    models_grouped_by_file_url = {}
    for key, group in groupby(all_models, key=lambda x: x["file_url"]):
        models_grouped_by_file_url[key] = list(group)

    for key, value in models_grouped_by_file_url.items():
        new_item_group = {
            "file_url": key,
            "models": [],
            "version": "",
            "file_name": "",
            "release_date": "",
            "discontinued": None
        }

        for item in value:
            new_item_group["models"].append(item.get("model"))
            # in theory are the same value for the same urls
            new_item_group["file_name"] = item.get("filename")
            new_item_group["version"] = item.get("version")
            new_item_group["file_name"] = item.get("file_name")
            new_item_group["release_date"] = item.get("date")
            new_item_group["discontinued"] = item.get("discontinued")

        result.append(new_item_group)

    return result

def main():
    pages_with_firmwares_raw: List[Dict] = get_all_firmwares(MANIFEST_URL)

    if len(pages_with_firmwares_raw) == 0:
        print("Error fetching firmware from manifest url")
        return

    firmwares_list_raw = reorganize_firmwares(pages_with_firmwares_raw)
    # vendor_metadata_list = get_manifest(pages_with_firmwares_raw)
    # firmwares = output_firmware(vendor_metadata_list)
    # for firmware in firmwares:
    #     print(firmware.to_json())


if __name__ == "__main__":
    main()
