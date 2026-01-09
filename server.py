import argparse
import sys
import json
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
from suds.client import Client # type: ignore

def main():
    parser = argparse.ArgumentParser(description="MCP Server for SOAP Web Services")
    parser.add_argument("wsdl", help="URL of the WSDL file")
    args = parser.parse_args()

    wsdl_url = args.wsdl
    
    # Initialize FastMCP server
    mcp = FastMCP("SOAP Gateway")

    # Initialize SOAP client
    try:
        client = Client(wsdl_url)
    except Exception as e:
        print(f"Error loading WSDL: {e}", file=sys.stderr)
        sys.exit(1)

    @mcp.tool()
    def list_methods() -> str:
        """
        Lists all available methods in the SOAP web service and their signatures.
        Returns a string representation of the service description.
        """
        # suds client string representation gives a good overview of methods and types
        return str(client)

    @mcp.tool()
    def call_method(method_name: str, parameters: Dict[str, Any] = {}) -> str:
        """
        Calls a specific SOAP method with the provided parameters.
        
        Args:
            method_name: The name of the method to call (case-sensitive as per WSDL).
            parameters: A dictionary of arguments to pass to the method. 
                        Keys should match the argument names expected by the SOAP method.
        """
        try:
            service = client.service
            if not hasattr(service, method_name):
                return f"Error: Method '{method_name}' not found."
            
            method = getattr(service, method_name)
            
            # call the method with unpacked parameters
            # Note: suds handles simple types and some complex types via dicts automatically.
            # For very complex types, suds 'factory' might be needed, but simple dict mapping usually works for simple structs.
            result = method(**parameters)
            
            # Serialize result to string (suds objects are not directly JSON serializable usually)
            # We use str() or we could try to convert to dict. 
            # sudsobject_to_dict is a common utility but for now str() is safe generic fallback.
            return str(result)

        except Exception as e:
            return f"Error executing '{method_name}': {str(e)}"

    print(f"MCP Server running for WSDL: {wsdl_url}", file=sys.stderr)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
