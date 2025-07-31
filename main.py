from datetime import datetime
from zoneinfo import ZoneInfo

from fastmcp import FastMCP

# Create a server instance with a descriptive name
mcp = FastMCP(name="My First MCP Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

@mcp.tool
def get_current_datetime(timezone: str = "America/New_York") -> dict[str, str]:
    """Get current date and time in the specified timezone.
    
    Args:
        timezone: IANA timezone string (default: "America/New_York" for EST/EDT)
        
    Returns:
        Dictionary with formatted date, time, and full datetime string
    """
    now = datetime.now(ZoneInfo(timezone))
    
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "timezone": timezone,
        "iso": now.isoformat()
    }

@mcp.resource("timezones://common")
def get_common_timezones() -> str:
    """Get a list of commonly used timezones with their current times.
    
    Returns a formatted list of major timezones around the world.
    """
    common_timezones = [
        ("UTC", "Coordinated Universal Time"),
        ("America/New_York", "Eastern Time (US & Canada)"),
        ("America/Chicago", "Central Time (US & Canada)"),
        ("America/Denver", "Mountain Time (US & Canada)"),
        ("America/Los_Angeles", "Pacific Time (US & Canada)"),
        ("Europe/London", "London, Edinburgh, Dublin"),
        ("Europe/Paris", "Paris, Berlin, Amsterdam"),
        ("Europe/Moscow", "Moscow, St. Petersburg"),
        ("Asia/Dubai", "Dubai, Abu Dhabi"),
        ("Asia/Shanghai", "Beijing, Shanghai, Hong Kong"),
        ("Asia/Tokyo", "Tokyo, Seoul, Osaka"),
        ("Australia/Sydney", "Sydney, Melbourne, Brisbane"),
    ]
    
    result = ["Common Timezones and Current Times\n" + "=" * 40 + "\n"]
    
    for tz_name, description in common_timezones:
        try:
            current_time = datetime.now(ZoneInfo(tz_name))
            result.append(
                f"\n{description} ({tz_name}):\n"
                f"  Time: {current_time.strftime('%H:%M:%S')}\n"
                f"  Date: {current_time.strftime('%Y-%m-%d')}\n"
                f"  Full: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            )
        except Exception as e:
            result.append(f"\n{description} ({tz_name}): Error - {str(e)}")
    
    return "\n".join(result)

# Educational Example: MCP Prompt Decorator
# Prompts guide AI assistants by providing pre-defined user messages
# that help them understand how to use the server's tools and resources
@mcp.prompt
def business_hub_times() -> str:
    """Educational prompt example for new MCP learners.
    
    This prompt demonstrates how to create reusable message templates
    that guide AI assistants to use your MCP server's capabilities.
    
    When an AI assistant receives this prompt, it will:
    1. Understand the user wants timezone information
    2. Use the 'timezones://common' resource to get the data
    3. Format and present the results
    
    Returns:
        A natural language prompt that maps to server functionality
    """
    return "Show me the current time in all major business hubs around the world"