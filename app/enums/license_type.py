from enum import Enum

class LicenseType(Enum):
    UNKNOWN_LICENSE = 0
    CLIENT_DOWNLOAD_LICENSE = 1
    CLIENT_SUBSCRIPTION_LICENSE = 2
    DEMO_LICENSE = 3