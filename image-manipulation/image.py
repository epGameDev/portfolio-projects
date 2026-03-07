import os

from PIL import Image, ImageFilter, ImageOps
    # Image: Main image module
    # ImageFilter: Allows for pre-configured filters
    # ImageOps: New in development, image functions



# ==================================
# =========== initialize ===========

pwd = os.getcwd()


# =================================
# ============= Notes =============

### Some Methods ###
# format, size, mode, show(), new(), resize(sizeX, sizeY), thumbnail(sizeX, sizeY) modifies in places
# crop((left, top, right, bottom)), rotate(deg), transpose(), convert(), paste(), save(), filter()

### Image Function Examples ###
# ImageOps.colorize(), ImageOps.crop(image: Image, border: int = 0) Removes image borders, ImageOps.flip()
# ImageOps.invert(image: Image), ImageOps.mirror(image: Image), ImageOps.posterize(image: Image, bits: int)
# ImageOps.solarize(image: Image, threshold: int = 128), ImageOps.pad(image, size, color="#f00").save("image.ext")




def gaussian_blur(image: str, filter_level: int, save_loc: str = pwd):
    """
    Args: 
        image (str): The string path to the file.
        filter_level (int): Between 1 and 50+. 
        save_loc (str): Saves an image to the specified location. Default is the current working directory.
    
    Returns:
        None: Saves object to specified location. Default location is pwd.
    
    gaussian_blur(<str: file path>, <int: blur level>, <str: save path>)
    """
    image_file = Image.open(image)
    image_name = os.path.basename(image).split(".")
    blurred_img = image_file.filter(ImageFilter.GaussianBlur(filter_level))
    blurred_img.show()
    blurred_img.save(f"{save_loc}/{image_name[0]}-grey-scale.png", "png")



def grey_scale(image: str, save_loc: str = pwd):
    """
    Args: 
        image (str): The string path to the file. 
        save_loc (str): Saves an image to the specified location. Default is the current working directory.
    
    Returns:
        None: Saves object to specified location. Default location is pwd.
    
    grey_scale(<str: file path>, <str: save path>)
    """
    image_file = Image.open(image)
    image_name = os.path.basename(image).split(".")
    print(image_name)
    grey_img = image_file.convert("L") # 'L' is grayscale, rgb, 'P' is for palette, '1' B&W dithering
    grey_img.show()
    grey_img.save(f"{save_loc}/{image_name[0]}-grey-scale.png", "png")

# grey_scale("../images/blurred-image.png", "../images")



def resize_img():

    # new_image = analogue.resize((1200, 900), 3) # Does not maintain aspect ratio
    # analogue.thumbnail((1200, 900), Image.ANTIALIAS) # Maintains Aspect Ratio
    # new_image = ImageOps.contain(analogue, (1200, 900)) # Maintains Aspect Ratio (experimental)
    # new_image.show()
    # new_image.save("../images/analogue-3D-edited.png")
    pass