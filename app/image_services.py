from PIL import Image

def do_resize_image(image_url, width=256, height=256, format="PNG"):
    image = Image.open(image_url)
    image_resized = image.resize((width,height))
    image_resized.save(image_url, format)

