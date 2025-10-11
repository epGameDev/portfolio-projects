from PIL import Image  # Import the main image module
import os

# Goal is to loop through a folder of images and convert their current type to a target type.

# Open the filepath to the image you want to convert.
directory = input("What directory would you like to iterate over?  # ").strip()
current_directory = os.getcwd()

if os.path.exists(directory):

    for image in os.listdir(directory):
        try:
            placeholder = Image.open(f"{directory}/{image}")
            file_name, extension = os.path.splitext(placeholder.filename)
            placeholder.save(f"{current_directory}/images/{file_name}-converted.webp", format="WEBP")
        except Exception as err:
            print(f"There was an error: {err}")
            
else:
    print(f"File path {directory} does not exist")