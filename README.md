# MCP SOAP Gateway

This is an MCP (Model Context Protocol) server that acts as a gateway to SOAP-based web services. It uses `suds` to communicate with the SOAP service and `mcp` to expose the functionality to an MCP client (like an LLM).

## Prerequisites

- Python 3.10+
- `pip`

## Installation

1.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the MCP server, run the `server.py` script with the URL of the WSDL file you want to access.

```bash
python server.py <WSDL_URL>
```

For example, if you have a WSDL at `http://example.com/service?wsdl`:

```bash
python server.py http://example.com/service?wsdl
```

## Available Tools

The server exposes the following tools to the MCP client:

-   `list_methods()`: Returns a description of the available methods and types in the SOAP service.
-   `call_method(method_name, parameters)`: Calls a specific SOAP method. `parameters` should be a dictionary where keys match the argument names of the SOAP method.

## Connection

Configure your MCP client (e.g., Claude Desktop, or an IDE extension) to run this script.

**Example generic MCP config:**

```json
{
  "mcpServers": {
    "soap-service": {
      "command": "python",
      "args": [
        "/path/to/server.py",
        "http://example.com/service?wsdl"
      ]
    }
  }
}
```
