"""Gets WiFi information"""
import re
from .scripts.helpers import syscommand


class Addon:
    """Addon module"""

    def __init__(self, lnxlink):
        """Setup addon"""
        self.name = "WiFi"

    def exposed_controls(self):
        """Exposes to home assistant"""
        return {
            "WiFi": {
                "type": "sensor",
                "icon": "mdi:wifi",
                "unit": "%",
                "entity_category": "diagnostic",
                "state_class": "measurement",
                "value_template": "{{ value_json.signal }}",
                "attributes_template": "{{ value_json.attributes | tojson }}",
            },
        }

    def get_info(self):
        """Gather information from the system"""
        wireless_info, _, _ = syscommand("cat /proc/net/wireless")
        match = re.findall(r"\s+(\S+):\s\S+\s+\S+\s+(\S+)", wireless_info)
        interface = ""
        ssid = ""
        mac = ""
        signal = 0
        if match:
            interface = match[0][0]
            rssi = float(match[0][1])
            signal = min(2 * (100 + rssi), 100)
            ssid, _, _ = syscommand("iwgetid -r")
            mac, _, _ = syscommand("iwgetid -ra")

        return {
            "signal": signal,
            "attributes": {
                "interface": interface,
                "ssid": ssid,
                "mac": mac,
            },
        }