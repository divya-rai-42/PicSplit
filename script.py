from flask import Flask, request, render_template, jsonify, Response, send_file, redirect, make_response, url_for
import os
# check opencv version
import cv2
# print version number
print(cv2.__version__)
import os
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from mtcnn.mtcnn import MTCNN
import face_recognition
import shutil
import zipfile

app = Flask(__name__, static_folder='static')

# Set the upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# Check if a file has a permitted file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def createZip():
    folder_path = "./Segregated_folders"
    zip_path = "./Segregated_folders.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file))
    print("zip folder created")


def processImages():
    
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])

    folder_name = "Segregated_folders"

    enc_dict={}

    # Specify the path where you want to create the new folder
    path = "./"

    # Use the os.mkdir() method to create the new folder
    os.mkdir(os.path.join(path, folder_name))

    # Verify that the folder has been created
    if os.path.exists(os.path.join(path, folder_name)):
        print("Folder created successfully!")
    else:
        print("Folder creation failed.")

    rootdir = './uploads'
    segregated_dir = './Segregated_folders'
    for file in os.listdir(rootdir):
        filename = os.path.join(rootdir, file)
        # load image from file
        pixels = pyplot.imread(filename)
        # create the detector, using default weights
        detector = MTCNN()
        # detect faces in the image
        faces = detector.detect_faces(pixels)
        # display faces on the original image
        # draw_faces(filename, faces)
        # print(faces)
        print("Number of faces:" + str(len(faces)))
        for face in faces:
            file_path = "./this_face.jpg"
            x1, y1, width, height = face['box']
            x2, y2 = x1 + width, y1 + height
            cv2.imwrite(file_path,pixels[y1:y2, x1:x2])
            list_dir = os.listdir(segregated_dir)

            flag = False
            flag2 = False
            flag3 = False

            img2 = cv2.imread("./this_face.jpg")
            rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
                # img_encoding2 = face_recognition.face_encodings(img2)[0]
            face_locations2 = face_recognition.face_locations(img2, number_of_times_to_upsample=2)
            face_encodings2_sample = face_recognition.face_encodings(img2, known_face_locations=face_locations2, num_jitters=100)

            if len(face_encodings2_sample) == 0:
                continue
            face_encodings2 = face_recognition.face_encodings(img2, known_face_locations=face_locations2, num_jitters=100)[0]
            print("Second step done")

            for item in list_dir:
                # print("item")
                item_path = os.path.join(segregated_dir, item)

                primary_path = item_path + "/primary.jpg"

                print("This is primary path" + primary_path)

                if os.path.exists(primary_path) == False:
                    print("continued")
                    continue

                face_encodings = enc_dict[item]
                print("First step done")

                results = face_recognition.compare_faces([face_encodings], face_encodings2,0.6)
                print(results[0])

                if results[0] == True:
                    flag = True
                    shutil.copy(filename, item_path)
                    print("Added")
                    break

            
            if flag2 == True:
                continue

            if flag == False:
                number = len(list_dir)
                new_folder_name = "Person" + str(number)

                # Specify the path where you want to create the new folder
                new_path = "./Segregated_folders/"
                
                enc_dict[new_folder_name]=face_encodings2

                # Use the os.mkdir() method to create the new folder
                new_folder_path = os.path.join(new_path, new_folder_name)
                os.mkdir(new_folder_path)

                cv2.imwrite(new_folder_path + "/primary.jpg",pixels[y1:y2, x1:x2])
                shutil.copy(filename, new_folder_path)

            
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file_path} has been deleted.")
            else:
                print(f"{file_path} does not exist.")



# Render the web form
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loggedin')
def loggedin():
    return render_template('loggedin.html')

@app.route('/collections')
def collections():
    return render_template('collections.html')

@app.route('/folders')
def folders():
    return render_template('folders.html')

@app.route('/photos')
def photos():
    return render_template('photos.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug = True)
