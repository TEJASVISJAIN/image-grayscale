from hashlib import new
from pickle import FALSE
import re
from app import app
import cv2 as cv
import numpy as np
from PIL import Image as im
#for emailing images
import smtplib
import imghdr
from email.message import EmailMessage
# from numpy import ndarray

import os
from flask import render_template, request, redirect, jsonify, make_response, send_from_directory, abort
from werkzeug.utils import secure_filename


# @app.route("/")
# def index():
#     return render_template("index-yt.html")

# @app.route("/about")
# def about():
#     return "All about Flask"

# basedir = os.path.abspath(os.path.dirname(__file__))

app.config["CLIENT_IMAGES"] = "C:/Users/Tejasvi/Desktop/sm-test/app/static/client/img"
app.config["CLIENT_CSV"] = "C:/Users/Tejasvi/Desktop/sm-test/app/static/client/csv"
app.config["CLIENT_PDF"] = "C:/Users/Tejasvi/Desktop/sm-test/app/static/client/pdf"

app.config['IMAGE_UPLOADS'] = "C:/Users/Tejasvi/Desktop/sm-test/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

def allowed_image(filename):
#checks extensions:
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/",methods=["GET","POST"])
def index():
    
    if request.method == "POST":
        # if request.form["size"]:
        #     size=int(request.form["size"])

        if request.files and request.form["size"]:
            size = int(request.form["size"])
           
            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                #secures the filename(removes spaces,full paths etc)
                filename = secure_filename(image.filename)
                
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                # converting it to grayscale
                num_image = cv.imread(os.path.join(app.config["IMAGE_UPLOADS"], filename),cv.IMREAD_UNCHANGED)
                image_copy = np.copy(num_image)
                gray = cv.cvtColor(image_copy, cv.COLOR_RGB2GRAY)

                # resizing images

                width = int(gray.shape[1] * size/100)
                height = int(gray.shape[0] * size/100)
                dimension = (width, height)
                
                resized_image = cv.resize(gray,dimension,interpolation = cv.INTER_AREA)

                gray_im = im.fromarray(resized_image)

                gray_im.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                print("Image processed and saved")
                nexturl=f"{request.url}get-image/{filename}"
                print("download link",nexturl)
                #sending this image on email
                recemail=request.form["email"]
                if recemail!="" :
                    Sender_Email = "shubhammalhotracr7@gmail.com"
                    Reciever_Email = recemail
                    Password="706448shub"

                    newMessage = EmailMessage()    #creating an object of EmailMessage class
                    newMessage['Subject'] = "Image converted to black and white." 
                    newMessage['From'] = Sender_Email  #Defining sender email
                    newMessage['To'] = Reciever_Email  #Defining reciever email
                    new_line='\n'
                    msg=f"Hi, here is your B/W image resized accordingly.{new_line}Download link is also given below.{new_line}{nexturl}"
                    newMessage.set_content(msg) 
                    
                    pathemail=os.path.join(app.config["IMAGE_UPLOADS"], filename)
                    with open(pathemail, 'rb') as f:
                        image_data = f.read()
                        image_type = imghdr.what(f.name)
                        image_name = f.name
                    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(Sender_Email, Password) #Login to SMTP server
                        smtp.send_message(newMessage)


                
                return  redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)
        
    return render_template("index.html")

#sending/downloading files
@app.route("/get-image/<image_name>")
def get_image(image_name):

    try:
        return send_from_directory(app.config["IMAGE_UPLOADS"], path=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# @app.route("/get-csv/<csv_id>")
# def get_csv(csv_id):

#     filename = f"{csv_id}.csv"

#     try:
#         return send_from_directory(app.config["CLIENT_CSV"], path=filename, as_attachment=True)
#     except FileNotFoundError:
#         abort(404)

# @app.route("/get-pdf/<pdf_id>")
# def get_pdf(pdf_id):

#     filename = f"{pdf_id}.csv"

#     try:
#         return send_from_directory(app.config["CLIENT_PDF"], path=filename, as_attachment=True)
#     except FileNotFoundError:
#         abort(404)


# for yt video example
# @app.route("/signup", methods=["GET", "POST"])
# def sign_up():

#     if request.method == "POST":

#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]

#         print(username,email,password)

#         return redirect(request.url)

#     return render_template("signup.html")

# @app.route("/json", methods=["POST"])
# def json_example():

#     if request.is_json:

#         req = request.get_json()

#         response_body = {
#             "message": "JSON received!",
#             "sender": req.get("name")
#         }

#         res = make_response(jsonify(response_body), 200)

#         return res

#     else:

#         return make_response(jsonify({"message": "Request body must be JSON"}), 400)

# GUESTBOOK - yt data submission form
@app.route("/guestbook")
def guestbook():
    return render_template("guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify({"message": "OK"}), 200)

    return res

#QUERYYYYYY-

# @app.route("/query")
# def query():

#     if request.args:

#         # We have our query string nicely serialized as a Python dictionary
#         args = request.args

#         # We'll create a string to display the parameters & values
#         serialized = ", ".join(f"{k}: {v}" for k, v in request.args.items())

#         # Display the query string to the client in a different format
#         return f"(Query) {serialized}", 200

#     else:

#         return "No query string received", 200 