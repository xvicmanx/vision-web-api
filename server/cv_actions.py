"""
Author: Victor Trejo
Description: Computer Vision actions.
"""

import cv2
import numpy as np
from collections import namedtuple

_actions_registry = {}
def register(name):
    """Register decorator:
    Registers a function as a Computer
    Vision action for the API.
    
    Args:
        name (string): given name to 
        register the function.
    
    Returns:
        function: The decorator.
    """
    global _actions_registry
    def _decorator(func):
        """Stores the reference in the
        actions registry so it become
        part of the API.
        
        Args:
            func (function): function to
            register.
        """
        _actions_registry[name] = func
    return _decorator



def _derivative(
    image,
    kernel_size=5,
    degree_x=0,
    degree_y=0):
    """Finds the derivatives of a given image
    by applying a sobel filter.
    
    Args:
        image (array): image to find the derivative from.
        kernel_size (int, optional): Kernel size, default is 5.
        degree_x (int, optional): x derivative degree, default is 0
            which is none derivative.
        degree_y (int, optional): y derivative degree, default is 0
            which is none derivative.
    
    Returns:
        array: the filtered image.
    """
    return np.absolute(
        cv2.Sobel(
            image,
            cv2.CV_8U,
            degree_x,
            degree_y,
            ksize=kernel_size
        )
    )


def _threshold(
    image,
    first_threshold,
    second_threshold,
    threshold_type
):
    """
    Apply a threshold to a image.
    
    Args:
        image (array): image to apply filter.
        first_threshold(int): first threshold.
        second_threshold(int): second threshold.
        threshold_type(int): type of threshold to apply.
    
    Returns:
        array: the filtered image.
    """
    result = cv2.threshold(
        image,
        first_threshold,
        second_threshold,
        threshold_type
    )
    return result[1]



@register('gray')
def _gray(image):
    """Converts a BGR image to gray scale.
    
    Args:
        image (array): image to be converted
        to gray scale.
    
    Returns:
        array: gray scale image.
    """
    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

@register('resize')
def _resize(image, width, height):
    """Resizes an image to a given size.
    
    Args:
        image (array): image to resize.
        width (int): new width.
        height (int): new height.
    
    Returns:
        array: the resized image.
    """
    return cv2.resize(
        image,
        (width, height)
    )

@register('dx')
def _dx(image, kernel_size=5, degree = 1):
    """Finds the x derivative of a given image
    by applying a sobel filter.
    
    Args:
        image (array): image to find the derivative from.
        kernel_size (int, optional): Kernel size, default is 5.
        degree (int, optional): Derivative degree, default is 1
            which is the first derivative.
    
    Returns:
        array: the filtered image.
    """
    return _derivative(
        image,
        kernel_size,
        degree,
        0
    )


@register('dy')
def _dy(image, kernel_size=5, degree = 1):
    """Finds the y derivative of a given image
    by applying a sobel filter.
    
    Args:
        image (array): image to find the derivative from.
        kernel_size (int, optional): Kernel size, default is 5.
        degree (int, optional): Derivative degree, default is 1
            which is the first derivative.
    
    Returns:
        array: the filtered image.
    """
    return _derivative(
        image,
        kernel_size,
        0,
        degree
    )


@register('canny_edges')
def _canny_edges(
    image,
    first_threshold,
    second_threshold
):
    """
    Finds the canny edges from a given image.
    
    Args:
        image (array): image to find the canny edges
        first_threshold(int): first threshold.
        second_threshold(int): second threshold.
    
    Returns:
        array: the filtered image.
    """
    return cv2.Canny(
        image,
        first_threshold,
        second_threshold
    )




@register('binary')
def _binary(
    image,
    first_threshold,
    second_threshold
):
    """
    Converts an image to binary.
    
    Args:
        image (array): image to find the binary.
        first_threshold(int): first threshold.
        second_threshold(int): second threshold.
    
    Returns:
        array: the filtered image.
    """
    
    return _threshold(
        image,
        first_threshold,
        second_threshold,
        cv2.THRESH_BINARY
    )


@register('binary_inverted')
def _binary_inverted(
    image,
    first_threshold,
    second_threshold
):
    """
    Converts an image to inverted binary.
    
    Args:
        image (array): image to find the inverted binary.
        first_threshold(int): first threshold.
        second_threshold(int): second threshold.
    
    Returns:
        array: the filtered image.
    """
    return _threshold(
        image,
        first_threshold,
        second_threshold,
        cv2.THRESH_BINARY_INV
    )





_Action = namedtuple(
    'Action',
    'name arguments'
)
def action(name, arguments = None):
    """Creates an action's configuration
    before being executed.
    
    Args:
        name (string): action name
        arguments (dictionary, optional): action's function
        arguments.
    
    Returns:
        Action: An action configuration namedtuple.
    """
    if arguments is None:
        arguments = {}
    return _Action(
        name,
        arguments
    )


def apply_actions(image, actions):
    """Apply a sequence of actions to an image.
    
    Args:
        image (array): target image.
        actions (enumerable): sequence of actions
        to be applied.
    
    Returns:
        array: the filtered image.
    """
    global _actions_registry
    result = image.copy()
    for action in actions:
        result =_actions_registry[action.name](
            result,
            **action.arguments
        )
    return result
