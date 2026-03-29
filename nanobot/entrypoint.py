import json
import os

config_path = "/app/nanobot/config.json"
resolved_path = "/tmp/config.resolved.json"
workspace = "/app/nanobot/workspace"
python_bin = "/app/.venv/bin/python"
nanobot_bin = "/app/.venv/bin/nanobot"

with open(config_path) as f:
    config = json.load(f)

# LLM provider
config["providers"]["custom"]["apiKey"] = os.environ.get("LLM_API_KEY", "")
config["providers"]["custom"]["apiBase"] = os.environ.get("LLM_API_BASE_URL", "")
config["agents"]["defaults"]["model"] = os.environ.get("LLM_API_MODEL", "coder-model")

# Gateway
config["gateway"]["host"] = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
config["gateway"]["port"] = int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790"))

# MCP LMS
config["tools"]["mcpServers"]["lms"]["command"] = python_bin
config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = os.environ.get("NANOBOT_LMS_API_KEY", "")

# MCP Observability
config["tools"]["mcpServers"]["obs"] = {
    "command": python_bin,
    "args": ["-m", "mcp_obs"],
    "env": {
        "NANOBOT_VICTORIALOGS_URL": os.environ.get("NANOBOT_VICTORIALOGS_URL", ""),
        "NANOBOT_VICTORIATRACES_URL": os.environ.get("NANOBOT_VICTORIATRACES_URL", "")
    }
}

# Webchat channel
webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
webchat_port = int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765"))
access_key = os.environ.get("NANOBOT_ACCESS_KEY", "")
config["channels"]["webchat"]["host"] = webchat_host
config["channels"]["webchat"]["port"] = webchat_port
config["channels"]["webchat"]["accessKey"] = access_key

# MCP webchat
webchat_url = f"http://{webchat_host}:{webchat_port}"
config["tools"]["mcpServers"]["webchat"] = {
    "command": python_bin,
    "args": ["-m", "mcp_webchat"],
    "env": {
        "MCP_WEBCHAT_URL": webchat_url,
        "MCP_WEBCHAT_TOKEN": access_key
    }
}

with open(resolved_path, "w") as f:
    json.dump(config, f, indent=2)

os.execv(nanobot_bin, [nanobot_bin, "gateway", "--config", resolved_path, "--workspace", workspace])
