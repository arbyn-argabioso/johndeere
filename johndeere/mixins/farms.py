"""Module containing class mixins for farms endpoints."""

from __future__ import annotations

from johndeere.enum import ExtendableStrEnum
from johndeere.mixins.commons import RecordStatuses
from johndeere.typing import JSONLike


__all__ = [
    # Class exports
    "FarmsMixin",
]


class FarmsMixin:
    """Farms endpoint mixin."""

    def get_farms(
        self,
        org_id: int | str,
        *,
        client_id: str | None = None,
        record_filter: str = RecordStatuses.ACTIVE.value,
    ) -> JSONLike:
        """Get the list of farms within a specified organization.

        Arguments:
            org_id: A String or integer ID of the organization.
            client_id: Optional string argument to filter farms by
                client.
            record_filter: Optional string argument to filter clients by
                their record status. Possible values are: "ACTIVE", "ALL",
                and "ARCHIVED". Default is "ACTIVE".

        Raises:
            ValueError: Raised if the provided `record_filter` is unknown.

        Return:
            JSON-dictionary containing the list of clients. Each client
            would also contain links pertaining to other resources related
            to that specific client.
        """
        org_id = str(org_id)

        if client_id is not None:
            url = self.BASE_URL / "organizations" / org_id / "clients"
            url = url / str(client_id) / "farms"
        else:
            url = self.BASE_URL / "organizations" / org_id / "farms"

            # Add optional parameters as URL query
            if record_filter in RecordStatuses:
                url = url % {"recordFilter": record_filter}
            else:
                raise ValueError(f"Invalid record status: {record_filter}")

            # Include all embeds
            url = url % {"embed": "showRecordMetadata"}

        # Do private request and check for errors
        response = self.private.get(url)
        response.raise_for_status()

        return response.json()
