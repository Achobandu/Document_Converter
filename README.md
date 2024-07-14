# Simple Document Converter

A straightforward web application that converts PDF files to DOCX and vice versa. This project uses Python for backend processing and HTML/CSS for the frontend interface.

## Features

- Convert PDF to DOCX
- Convert DOCX to PDF
- Convert DOC to PDF
- Simple and intuitive web interface
- File upload and download functionality

## Technologies Used

- Backend: Python 3.x
- Frontend: HTML, CSS
- Web Framework: Flask
- File Conversion Libraries: 
  - docx2pdf
  - python-docx
  - pdf2docx

## Installation

1. Clone the repository:
  git clone https://github.com/achobandu/document_converter.git
  cd document_converter
2. Install the required dependencies:
  pip install flask werkzeug docx2pdf python-docx pdf2docx
3. Run the application:
  python app.py
4. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Open the web application in your browser.
2. Click on the "Choose File" button to select a PDF, DOCX, or DOC file.
3. Click "Convert" to start the conversion process.
4. Once conversion is complete, click the "Download Converted File" button to get your converted document.

## File Structure

- `app.py`: The main Python script containing the Flask application and conversion logic.
- `templates/index.html`: The HTML template for the web interface.
- `uploads/`: Directory where uploaded and converted files are temporarily stored.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/document_converter/issues) if you want to contribute.

## License

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [docx2pdf](https://github.com/AlJohri/docx2pdf)
- [python-docx](https://python-docx.readthedocs.io/)
- [pdf2docx](https://github.com/dothinking/pdf2docx)
