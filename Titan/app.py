from flask import Flask, request, send_file, render_template_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

app = Flask(__name__)

def convert_to_pdf(input_file, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)

    if input_file.endswith('.pdf'):
        c.drawImage(ImageReader(input_file), 0, 0, width=letter[0], height=letter[1])
    elif input_file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        c.drawImage(input_file, 0, 0, width=letter[0], height=letter[1])
    else:
        with open(input_file, 'r') as f:
            lines = f.readlines()
            text = ' '.join(lines)
            c.drawString(100, 750, text)

    c.save()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        input_file_path = os.path.join('uploads', file.filename)
        output_file_path = os.path.join('outputs', 'output.pdf')
        
        # Ensure the directories exist
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('outputs', exist_ok=True)

        file.save(input_file_path)
        convert_to_pdf(input_file_path, output_file_path)
        
        return send_file(output_file_path, as_attachment=True)

    return render_template_string('''
    <!doctype html>
    <title>Upload a File</title>
    <h1>Upload a File to Convert to PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
