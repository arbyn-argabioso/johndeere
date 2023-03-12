"""Module containing class mixins for field endpoints."""

from __future__ import annotations

from johndeere.enum import ExtendableStrEnum
from johndeere.typing import JSONLike


__all__ = [
    # Class exports
    "FieldsMixin",
    "RecordStatuses",
]


class RecordStatuses(ExtendableStrEnum):
    ALL: str = "ALL"
    ACTIVE: str = "ACTIVE"
    ARCHIVED: str = "ARCHIVED"


class FieldOperationTypes(ExtendableStrEnum):
    APPLICATION: str = "APPLICATION"
    HARVEST: str = "HARVEST"
    SEEDING: str = "SEEDING"
    TILLAGE: str = "TILLAGE"


class MeasurementTypes(ExtendableStrEnum):
    VOLUME: str = "volume"
    MASS: str = "mass"


class FieldsMixin:
    """Fields endpoint mixin."""

    def get_fields(
        self,
        org_id: int | str,
        *,
        field_name: str | None = None,
        farm_name: str | None = None,
        client_name: str | None = None,
        record_filter: str = RecordStatuses.ACTIVE.value,
        embed: str | list[str] | None = None,
    ) -> JSONLike:
        """Get the list of fields within a specified organization.

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
            JSON-dictionary containing the list of fields. Each field
            would also contain links pertaining to other resources related
            to that specific field.
        """
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

    def get_field(self, org_id: int | str, field_id: str) -> JSONLike:
        """View details on a specific field.

        Arguments:
            org_id: A String or integer ID of the organization.
            field_id: GUID string ID of the field.

        Return:
            JSON-dictionary containing details of a single field. The field
            would also contain links pertaining to other resources related
            to the specific field.
        """
        org_id = str(org_id)
        field_id = str(field_id)

        # Build complete endpoint URL
        url = self.BASE_URL / "organizations" / org_id / "fields" / field_id

        # Do private request and check for errors
        response = self.private.get(url)
        response.raise_for_status()

        return response.json()

    def get_field_operations(
        self,
        org_id: int | str,
        field_id: str,
        *,
        crop_season: int | None = None,
        operation_type: str | None = None,
        measurement_type: str | None = None,
    ) -> JSONLike:
        """Return the agronomic operations performed in a field.

        Supported field operation types include Seeding, Application, and
        Harvest. A single field operation may potentially span consecutive
        days depending on the type of operation. Each field operation may
        have one or more measurements, listed as links from the field
        operation itself.

        Arguments:
            org_id: A String or integer ID of the organization.
            field_id: GUID string ID of the field.
            crop_season: Optional integer argument representing the
                year of the crop season.
            operation_type: Optional string argument that filter results by
                field operation type. Takes the values "APPLICATION",
                "HARVEST", "SEEDING", and "TILLAGE".

        Return:
            JSON-dictionary containing details of a single field. The field
            would also contain links pertaining to other resources related
            to the specific field.
        """
        org_id = str(org_id)
        field_id = str(field_id)

        # Build complete endpoint URL
        url = self.BASE_URL / "organizations" / org_id / "fields" / field_id
        url = url / "fieldOperations"

        # Add optional parameters as URL query
        if crop_season is not None:
            url = url % {"cropSeason": str(crop_season)}

        if operation_type is not None:
            if operation_type in FieldOperationTypes:
                url = url % {"fieldOperationType": operation_type}
            else:
                raise ValueError(
                    f"Invalid field operation type: {operation_type}"
                )

        if measurement_type is not None:
            if measurement_type in MeasurementTypes:
                url = url % {"measurementTypes": measurement_type}
            else:
                raise ValueError(
                    f"Invalid measurement type: {measurement_type}"
                )

        # Do private request and check for errors
        response = self.private.get(url)
        response.raise_for_status()

        return response.json()
