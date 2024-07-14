from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from docx2pdf import convert as convert_to_pdf
from docx import Document as PythonDocxDocument
from pdf2docx import Converter as PdfToDocxConverter
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_to_docx(doc_filename, docx_filename):
    doc = PythonDocxDocument(doc_filename)
    doc.save(docx_filename)


def convert_to_pdf_from_docx(docx_filename, pdf_filename):
    convert_to_pdf(docx_filename, pdf_filename)


def convert_to_docx_from_pdf(pdf_filename, docx_filename):
    converter = PdfToDocxConverter(pdf_filename)
    converter.convert(docx_filename)
    converter.close()


def cleanup_files(*filepaths):
    for filepath in filepaths:
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error removing file '{filepath}': {e}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    print(f'Uploaded File: {file.filename}')
    print(f'Uploaded File Path: {file.filename}')

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if not allowed_file(filename):
            cleanup_files(filepath)
            return render_template('index.html', message='Unsupported file format')

        if filename.endswith('.pdf'):
            docx_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{os.path.splitext(filename)[0]}_converted.docx')
            convert_to_docx_from_pdf(filepath, docx_filename)
            cleanup_files(filepath)  # Remove original PDF file
            return render_template('index.html', converted_file=docx_filename)
        elif filename.endswith('.docx'):
            pdf_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{os.path.splitext(filename)[0]}_converted.pdf')
            convert_to_pdf_from_docx(filepath, pdf_filename)
        elif filename.endswith('.doc'):
            temp_docx_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{os.path.splitext(filename)[0]}_temp.docx')
            convert_to_docx(filepath, temp_docx_filename)
            pdf_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{os.path.splitext(filename)[0]}_converted.pdf')
            convert_to_pdf_from_docx(temp_docx_filename, pdf_filename)
            cleanup_files(temp_docx_filename)  # Remove temporary DOCX file
        else:
            cleanup_files(filepath)  # Remove unsupported file
            return render_template('index.html', message='Unsupported file format')

        cleanup_files(filepath)  # Remove original uploaded file
        return render_template('index.html', converted_file=pdf_filename)

    except Exception as e:
        print(f'Error: {e}')
        cleanup_files(filepath)  # Remove any partially processed files
        return 'An error occurred during file access or conversion.'


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
