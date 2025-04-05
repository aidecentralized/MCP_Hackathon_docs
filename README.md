# MCP Python SDK Documentation

This repository contains the documentation for the Model Context Protocol (MCP) Python SDK. It is built using Sphinx and the Read the Docs theme.

## Overview

The Model Context Protocol (MCP) is an open standard that defines how applications interact with large language models (LLMs). This documentation aims to help developers:

- Understand the core concepts of MCP
- Build MCP servers to expose resources, tools, and prompts
- Create MCP clients to connect to MCP servers
- Explore advanced topics and best practices

## FastMCP

Our documentation includes comprehensive coverage of FastMCP, a high-level, Pythonic interface for building MCP servers. Originally a standalone project, FastMCP has been integrated into the official MCP Python SDK. It provides a developer-friendly way to create MCP servers with minimal boilerplate:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

The SDK provides multiple ways to run your server:
- Development mode with the MCP Inspector
- Claude Desktop integration
- Direct execution for custom deployments

## Building the Documentation

1. **Install Dependencies**

   First, make sure you have Python installed. Then, install the required packages:

   ```bash
   # Using conda (recommended)
   conda activate cuda_test
   pip install -r requirements.txt
   
   # Or using pip in a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Build the Documentation**

   To build the documentation:

   ```bash
   make html
   ```

   The built documentation will be in the `_build/html/` directory.

3. **Live Preview**

   For a live preview with auto-reload:

   ```bash
   sphinx-autobuild . _build/html
   ```

   Then open your browser to http://localhost:8000.

## Hosting on GitHub Pages

You can host this documentation on GitHub Pages by following these steps:

1. **Create a GitHub Repository**

   ```bash
   # Initialize a local repository if you haven't already
   git init
   git add .
   git commit -m "Initial commit with MCP documentation"
   
   # Create a repository on GitHub through the web interface
   # Then add the remote and push
   git remote add origin https://github.com/yourusername/mcp_docs.git
   git push -u origin main
   ```

2. **Set Up GitHub Pages**

   There are two ways to set up GitHub Pages for your documentation:

   ### Option 1: Using GitHub Actions (Recommended)

   The repository already includes a GitHub Actions workflow at `.github/workflows/docs.yml` that will automatically build and deploy the documentation to GitHub Pages whenever you push to the main branch.

   1. Go to your GitHub repository
   2. Navigate to "Settings" > "Pages"
   3. Under "Source", select "GitHub Actions"
   4. Make sure the "GitHub Actions" workflow is running after your first push

   ### Option 2: Manual Setup with gh-pages Branch

   If you prefer to manage the deployment manually:

   ```bash
   # Create an orphan gh-pages branch
   git checkout --orphan gh-pages
   git rm -rf .
   touch .nojekyll
   git add .nojekyll
   git commit -m "Initial gh-pages commit"
   git push origin gh-pages
   git checkout main
   
   # Build and copy the documentation to gh-pages
   make html
   git checkout gh-pages
   cp -r _build/html/* .
   git add .
   git commit -m "Update documentation"
   git push origin gh-pages
   git checkout main
   ```

   Then go to your GitHub repository's Settings > Pages and select the gh-pages branch as the source.

3. **Access Your Documentation**

   Your documentation will be available at:
   `https://yourusername.github.io/mcp_docs/`

4. **Update the Documentation**

   Whenever you want to update the documentation:

   ```bash
   # If using GitHub Actions
   # Just push your changes to the main branch
   git add .
   git commit -m "Update documentation"
   git push origin main
   
   # If using manual gh-pages setup
   make html
   git checkout gh-pages
   cp -r _build/html/* .
   git add .
   git commit -m "Update documentation"
   git push origin gh-pages
   git checkout main
   ```

## Documentation Structure

- `index.rst`: Main entry point
- `introduction.rst`: Introduction to MCP
- `getting-started.rst`: Getting started guide
- `server-guide.rst`: Guide for building MCP servers
- `client-guide.rst`: Guide for building MCP clients
- `examples.rst`: Example MCP applications
- `advanced-topics.rst`: Advanced MCP concepts
- `api-reference.rst`: API reference

## Contributing

Contributions to improve the documentation are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes
4. Build the documentation to verify your changes
5. Submit a pull request

## Resources

- [Official MCP Website](https://modelcontextprotocol.io/)
- [MCP Python SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Officially Supported Servers](https://github.com/modelcontextprotocol/servers)
- [GitHub Discussions](https://github.com/modelcontextprotocol/python-sdk/discussions)
- [FastMCP GitHub (Legacy)](https://github.com/jlowin/fastmcp)

## License

This documentation is licensed under the MIT License - see the LICENSE file for details. 