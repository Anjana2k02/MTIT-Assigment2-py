import httpx
from fastapi import Request, Response

EXCLUDED_HEADERS = {"host", "content-length", "transfer-encoding"}


async def forward_request(request: Request, target_url: str) -> Response:
    body = await request.body()
    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in EXCLUDED_HEADERS
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=dict(request.query_params),
        )
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type"),
    )
