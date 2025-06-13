# mcp-mail
MCP Server to Perform actions with GMail via API

# How to install
1) Create a local python virtual environment and activate it

   ```python -m venv .venv```

   ```.venv\Scripts\activate```

2) Install the libraries using the below command
```pip install -r requirements.txt```

3) Install uv for python environment

   - For Windows:

     ```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"```

   - For Linux: 

     ```curl -LsSf https://astral.sh/uv/install.sh | sh```

## Setup Google Project
Refer google documentation on how to setup project and oauth. It would generate a credentials.json. 
Save it locally, to be read by mcp-mail server
https://developers.google.com/workspace/guides/get-started 

## Try Locally

   1) From Postman
      - Open Postman
      - Create a new collection
      - Add a new MCP request
      - Choose STDIO method
      - Paste the following in the address and click Run. Update the correct the directory location

        `
        {
          "mcpServers": {
            "gmailmcp": {
              "command": "uv",
              "args": [
                "--directory",
                "D:\\Local\\vscode\\ai\\mcp-mail",
                "run",
                "mcp-mail-stdio.py"
              ]
            }
          }
        }
        `
        - Try any of the tools
          - echo()
          - login()
          - labels()
          - messages(query,label)

   2) From MCP Enabled IDE
      - Open your IDE
      - Add mcpServer configuration with correct directory location and restart IDE

        `
        {
          "mcpServers": {
            "gmailmcp": {
              "command": "uv",
              "args": [
                "--directory",
                "D:\\Local\\vscode\\ai\\mcp-mail",
                "run",
                "mcp-mail-stdio.py"
              ]
            }
          }
        }
        `

