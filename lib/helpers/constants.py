from enum import StrEnum

VENDOR_MODEL_TYPE = "vendor.model"

CURRENCIES = {
    "RUB": "RUR"
}

class ProductOfferFields(StrEnum):
    ID = "id"
    NAME = "name"
    DESCRIPTION = "description"
    SHORT_DESCRIPTION = "short_description"
    PRICE = "price"
    PICTURE = "picture"
    URL = "url"
