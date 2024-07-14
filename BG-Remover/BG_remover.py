from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        input_image = Image.open(file.stream)
        output_image = remove(input_image)

        # It Saves the output image to a BytesIO object to be sent as a response
        '''Memory Efficiency: The image is stored in memory rather than on disk, which can be faster and avoids the overhead of file I/O operations. This is particularly useful for applications that need to handle images quickly and don't require long-term storage.

           Temporary Storage: When you don't need to save the image permanently, BytesIO is an ideal way to handle temporary storage. It keeps the image in memory until it's sent to the client, then it's discarded.

           Ease of Use with Web Frameworks: Many web frameworks can work directly with BytesIO objects. For example, in Flask, you can use BytesIO to send an image as an HTTP response without saving it to disk. This makes it straightforward to serve dynamically generated images.

           Portability: BytesIO objects are portable and can be easily transferred over the network or between different parts of an application without worrying about file paths or permissions.'''
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name='output.png'
        )

if __name__ == '__main__':
    app.run(debug=True)
