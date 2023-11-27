from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file to the uploads folder
            file.save('uploads/' + file.filename)
            return 'File uploaded successfully!'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
