"""Module containing class mixins for performing private requests."""

from __future__ import annotations

import json as jsonlib

import requests


__all__ = [
    # Class exports
    "PrivateMixin",
]


class JohnDeereSession(requests.Session):
    """Custom John Deere session."""

    def get(self, url: str, handle_pagination: bool | None = None, **kwargs):
        """Sends a GET request.

        Overrides the default `requests.Session().get()` function to allow
        for pagination internally when dealing with John Deere responses.

        Arguments:
            url: URL for the new request.
            handle_pagination: Optional argument to automate or disable
                handling of pagination based on the response.
            kwargs: Optional arguments that the request takes.

        Return:
            The response of the request.
        """
        kwargs.setdefault("allow_redirects", True)
        response = self.request("GET", url, **kwargs)

        if handle_pagination == False:
            return response

        # Handle pagination here, make sure `total` and `values` key exist
        # in the response first before even trying to handle pagination
        response.raise_for_status()
        data = response.json()
        if "total" not in data or "values" not in data:
            return response

        # Make sure the "total" value is an integer and the
        # "values" value is a list. Don't try pagination otherwise.
        try:
            total = int(data["total"])
            values = data["values"]

            if not isinstance(values, list):
                return response

        except (ValueError, TypeError):
            return response

        # Keep track of previous and current dataset
        previous_data = data
        current_data = data

        while len(values) < total:
            next_link = None
            for link in previous_data["links"]:
                if link["rel"] == "nextPage":
                    next_link = link["uri"]

            if next_link is None:
                break

            response = self.get(next_link)
            response.raise_for_status()
            current_data = response.json()

            values.extend(current_data.get("values", []))

            previous_data = current_data

        current_data["values"] = values

        response._content = jsonlib.dumps(current_data).encode()
        return response


class PrivateMixin:
    """Mixin for private requests or operations to John Deere."""

    def __init__(self, *args, **kwargs):
        self.private = JohnDeereSession()
        self.private.verify = True  # `False` to fix SSL-related errors
        self.private.headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/vnd.deere.axiom.v3+json",
        }
