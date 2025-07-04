"""
convert_docx.py
---------------
Command-line utility to batch convert all `.docx` files in a specified folder into Markdown format.

It uses Mammoth to extract semantic HTML from Word documents, then converts the HTML to Markdown
using the `markdownify` library. All resulting `.md` files are saved in the `markdown_files/` directory.

Usage:
    python convert_docx.py <input_folder> [-v]
"""

import mammoth
from markdownify import markdownify as md
import argparse
import os

def docx_to_html(docx_path):
    try:
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html_content = result.value  # The generated HTML
            return html_content
    except Exception as e:
        print(f"Error converting DOCX to HTML: {e}")
        raise

def docx_to_markdown(docx_path, md_path, verbose=False):
    try:
        # Convert DOCX to HTML
        if verbose:
            print(f"Converting '{docx_path}' to HTML...")
        html_content = docx_to_html(docx_path)

        # Convert HTML to Markdown
        if verbose:
            print(f"Converting HTML to Markdown...")
        md_content = md(html_content, heading_style="ATX")

        # Save the Markdown content to a file
        with open(md_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_content)

        if verbose:
            print(f"Markdown file saved to '{md_path}'")
    except Exception as e:
        print(f"Error converting '{docx_path}' to Markdown: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Batch convert DOCX files in a folder to Markdown.")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing DOCX files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

    args = parser.parse_args()
    input_folder = args.input_folder

    if not os.path.isdir(input_folder):
        print(f"Error: '{input_folder}' is not a valid directory.")
        return

    docx_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".docx")]

    if not docx_files:
        print("No DOCX files found in the directory.")
        return

    output_folder = "markdown_files"
    os.makedirs(output_folder, exist_ok=True)

    for docx_filename in docx_files:
        docx_path = os.path.join(input_folder, docx_filename)
        md_filename = os.path.splitext(docx_filename)[0] + ".md"
        md_path = os.path.join(output_folder, md_filename)
        docx_to_markdown(docx_path, md_path, verbose=args.verbose)

if __name__ == "__main__":
    main()