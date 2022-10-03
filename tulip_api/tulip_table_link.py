from .tulip_api import TulipAPI


class TulipTableLink:
    """
    An interface with Tulip Table Links.
    """

    def __init__(self, tulip_api: TulipAPI, link_id: str):
        self.tulip_api = tulip_api
        self.link_id = link_id

    def get_details(self):
        """
        GET `/tableLinks/{linkId}`

        Returns the metadata of a Tulip Table Link.
        """
        return self.tulip_api.make_request(
            self._construct_base_table_link_path(), "GET"
        )

    def link_records(self, left_record_id: str, right_record_id: str):
        """
        PUT `/tableLinks/{linkId}/link`

        Links the given records.
        """
        self.tulip_api.make_request_expect_nothing(
            self._construct_link_path(),
            "PUT",
            json={"leftRecord": left_record_id, "rightRecord": right_record_id},
        )

    def unlink_records(self, left_record_id: str, right_record_id: str):
        """
        PUT `/tableLinks/{linkId}/unlink`

        Unlinks the given records.
        """
        self.tulip_api.make_request_expect_nothing(
            self._construct_unlink_path(),
            "PUT",
            json={"leftRecord": left_record_id, "rightRecord": right_record_id},
        )

    def _construct_base_table_link_path(self):
        return f"tableLinks/{self.link_id}"

    def _construct_link_path(self):
        return f"{self._construct_base_table_link_path()}/link"

    def _construct_unlink_path(self):
        return f"{self._construct_base_table_link_path()}/unlink"
