import hashlib
from typing import Any, Callable, Dict, Optional, Tuple

from starlette.requests import Request
from starlette.responses import Response

from core.constants import FORBIDDEN_ENDPOINT_PROP_NAMES


def custom_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    filtered_kwargs = {}
    for key, value in kwargs.items():
        if key not in FORBIDDEN_ENDPOINT_PROP_NAMES:
            filtered_kwargs[key] = value

    cache_key = hashlib.md5(  # noqa: S324
        f"{func.__module__}:{func.__name__}:{args}:{filtered_kwargs}".encode()
    ).hexdigest()
    return f"{namespace}:{cache_key}"
