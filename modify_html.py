from pathlib import Path


import http.server
import socketserver
import webbrowser
import os
import time

def start_server_and_open_html(html_file_path, port=8000):
    # Ensure the HTML file exists
    if not os.path.isfile(html_file_path):
        print(f"Error: The file {html_file_path} does not exist.")
        return

    # Start the HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(os.path.dirname(html_file_path))  # Change directory to where the HTML file is located

    # Create a socket server
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server started at http://localhost:{port}")
        
        # Open the HTML file in the default web browser
        webbrowser.open(f'http://localhost:{port}/{os.path.basename(html_file_path)}')

        # Keep the server running
        httpd.serve_forever()

def modify_html_with_glb(html_file_path, glb_file_path, output_html_path):
    # Read the content of the existing HTML file
    with open(html_file_path, 'r') as html_file:
        html_content = html_file.read()

    # Replace the .glb file path with the new one provided
    modified_html_content = html_content.replace('./replacemereplacemereplaceme.glb', f'./{glb_file_path}')

    # Write the modified content to a new HTML file
    with open(output_html_path, 'w') as output_file:
        output_file.write(modified_html_content)

    print(f"Modified HTML saved to: {output_html_path}")

# Example usage:
html_file = 'index.html'  # Path to the HTML file to be modified
glb_file = 'your_model.glb'  # Path to the .glb file you want to reference
output_html = 'modified_index.html'  # Output path for the modified HTML file

modify_html_with_glb(html_file, glb_file, output_html)