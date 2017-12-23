import cv_actions as cva
import api_utilities as utl
from flask import Flask
from flask import request
import json
import sys

app = Flask(__name__)
from flask_cors import CORS, cross_origin
CORS(app)


@app.route("/", methods=['POST'])
def apply_actions():
    """
    Apply a series of actions to a given
    base4 encoded image.
    
    It is expected a POST request with the following
    fields:
        data (string) : a base64 encoded image.
        actions (string): json string that contains a
        list of actions [
                {
                    NAME_KEY:ACTION_NAME,
                    ARGUMENTS_KEY:{
                        ARGUMENT_1: VALUE_1,
                        ...
                        ARGUMENT_N: VALUE_N
                    }
                },
                ...
            ]

    Returns:
        string: A base64 encoded image, which is
        the result after applying the actions. 
    """
    form = request.get_json()
    # The DATA_KEY and ACTIONS_KEY are
    # expected, so if either one is missing
    # a bad request is thrown.
    # for key in [utl.ACTIONS_KEY, utl.DATA_KEY]:
    #     utl.bad_request_if_missing(key, form)

    image_data = form.get(utl.DATA_KEY)
    actions_data = form.get(utl.ACTIONS_KEY)
    # print(image_data, file=sys.stderr)

    # If either the image or the actions are not
    # correctly encoded a bad request is thrown.
    try:
        image_data = utl.remove_type_header(
            image_data
        )
        image_array = utl.base64_to_image_array(
            image_data
        )
        actions = actions_data
    except:
        utl.bad_request()

    # A bad request is thrown if the actions
    # do not contain the correct fields.
    if not utl.actions_valid(actions):
        utl.bad_request()

    # Mapping actions before being applied.
    mapped_actions = (
        cva.action(**action)
        for action in actions
    )

    # Applying the actions to the image.
    result =  cva.apply_actions(
        image_array,
        mapped_actions
    )

    return utl.send_base64_image(
        utl.array_to_image(result)
    )
@app.route("/hello", methods=['GET'])
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True, port=3005, host='0.0.0.0')