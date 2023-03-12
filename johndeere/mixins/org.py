"""Module containing class mixins for organization endpoints."""

from __future__ import annotations

from johndeere.typing import JSONLike

__all__ = [
    # Class exports
    "OrganizationsMixin",
]


class OrganizationsMixin:
    """Organizations endpoint mixin."""

    def get_organizations(
        self,
        *,
        username: str | None = None,
        org_id: int | str | None = None,
        org_name: str | None = None,
    ) -> JSONLike:
        """Get the list of organizations connected to the access token.

        Arguments:
            username: Optional string argument to get all the organizations
                of which a particular user is a member.
            org_id: Optional string or integer ID of the organization. If
                provided, this function returns the specific organization.
            org_name: Optional string argument to used as a string match
                to filter the organizations by their name.

        Return:
            JSON-dictionary containing the list of organizations. Each org
            would also contain links pertaining to other resources related
            to that specific org.
        """

        # Build complete endpoint URL
        url = self.BASE_URL / "organizations"

        # Add optional parameters as URL query
        if username is not None:
            url = url % {"userName": username}
        if org_id is not None:
            url = url % {"orgId": str(org_id)}

        # Do private request and check for errors
        response = self.private.get(url)
        response.raise_for_status()

        return response.json()

    def get_organization(self, org_id: int | str) -> JSONLike:
        """Get a specific organization connected to the access token.

        Arguments:
            org_id: A string or integer ID of the organization. If
                provided, this function returns the specific organization.

        Return:
            JSON-dictionary containing details of a single organization.
            The organization response would also contain links pertaining
            to other resources related to the specific organization.

        """
        org_id = str(org_id)

        # Build complete endpoint URL
        url = self.BASE_URL / "organizations" / org_id

        # Do private request and check for errors
        response = self.private.get(url)
        response.raise_for_status()

        return response.json()
