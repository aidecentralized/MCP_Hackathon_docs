Getting Started with MCP Python SDK
===============================

This guide will help you get started with the MCP Python SDK, which allows you to build MCP servers and clients in Python.

Installation
-----------

There are several ways to install the MCP Python SDK:

Using uv (Recommended)
^^^^^^^^^^^^^^^^^^^^^

We strongly recommend using `uv <https://docs.astral.sh/uv/>`_ to install and manage the MCP SDK, especially when deploying servers:

.. code-block:: bash

   # Install uv if you don't have it
   curl -sSf https://astral.sh/uv/install.sh | sh

   # Install MCP with uv
   uv pip install "mcp[cli]"

On macOS, you may need to install uv with Homebrew to make it available to Claude Desktop:

.. code-block:: bash

   brew install uv

Using pip
^^^^^^^^

You can also use pip to install the MCP SDK:

.. code-block:: bash

   pip install "mcp[cli]"

Adding MCP to your Python project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have a uv-managed project, add MCP to your dependencies:

.. code-block:: bash

   uv init mcp-server-demo
   cd mcp-server-demo
   uv add "mcp[cli]"

For pip-managed projects:

.. code-block:: bash

   pip install "mcp[cli]"

Running the MCP command line tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run the mcp command:

.. code-block:: bash

   # With uv
   uv run mcp

   # With pip
   mcp

Learning Resources
-----------------

The following resources provide excellent practical examples for getting started with MCP server development:

Official MCP Weather Server Tutorial
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div style="margin-bottom: 20px;">
   <iframe src="https://modelcontextprotocol.io/quickstart/server" style="width: 100%; height: 500px; border: 1px solid #ddd; border-radius: 5px;"></iframe>
   </div>

This official tutorial walks you through building a weather API server that connects to Claude Desktop.

Basic Python MCP Server Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div style="margin-bottom: 20px;">
   <iframe width="100%" height="400" src="https://www.youtube.com/embed/wa_A0qY0anA" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>

This video demonstrates how to create a simple MCP server for counting occurrences of the letter 'r' in words, with insights on integrating with Claude Desktop.

MCP Server with Cursor AI Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div style="margin-bottom: 20px;">
   <iframe width="100%" height="400" src="https://www.youtube.com/embed/L94WBLL0KjY?start=438" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>

This tutorial explains how to build an MCP server and integrate it with the Cursor AI code editor.

Quickstart
---------

Let's create a simple MCP server that exposes a calculator tool and some data:

.. code-block:: python

   # server.py
   from mcp.server.fastmcp import FastMCP

   # Create an MCP server
   mcp = FastMCP("Demo")


   # Add an addition tool
   @mcp.tool()
   def add(a: int, b: int) -> int:
       """Add two numbers"""
       return a + b


   # Add a dynamic greeting resource
   @mcp.resource("greeting://{name}")
   def get_greeting(name: str) -> str:
       """Get a personalized greeting"""
       return f"Hello, {name}!"

Running Your Server
-----------------

There are several ways to run your MCP server:

Development Mode (Testing & Debugging)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The fastest way to test and debug your server is with the MCP Inspector:

.. code-block:: bash

   mcp dev server.py

This launches a web interface where you can:
- Test your tools and resources interactively
- See detailed logs and error messages
- Monitor server performance
- Set environment variables for testing

During development, you can:

.. code-block:: bash

   # Add dependencies
   mcp dev server.py --with pandas --with numpy

   # Mount local code for live updates
   mcp dev server.py --with-editable .

Claude Desktop Integration (Regular Use)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For regular use with Claude, install your server in Claude Desktop:

.. code-block:: bash

   mcp install server.py

Your server will run in an isolated environment with:

.. code-block:: bash

   # Custom name
   mcp install server.py --name "My Analytics Server"

   # Environment variables (individual)
   mcp install server.py -e API_KEY=abc123 -e DB_URL=postgres://...
   
   # Environment variables (from file)
   mcp install server.py -f .env

Direct Execution (Advanced)
^^^^^^^^^^^^^^^^^^^^^^^^

For advanced scenarios like custom deployments:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("My App")

   if __name__ == "__main__":
       mcp.run()

Run it with:

.. code-block:: bash

   python server.py
   # or
   mcp run server.py

Finding Your Server Object
^^^^^^^^^^^^^^^^^^^^^^^^

MCP commands look for a server object called ``mcp``, ``app``, or ``server`` in your file. For custom object names:

.. code-block:: bash

   # Using a standard name
   mcp run server.py

   # Using a custom name
   mcp run server.py:my_custom_server

Next Steps
---------

Now that you have a basic server running, continue to these sections:

* :doc:`server-guide` - Learn more about building MCP servers
* :doc:`client-guide` - Learn how to build clients that connect to MCP servers
* :doc:`examples` - Explore more complex examples 