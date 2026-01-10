# mcp2ws

Did you just wake up from a 20 year coma? Did you build a bunch of buzzword compliant web services
back in the early 2000s and want all your [SOAP](https://en.wikipedia.org/wiki/SOAP) and
[WSDL](https://en.wikipedia.org/wiki/Web_Services_Description_Language) and
to be relevant again?
Fear not, now you can put the smooth sheen of AI on your pile of angle brackets by exposing your
SOAP-based web service as a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server.

## Prerequisites

* Have a web service described by a WSDL file.
* Have a compatible version of Python (tested with 3.13) or [`uv`](https://docs.astral.sh/uv/) installed on your computer.

## Running

With `uv`:

```bash
uv run main.py
```

With regular python:

```
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Usage

To start the MCP server, run the `main.py` script with the URL of the WSDL file you want to access.

```bash
uv run main.py <WSDL_URL>
```

For example, if you have a WSDL at `http://www.dneonline.com/calculator.asmx?wsdl`:

```bash
uv run main.py http://www.dneonline.com/calculator.asmx?wsdl
```

This tool has been tested with these ran WSDL files I found on the internet:

* http://www.dneonline.com/calculator.asmx?wsdl
* http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL

## Configure your agentic coding tool

Configure your MCP client (e.g., Gemini CLI, or an IDE extension) to run this script.

**Example generic MCP config:**

```json
{
  "mcpServers": {
    "soap-service": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/mcp2ws/",
        "/path/to/mcp2ws/main.py",
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
> What is the capital city of France? Use the soap tool.

✦ I will find the ISO code for France and then use it to get the capital city.

╭────────────────────────────────────────────────────────────────────────╮
│ ✓  CountryISOCode (soap-service MCP Server) {"sCountryName":"France"}  │
│                                                                        │
│ FR                                                                     │
╰────────────────────────────────────────────────────────────────────────╯
✦ I will now retrieve the capital city of France using its ISO code.
╭────────────────────────────────────────────────────────────────────────╮
│ ✓  CapitalCity (soap-service MCP Server) {"sCountryISOCode":"FR"}      │
│                                                                        │
│ Paris                                                                  │
╰────────────────────────────────────────────────────────────────────────╯
✦ The capital city of France is Paris.
```

## TODO

* Better support for mapping XML schema to JSON schema. Currently only primitive types are supported.
* Implement support for more of fun web service standards like
  [WS-*](https://en.wikipedia.org/wiki/List_of_web_service_specifications) and
  [UDDI](https://en.wikipedia.org/wiki/Web_Services_Discovery).
  This probably won't happen because this stops being a fun joke and starts being a job.
