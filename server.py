import argparse
import sys
import asyncio
from typing import Any, Dict, List
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from suds.client import Client # type: ignore

# Type mapping from XML Schema types to JSON Schema types
TYPE_MAPPING = {
    'xs:int': 'integer',
    'xs:integer': 'integer',
    'xs:long': 'integer',
    'xs:short': 'integer',
    'xs:string': 'string',
    'xs:boolean': 'boolean',
    'xs:double': 'number',
    'xs:float': 'number',
    'xs:decimal': 'number',
}

def parse_suds_methods(client: Client) -> Dict[str, List[Dict[str, str]]]:
    """
    Parses the suds client object to extract method signatures using internal data structures.
    Returns a dictionary where keys are method names and values are lists of argument definitions.
    """
    methods = {}
    
    for sd in client.sd:
        for port, port_methods in sd.ports:
            for method_name, method_args in port_methods:
                args = []
                for arg_name, arg_type, _ in method_args:
                    type_name = sd.xlate(arg_type)
                    args.append({"name": arg_name, "type": type_name})
                methods[method_name] = args
    
    return methods

def main():
    parser = argparse.ArgumentParser(description="MCP Server for SOAP Web Services")
    parser.add_argument("wsdl", help="URL of the WSDL file")
    args = parser.parse_args()

    wsdl_url = args.wsdl
    
    try:
        client = Client(wsdl_url)
    except Exception as e:
        print(f"Error loading WSDL: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse methods early to fail fast if parsing fails
    parsed_methods = parse_suds_methods(client)
    print(f"Discovered methods: {list(parsed_methods.keys())}", file=sys.stderr)

    server = Server("SOAP Gateway")

    @server.list_tools()
    async def handle_list_tools(request: types.ListToolsRequest) -> types.ListToolsResult:
        tools = []
        for name, args in parsed_methods.items():
            properties = {}
            required = []
            
            for arg in args:
                arg_name = arg['name']
                arg_type = arg['type']
                json_type = TYPE_MAPPING.get(arg_type, 'string')
                
                properties[arg_name] = {"type": json_type}
                required.append(arg_name)
            
            tool = types.Tool(
                name=name,
                description=f"SOAP method: {name}",
                inputSchema={
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            )
            tools.append(tool)
            
        return types.ListToolsResult(tools=tools)

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name not in parsed_methods:
            raise ValueError(f"Unknown tool: {name}")

        try:
            service = client.service
            method = getattr(service, name)
            
            # Execute SOAP call
            # Arguments are passed as kwargs. 
            # Note: suds expects arguments in order or as kwargs matching names.
            # Our parsing extracted names so kwargs should work.
            result = method(**(arguments or {}))
            
            return [types.TextContent(type="text", text=str(result))]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error executing {name}: {str(e)}")]

    async def run_server():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
