# ========================= Color Palette Generator Program ========================= #


# ------------------------- General Section ------------------------- #

# Import needed modules
import PIL                  # for reading image files
import extcolors            # for extracting colors from image
from webcolors import *     # for converting RGB to hexadecimal color code
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


# ------------------------- Image Processing Class ------------------------- #

class Img:

    # Define class static attributes
    filename = ""
    colors_list = []
    upload_folder = 'static/images/'

    # Define class method
    @classmethod
    def extract_colors(self):
        # Get file name of image to process
        print("Extracting colors from: ", self.filename)
        image_name = self.filename
        # Open the specified image and get its dimensions
        my_image = PIL.Image.open(image_name)
        width, height = my_image.size
        pixels = width * height
        # Extract image colors with relevant number of pixels
        colors, pixel_count = extcolors.extract_from_path(image_name)   # second argument fo assignment IS required
        # Display image color palette
        self.colors_list = []
        for color in colors:
            self.colors_list.append((rgb_to_hex(color[0]), "{0:.00%}".format(color[1] / pixels)))
        return


# ------------------------------ Main Section ------------------------------ #

# Start Flask Application
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER   # Suggested in documentation but not really needed


# Display Main Page
@app.route('/')
def home():
    for color in Img.colors_list:
        print(color[0], color[1])
    return render_template("index.html", photo_image=Img.filename, colors=Img.colors_list)


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        new_file_name = secure_filename(file.filename)
        if not (new_file_name == ""):
            Img.filename = Img.upload_folder + new_file_name
            file.save(Img.filename)
            Img.extract_colors()
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
