# db_server.py
import sys
import os
import traceback
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from db_integration import create_record, read_records, update_record, delete_record
from dotenv import load_dotenv

class DatabaseServer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize MCP Server
        self.mcp = FastMCP("neon_db_server")
        print("MCP Server initialized", file=sys.stderr)
        
        # Register MCP tools
        self._register_tools()
    
    def _register_tools(self):
        """Register MCP tools for database CRUD operations."""
        @self.mcp.tool()
        async def create(table: str, data: dict) -> Dict[str, Any]:
            """Create a new record in the specified table."""
            print(f"Creating record in table '{table}'", file=sys.stderr)
            try:
                result = create_record(table, data)
                if "error" not in result:
                    print(f"Successfully created record in {table}", file=sys.stderr)
                else:
                    print(f"Failed to create record: {result['error']}", file=sys.stderr)
                return result
            except Exception as e:
                print(f"Error in create tool: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return {"error": str(e)}

        @self.mcp.tool()
        async def read(table: str, condition: str = "", params: List[Any] = []) -> List[Dict[str, Any]]:
            """Read records from the specified table."""
            print(f"Reading from table '{table}' with condition '{condition}'", file=sys.stderr)
            try:
                result = read_records(table, condition if condition else None, tuple(params))
                if not any("error" in r for r in result):
                    print(f"Successfully read {len(result)} records from {table}", file=sys.stderr)
                else:
                    print(f"Failed to read records: {result[0]['error']}", file=sys.stderr)
                return result
            except Exception as e:
                print(f"Error in read tool: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return [{"error": str(e)}]

        @self.mcp.tool()
        async def update(table: str, data: dict, condition: str, params: List[Any]) -> Dict[str, Any]:
            """Update a record in the specified table."""
            print(f"Updating record in table '{table}' with condition '{condition}'", file=sys.stderr)
            try:
                result = update_record(table, data, condition, tuple(params))
                if "error" not in result:
                    print(f"Successfully updated record in {table}", file=sys.stderr)
                else:
                    print(f"Failed to update record: {result['error']}", file=sys.stderr)
                return result
            except Exception as e:
                print(f"Error in update tool: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return {"error": str(e)}

        @self.mcp.tool()
        async def delete(table: str, condition: str, params: List[Any]) -> Dict[str, Any]:
            """Delete a record from the specified table."""
            print(f"Deleting record from table '{table}' with condition '{condition}'", file=sys.stderr)
            try:
                result = delete_record(table, condition, tuple(params))
                if "error" not in result:
                    print(f"Successfully deleted record from {table}", file=sys.stderr)
                else:
                    print(f"Failed to delete record: {result['error']}", file=sys.stderr)
                return result
            except Exception as e:
                print(f"Error in delete tool: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return {"error": str(e)}

    def run(self):
        """Start the MCP server."""
        try:
            print("Running MCP Server for Neon Database...", file=sys.stderr)
            self.mcp.run(transport="stdio")
        except Exception as e:
            print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    db_server = DatabaseServer()
    db_server.run()