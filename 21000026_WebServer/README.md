# scs2205-web-server

# Simple Python Web Server

This is a simple Python web server that serves static files and handles PHP scripts. The server looks for `index.php` or `index.html` files in the `htdocs` directory and serves them as the default pages.

## Features

- Serves static HTML and PHP files.
- Supports both GET and POST requests for PHP scripts.
- Handles URL parameters for PHP scripts.

## Prerequisites

- Python 3.x
- PHP (for executing PHP scripts)

## Method of execution

- The server will start and listen on http://127.0.0.1:2728 by default. You can change the host and port by modifying the host and port variables in the webserver.py script.

- Access the server in your web browser by navigating to http://127.0.0.1:2728. It will display index.php or index.html if found in the requested directory.

- To execute PHP scripts, place them in the htdocs directory and access them through the web browser, e.g., http://127.0.0.1:2728/myscript.php.
