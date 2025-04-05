# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Model Context Protocol (MCP) Python SDK'
copyright = '2023, Model Context Protocol'
author = 'Model Context Protocol'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- GitHub Pages settings ---------------------------------------------------
# These settings are important for GitHub Pages

# Ensure no .doctrees in output
html_use_directory_rtd_theme = True

# Add .nojekyll file to prevent GitHub Pages from ignoring files that start with _
html_extra_path = ['.nojekyll']

# Specify the master document
master_doc = 'index'

# Use index.html for GitHub Pages
html_copy_source = False
html_baseurl = '/mcp_docs/'  # Replace with your repository name

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'custom.css',
]

# External links
extlinks = {
    'github': ('https://github.com/modelcontextprotocol/python-sdk/blob/main/%s', '%s'),
    'spec': ('https://modelcontextprotocol.io/%s', '%s'),
}

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'starlette': ('https://www.starlette.io/', None),
} 