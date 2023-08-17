from typing import Optional, List, Any
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

@dataclass_json
@dataclass
class VendorMetadata:
    product_family: str
    models: List[str]
    status: str
    os: str
    version: str
    filename: str

    landing_urls: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    firmware_urls: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    bootloader_url: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    release_notes: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    release_date: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    device_picture_urls: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    user_manual: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    fixed_cves: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    vendor_metadata: Optional[Any] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )    
    description: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    discontinued: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
