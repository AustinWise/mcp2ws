# MCP SOAP Gateway

This is an MCP (Model Context Protocol) server that acts as a gateway to SOAP-based web services. It uses `suds` to communicate with the SOAP service and `mcp` to expose the functionality to an MCP client (like an LLM).

NOTE: this code is absolute garbage and should not be used. It currently calls `str()` on the parsed
WSDL object and then use regexes to parse the output. But it *does* work...

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

For example, if you have a WSDL at `http://www.dneonline.com/calculator.asmx?wsdl`:

```bash
python server.py http://www.dneonline.com/calculator.asmx?wsdl
```

## Available Tools

Each web service method will be available as a tool.

## Connection

Configure your MCP client (e.g., Gemini CLI, or an IDE extension) to run this script.

**Example generic MCP config:**

```json
{
  "mcpServers": {
    "soap-service": {
      "command": "python",
      "args": [
        "/path/to/server.py",
        "http://www.dneonline.com/calculator.asmx?wsdl"
      ]
    }
  }
}
```
http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL
