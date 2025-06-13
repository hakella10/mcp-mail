import asyncio

from fastmcp import FastMCP
from pydantic import Field
from datasvc import DataService

MCP_HOST = "0.0.0.0"
MCP_PORT = 8000

mcp = FastMCP(name="GmailMCP",
              instructions="Provides tools to iteract with mail server",
              json_response=True,
              mask_error_details=True)

svc = DataService()

@mcp.tool(description="Simple loopback function which echoes back the input. This is a default tool")
def echo(any : str = Field(description="Loopback Echo", default= None)):
    return svc.gecho(any)

@mcp.tool(description="login by redirecting to consent page")
def login():
    return svc.glogin()

@mcp.tool(description="Get list of folders in user's mailbox")
def labels():
    return svc.glabels()

@mcp.tool(description="Search mails with a query")
def messages(query : str = Field(description="Query Criteria. Use keywords instead of the phrases", default= ""),
             label : str = Field(description="Search within label", default= "all")):
    print(f"messages({query},{label})")
    return svc.gmessages(query=query, label=label)

"""
@mcp.tool(description="Search mail threads with a query. A thread is combination of multiple to/fro mails in the same conversation")
def threads(query : str = Field(description="Query Criteria. Use keywords instead of the phrases", default= "")):
    return svc.gthreads(query=query)
"""

async def main():
    await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())