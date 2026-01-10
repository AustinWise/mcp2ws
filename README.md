# mcp2ws

Did you just wake up from a 20 year comma? Did you build a bunch of buzzword compliant web services
back in the early 2000s and want all your [SOAP](https://en.wikipedia.org/wiki/SOAP) and
[WSDL](https://en.wikipedia.org/wiki/Web_Services_Description_Language) and
[WS-*](https://en.wikipedia.org/wiki/List_of_web_service_specifications) and
[UDDI](https://en.wikipedia.org/wiki/Web_Services_Discovery) to be relevant again?
Fear not, now you can put the smooth sheen of AI on your pile of angle brackets by exposing your
SOAP-based web service as a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server.

## Prerequisites

* Have a web service described by a WSDL file.
* Have some version of Python on your computer
* Perfect understand Python packaging and virtual environments, so you understand why you following
  the directions in this readme will break your computer. (Maybe use `uv` instead, idk)

## Installation

1. Install the required dependencies:

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

## Configure your agentic coding tool

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

## Example Session

In Gemini CLI, using the
<http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL>
service:

```
> What is the capital city of france? Use the soap tool.

✦ I will find the ISO code for France and then use it to get the capital city.

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✓  CountryISOCode (soap-service MCP Server) {"sCountryName":"France"}                                                                                                                                                                         │
│                                                                                                                                                                                                                                               │
│ FR                                                                                                                                                                                                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ I will now retrieve the capital city of France using its ISO code.

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✓  CapitalCity (soap-service MCP Server) {"sCountryISOCode":"FR"}                                                                                                                                                                             │
│                                                                                                                                                                                                                                               │
│ Paris                                                                                                                                                                                                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ The capital city of France is Paris.
```
