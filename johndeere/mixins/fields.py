"""Module containing class mixins for field endpoints."""

from __future__ import annotations

from johndeere import enum


__all__ = [
    # Class exports
    "FieldsMixin",
    "RecordStatuses",
]


class RecordStatuses(enum.ExtendableStrEnum):
    ALL: str = "ALL"
    ACTIVE: str = "ACTIVE"
    ARCHIVED: str = "ARCHIVED"


class FieldsMixin:
    """Fields endpoint mixin."""

    def get_fields(self,
        org_id: int | str,
        field_name: str | None = None,
        farm_name: str | None = None,
        client_name: str | None = None,
        record_filter: str = RecordStatuses.ACTIVE.value,
        embed: str | list[str] | None = None,
    ):
        """View a list of fields within a specified organization.

        Arguments:
            org_id: A String or integer ID of the organization.
            field_name: Optional string argument to filter fields by name.
            farm_name: Optional string argument to filter fields by farm.
            client_name: Optional string argument to filter fields by
                client.
            record_filter: Optional string argument to filter fields by
                their record status. Possible values are: "ACTIVE", "ALL",
                and "ARCHIVED". Default is "ACTIVE".

        Raises:
            ValueError: Raised if the provided `record_filter` is unknown.

        Return:
            JSON-dictionary containing the list of fields.
            For each field, the response will contain links to the
            following resources:

            - boundaries: View the boundaries of this field.
            - clients: View the clients belonging to this field.
            - farms: View the farms within this field.
            - owningOrganization: View details on the owning organization.
            - activeBoundary: View the details of the active boundary.
        """

        # Make sure the organization ID is a string since it can be an
        # integer or a string which yarl URL don't work well with
        org_id = str(org_id)

        # Build complete endpoint URL
        url = self.BASE_URL / "organizations" / org_id / "fields"

        # Add optional parameters as URL query
        if field_name is not None:
            url = url % {"fieldName": field_name}
        if farm_name is not None:
            url = url % {"farmName": farm_name}
        if client_name is not None:
            url = url % {"clientName": client_name}
        if record_filter in RecordStatuses:
            url = url % {"recordFilter": record_filter}
        else:
            raise ValueError(f"Invalid record status: {record_filter}")

        # Include all embeds
        url = url % {"embed": "clients,farms,boundaries"}

        # Do private request and check for errors
        response = self.private.get(url)
        response.raise_for_status()

        return response.json()

    def get_field(self, org_id: int | str, field_id: str):
        """View details on a specific field.

        Arguments:
            org_id: A String or integer ID of the organization.
            field_id: GUID string ID of the field.

        Return:
            JSON-dictionary containing details of a single field.
            For the field, the response will link to the following
            resources:

            - boundaries: View the boundaries of this field.
            - clients: View the clients belonging to this field.
            - farms: View the farms within this field.
            - owningOrganization: View details on the owning organization.
            - activeBoundary: View the details of the active boundary.
        """
        org_id = str(org_id)
        field_id = str(field_id)

        # Build complete endpoint URL
        url = self.BASE_URL / "organizations" / org_id / "fields" / field_id

        # Do private request and check for errors
        response = self.private.get(url)
        response.raise_for_status()

        return response.json()
