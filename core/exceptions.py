"""
core/exceptions.py  —  Custom DRF exception handler.

Guarantees that every error response has the shape:
    {
        "success": false,
        "status_code": <int>,
        "error": "<human-readable label>",
        "detail": <str | dict | list>
    }
No stack traces are ever leaked to the client.
"""
from __future__ import annotations

import logging
from typing import Any

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_default_handler

logger = logging.getLogger(__name__)

_STATUS_LABELS: dict[int, str] = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    409: "Conflict",
    422: "Unprocessable Entity",
    429: "Too Many Requests",
    500: "Internal Server Error",
}


def _build_error_response(status_code: int, detail: Any) -> Response:
    return Response(
        {
            "success": False,
            "status_code": status_code,
            "error": _STATUS_LABELS.get(status_code, "Error"),
            "detail": detail,
        },
        status=status_code,
    )


def custom_exception_handler(exc: Exception, context: dict) -> Response | None:
    # Let DRF convert Django exceptions to APIException first
    if isinstance(exc, Http404):
        exc = APIException()
        exc.status_code = status.HTTP_404_NOT_FOUND
        exc.detail = "The requested resource was not found."  # type: ignore[assignment]
    elif isinstance(exc, DjangoPermissionDenied):
        exc = APIException()
        exc.status_code = status.HTTP_403_FORBIDDEN
        exc.detail = "You do not have permission to perform this action."  # type: ignore[assignment]

    response = drf_default_handler(exc, context)

    if response is None:
        # Unhandled server error — log it, return generic 500
        logger.exception("Unhandled server error: %s", exc)
        return _build_error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred. Please try again later.",
        )

    detail = response.data
    # Flatten single-key "detail" dicts
    if isinstance(detail, dict) and list(detail.keys()) == ["detail"]:
        detail = detail["detail"]
        if hasattr(detail, "string"):          # ErrorDetail → str
            detail = str(detail)

    return _build_error_response(response.status_code, detail)
