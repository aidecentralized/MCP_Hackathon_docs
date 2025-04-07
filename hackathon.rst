Hackathon: MCP Weather Server Setup
=================================

This guide will help you quickly get started with adding a basic MCP server to Claude Desktop.
This workshop will introduce you to adding MCP servers to Claude and using them effectively.

Prerequisites Part 1
------------------

We will be using Claude Desktop for this Hackathon/Workshop as it is the simplest client to connect with MCP servers.

* `Claude Desktop <https://claude.ai/download>`_ - Currently available on Windows and MacOS only
* `Node.js <https://nodejs.org/en/download>`_ - Required for installing the weather server example

.. note::
   Make sure you don't exhaust your token limit on Claude Desktop or you might have to wait for a while.

For a step-by-step visual guide, you can watch the following tutorial:
`Claude Desktop Tutorial <https://youtu.be/7TtuiNnhwmM>`_

This example is taken from the `mcp-weather-server <https://socket.dev/npm/package/@h1deya/mcp-server-weather>`_ package.

To install the weather server example, run the following command:

.. code-block:: bash

   npm i @h1deya/mcp-server-weather

Adding the Server to Claude Desktop
--------------------------------

1. Open Claude Desktop (On Windows, run as Administrator)
2. Click on the "Files" tab in the top left
3. Click on the "Settings" menu item
4. Click on the "Developer" option
5. Click on the "Edit Config" button to open the JSON configuration file
6. Copy and paste the following configuration:

.. code-block:: json

    {
      "mcpServers": {
        "weather": {
          "command": "npx",
          "args": [
            "-y",
            "@h1deya/mcp-server-weather"
          ]
        }
      }
    }

.. note::
   You might need to restart Claude Desktop to see the hammer icon in the chat interface, indicating that your MCP server is detected.
   You can verify the server status in the "Files/Settings/Developer" menu - "active" means the server is running and available.

Testing the Weather Server
------------------------

You can now use the weather server in your chat. Try asking:

.. code-block:: bash

   What is the weather in Boston?

.. note::
   This example uses a public government API that is currently functional in the US only.

Hackathon: Docker SQLite Database Server
======================================

In this part, we will set up a SQLite database server using Docker.

Prerequisites Part 2
------------------

* `Docker <https://docs.docker.com/engine/install/>`_ - Install and verify it's running as per the documentation

We will be using the SQLite server from the official MCP servers repository:
`MCP SQLite Server <https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite>`_

Clone the repository and navigate to the SQLite folder:

.. code-block:: bash

   git clone https://github.com/modelcontextprotocol/servers.git 
   cd servers/src/sqlite

Build the Docker image:

.. code-block:: bash

   docker build -t mcp/sqlite .

Adding the SQLite Server to Claude Desktop
---------------------------------------

1. Open Claude Desktop (On Windows, run as Administrator)
2. Click on the "Files" tab in the top left
3. Click on the "Settings" menu item
4. Click on the "Developer" option
5. Click on the "Edit Config" button to open the JSON configuration file
6. Update the configuration file with the following content for Windows:

.. code-block:: json

   {
     "mcpServers": {
       "weather": {
         "command": "npx",
         "args": [
           "-y",
           "@h1deya/mcp-server-weather"
         ]
       },
       "sqlite": {
         "command": "docker",
         "args": [
           "run",
           "--rm",
           "-i",
           "-v",
           "mcp-test:/mcp",
           "mcp/sqlite",
           "--db-path",
           "/mcp/test.db"
         ]
       }
     }
   }

Using the SQLite Server
---------------------

You can now use the SQLite server in your chat. Try the following prompts:

Basic Example:

.. code-block:: bash

   1) Create bakery DB tables:
   - ingredients (id, name, unit, quantity, cost, supplier, min_order_quantity)

   2) Populate with:
   - 10 ingredients with MOQs

   3) Add queries for:
   - Low stock alerts

Create a dashboard visualization:

.. code-block:: bash

   Let's create a simple dashboard to visualize the low stock alerts

Advanced Example (More Comprehensive):

.. code-block:: bash

   1) Create bakery DB tables:
   - ingredients (id, name, unit, quantity, cost, supplier, min_order_quantity)
   - products (id, name, price, category, available)
   - recipes (product_id, ingredient_id, quantity)
   - suppliers (id, name, contact)
   - inventory_logs (date, ingredient_id, quantity, type)

   2) Populate with:
   - 10 ingredients with MOQs
   - 8 bakery products
   - Complete recipes
   - 3 suppliers
   - Recent inventory activity

   3) Add queries for:
   - Low stock alerts
   - Product cost analysis
   - Production metrics

Create a comprehensive dashboard:

.. code-block:: bash

   Let's create a detailed dashboard to visualize the low stock alerts and other insights






