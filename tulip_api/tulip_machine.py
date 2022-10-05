from typing import Any, Dict

from .tulip_api import TulipAPI


class TulipMachine:
    """
    An interface with the machine event reporting api.
    """

    attributes_report_path: str = "attributes/report"

    def __init__(self, tulip_api: TulipAPI, machine_id: str):
        self.tulip_api = tulip_api
        self.machine_id = machine_id

    def send_event(self, attributes: Dict[str, Any]):
        """
        POST `/attributes/report`

        `attributes`: A dict with attributeId: value pairs.
        ```
        {
            "attributeIdA": "valueA",
            "attributeIdB": "valueB",
        }
        ```
        """
        self.tulip_api.make_request_expect_nothing(
            TulipMachine.attributes_report_path,
            "POST",
            json=self._construct_attributes(attributes),
        )

    def _construct_attributes(self, attributes: Dict[str, Any]):
        return {
            "attributes": [
                {"machineId": self.machine_id, "attributeId": key, "value": value}
                for key, value in attributes.items()
            ]
        }
