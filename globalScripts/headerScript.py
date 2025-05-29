import tkinter as tk
from tkinter import filedialog as fd

import customtkinter as ctk 
import os
import pdfplumber
import PyPDF2
import fitz  # PyMuPDF

import sys

def select_file():
    # Use a customtkinter window for file picking
    def open_file_picker():
        file_path = fd.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        app.selected_file = file_path
        app.destroy()

    app = ctk.CTk()
    app.title("CustomTkinter File Picker")
    app.geometry("1920x1080")

    button = ctk.CTkButton(app, text="Pick a File", command=open_file_picker)
    button.pack(pady=20)

    label = ctk.CTkLabel(app, text="No file selected.")
    label.pack(pady=10)

    app.selected_file = None
    app.mainloop()
    return app.selected_file

def count_pdf_pages(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)

def extract_content_headers(pdf_path):
    doc = fitz.open(pdf_path)
    headers = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        if not blocks:
            continue

        # Sortiere Textblöcke von oben nach unten
        blocks.sort(key=lambda b: b[1])

        for block in blocks:
            text = block[4].strip()
            if text:
                first_line = text.split('\n')[0].strip()
                headers.append((page_num, first_line))
                break  # Nur ein Header pro Seite
    return headers

def save_content_headers_to_markdown(content_headers, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for page_num, header_text in content_headers:
            f.write(f"- Seite {page_num}: {header_text}\n")

def main(data_path=None):
    if data_path:
        file_path = data_path
    else:
        file_path = select_file()
    if not file_path:
        print("No file selected.")
        return

    num_pages = count_pdf_pages(file_path)
    print(f"Number of Pages: {num_pages}")

    content_headers = extract_content_headers(file_path)
    print(f"Extracted Content Headers: {content_headers}")

    output_path = os.path.splitext(file_path)[0] + "_content_headers.md"
    save_content_headers_to_markdown(content_headers, output_path)
    print(f"Content headers saved to {output_path}")

if __name__ == "__main__":
    # If a path is given as a command-line argument, use it
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
