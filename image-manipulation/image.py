from PIL import Image, ImageFilter, ImageOps

mario3 = Image.open("./images/mario1.png")
analogue = Image.open("./images/analogue-3D.png")
# analogue2 = Image.open("./images/analogue-3D-edited.png")


### Some Methods ###

# format, size, mode, show(), new(), resize(sizeX, sizeY), thumbnail(sizeX, sizeY) modifies in places
# crop((left, top, right, bottom)), rotate(deg), transpose(), convert(), paste(), save(), filter()

# ImageOps.colorize(), ImageOps.crop(image: Image, border: int = 0) Removes image borders, ImageOps.flip()
# ImageOps.invert(image: Image), ImageOps.mirror(image: Image), ImageOps.posterize(image: Image, bits: int)
# ImageOps.solarize(image: Image, threshold: int = 128), ImageOps.pad(image, size, color="#f00").save("image.ext")
# "dir" shows all image properties you can use. print(dir(image))


# new_image = analogue.resize((1200, 900), 3) # Does not maintain aspect ratio
# analogue.thumbnail((1200, 900), Image.ANTIALIAS) # Maintains Aspect Ratio
new_image = ImageOps.contain(analogue, (1200, 900)) # Maintains Aspect Ratio (experimental)
new_image.show()
new_image.save("./images/analogue-3D-edited.jpg")

# filtered_img = analogue2.filter(ImageFilter.GaussianBlur(3))
# grey_img = filtered_img.convert("L") # 'L' is grayscale, rgb, 'P' is for palette, '1' B&W dithering
# grey_img.show()
# grey_img.save("./images/filtered.png", "png")