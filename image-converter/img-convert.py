from PIL import Image  # Import the main image module
import os

# Open the filepath to the image you want to convert.
image_path = input("Provide the image path:  ")
originalIMG = Image.open(image_path)
image_name = os.path.splitext(image_path)


# Convert the image to PNG
try:
    if originalIMG.format == "JPEG":
        convertedIMG= originalIMG.convert("RGBA")
        convertedIMG.save(f"{image_name[0]}.png")
        print("It's now a PNG!")

    elif originalIMG.format == "PNG":
        convertedIMG= originalIMG.convert("RGB")
        convertedIMG.save(f"{image_name[0]}.jpg")
        print("It's now a JPEG!")
except:
    print("Error was received")

# Learned new thing. Default parameters must com after regular parameters.
def convert_many(file_extension, filefolder_location = "."):
    for filename in os.listdir("folder_location"):
        if filename.endswith(f".{file_extension}"):
            pass