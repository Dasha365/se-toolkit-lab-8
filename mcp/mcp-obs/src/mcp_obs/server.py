import os
import httpx
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-obs")

VICTORIALOGS_URL = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
VICTORIATRACES_URL = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")


@mcp.tool()
async def logs_search(query: str, limit: int = 20) -> str:
    """Search logs using LogsQL query. Example: '_time:1h service.name:"Learning Management Service" severity:ERROR'"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{VICTORIALOGS_URL}/select/logsql/query",
            params={"query": query, "limit": limit},
            timeout=10
        )
        resp.raise_for_status()
        lines = resp.text.strip().split("\n")
        results = []
        for line in lines[:limit]:
            if line:
                try:
                    results.append(json.loads(line))
                except Exception:
                    results.append({"_msg": line})
        return json.dumps(results, indent=2)


@mcp.tool()
async def logs_error_count(service: str = "Learning Management Service", time_window: str = "1h") -> str:
    """Count errors per service over a time window."""
    query = f'_time:{time_window} service.name:"{service}" severity:ERROR'
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{VICTORIALOGS_URL}/select/logsql/query",
            params={"query": query, "limit": 1000},
            timeout=10
        )
        resp.raise_for_status()
        lines = [l for l in resp.text.strip().split("\n") if l]
        return json.dumps({"service": service, "time_window": time_window, "error_count": len(lines)})


@mcp.tool()
async def traces_list(service: str = "Learning Management Service", limit: int = 10) -> str:
    """List recent traces for a service."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{VICTORIATRACES_URL}/select/jaeger/api/traces",
            params={"service": service, "limit": limit},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        traces = []
        for trace in data.get("data", []):
            spans = trace.get("spans", [])
            traces.append({
                "traceID": trace.get("traceID"),
                "spans": len(spans),
                "duration": max((s.get("duration", 0) for s in spans), default=0),
                "operations": list(set(s.get("operationName", "") for s in spans))[:3]
            })
        return json.dumps(traces, indent=2)


@mcp.tool()
async def traces_get(trace_id: str) -> str:
    """Fetch a specific trace by ID."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{trace_id}",
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        traces = data.get("data", [])
        if not traces:
            return json.dumps({"error": "trace not found"})
        trace = traces[0]
        spans = trace.get("spans", [])
        summary = []
        for span in spans:
            tags = {t["key"]: t["value"] for t in span.get("tags", [])}
            summary.append({
                "operation": span.get("operationName"),
                "duration_us": span.get("duration"),
                "error": tags.get("error", False),
                "status": tags.get("http.status_code")
            })
        return json.dumps({"traceID": trace_id, "spans": summary}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
