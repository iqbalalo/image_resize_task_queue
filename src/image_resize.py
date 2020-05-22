import os
from PIL import Image
import base64
from io import BytesIO


def resize_process(img):
    """Image resize process
    Arguments:
        img {string} -- file path
    Returns:
        sring -- image data in base64 utf-8 decoded
    """

    # define dimension
    size = (100, 100)

    buffered = BytesIO()

    try:
        # Open image and resize and save result to buffered,
        # then encode and return utf decoded as result

        im = Image.open(img)
        im = im.resize(size, Image.ANTIALIAS)
        im.save(buffered, "JPEG")

        _base64 = base64.b64encode(buffered.getvalue())

        # Better to delete source file as it is unused
        os.remove(img)

        return _base64.decode("utf-8")

    except IOError:
        # Any IO error return error message
        return "cannot resize image for '%s'" % img.filename
