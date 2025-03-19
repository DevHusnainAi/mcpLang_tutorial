from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def calculate(expression: str) -> str:
    """Calculate the result of a mathematical expression"""
    try:
        # Using a restricted eval for safety
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")