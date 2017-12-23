"""
Author: Victor Trejo
Description: API utilities functions.

Attributes:
    ACTIONS_KEY (str): name of the action key..
    ARGUMENTS_KEY (str): name of the key for the
                        action's arguments.
    BASE_64_HEADER_REGEXP (str): Header's regular expression
                            for encoded images.
    DATA_KEY (str): name of the data key.
    NAME_KEY (str): name of the name key.
    RGB_MODE (string): RGB mode type.
"""
from flask import send_file
from flask import abort
from io import BytesIO
import base64
from PIL import Image
import numpy
import re

ACTIONS_KEY = "actions"
DATA_KEY = "data"
NAME_KEY = 'name'
ARGUMENTS_KEY = 'arguments'
RGB_MODE = 'RGB'
BASE_64_HEADER_REGEXP = r'(data:image/.*;base64,)(.*)'
BASE_64_HEADER_FORMAT = 'data:image/{0};base64,{1}'

def _image_to_io(
    image,
    image_format,
    quality
):
    """
    Converts a PIL Image to a
    StringIO object.
    
    Args:
        image (Image): Image to be converted.
        image_format (str): Format of the image
        quality (int): quality of the image
    Returns:
        StringIO: the resulting StringIO object.
    """
    if image.mode != RGB_MODE:
        image = image.convert(RGB_MODE)

    io = BytesIO()
    image.save(
        io,
        image_format,
        quality=quality
    )
    io.seek(0)
    return io


def send_image(
    image,
    image_format='PNG',
    quality=100
):
    """
    Sends an image back to the client.
        
    Args:
        data (Image): PIL Image to send back.
        image_format (str, optional): Format of the image,
            default is 'PNG'.
        quality (int, optional): quality of the image,
            default is 100.
    """
    io = _image_to_io(
        image,
        image_format,
        quality
    )

    return send_file(
        io,
        mimetype='image/{}'.format(
            image_format.lower()
        )
    )


def send_base64_image(
    image,
    image_format='PNG',
    quality=100
):
    """
    Sends an image back to the client.
        
    Args:
        data (Image): PIL Image to send back.
        image_format (str, optional): Format of the image,
            default is 'PNG'.
        quality (int, optional): quality of the image,
            default is 100.
    """
    io = _image_to_io(
        image,
        image_format,
        quality
    )

    return  BASE_64_HEADER_FORMAT.format(
        image_format.lower(),
        base64.b64encode(io.getvalue()).decode("utf-8")
    )


def base64_to_image_array(data):
    """Converts a base4 encoded image
    to an image array.
    
    Args:
        data (string): base64 encoded image.
    
    Returns:
        array: decoded image.
    """
    image = Image.open(
        BytesIO(
            base64.b64decode(data)
        )
    )
    return numpy.array(image)



def array_to_image(image_array):
    """Converts an numpy array to a
    PIL image.
    
    Args:
        image_array (array): numpy array
    
    Returns:
        Image: PIL image.
    """
    return Image.fromarray(
        image_array
    )


def bad_request_if_missing(field, data):
     """
     Abort returning a bad request response
     if the given field is not present in
     the data dictionary
     
     Args:
         field (string): field to search
         data (dictionary): data dictionary
     """
     if field not in data:
        bad_request()

def bad_request():
        """Aborts with a bad request.
        """
        abort(400)


def actions_valid(actions):
    """
    Checks if a sequence of actions are valid.
    
    Args:
        actions (enumerable): sequence of actions
    
    Returns:
        bool: True if the actions are valid.
    """
    def _is_valid(action):
        return all(
            key in action
            for key in [NAME_KEY, ARGUMENTS_KEY]
        )
    
    try:
        actions = list(actions)
        return all(
            _is_valid(action)
            for action in actions
        )
    except:
        return False


def remove_type_header(image_data):
    """
    Removes the type header added by the browser
    from base64 encoded image data.
    
    Args:
        image_data (str): Encoded image data.
    
    Returns:
        str: the encoded data without the header.
    """
    return re.sub(
        BASE_64_HEADER_REGEXP,
        r'\2',
        image_data
    )
