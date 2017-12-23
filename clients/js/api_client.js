/**
 * Author: Victor Trejo
 * Description: Javascript client library to the
 *               Computer vision web API.
 */


CV_API = (function(){
  /**
   * [API_URL url of the service api]
   * @type {String}
   */
  var API_URL = '';

  /**
   * Encodes an image to base 64.
   * @param  {Image} image image to be encoded.
   * @return {String}       the encoded result.
   */
  var _base64_encode = function (image)
  {
    var canvas = document.createElement('canvas');
    canvas.height = image.height;
    canvas.width = image.width;
    var context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    return canvas.toDataURL();
  };

  /**
   * Loads an image from a given url
   * @param  {String}   url      url's of the image.
   * @param  {Function} callback function that
   * receives the result.
   */
  var _load_image = function (url, callback) {
     var _image = new Image();
    _image.crossOrigin = 'Anonymous';
    _image.onload = function() {
      callback(
        _base64_encode(this)
      );
    };
    _image.src = url;
  };

  /**
   * [ActionsSequence's constructor function]
   */
  ActionsSequence = function (){

      if ( typeof this.requester ==! "object" )
      {
        throw "'requester' is not set to a request function. " +
              "Set it to a function such as 'JQuery.post' for example."
      }
      
      var _actions = [];
      var that = this;
      /**
       * Creates an action object given the name
       * and arguments.
       * @param  {String} name name of the action.
       * @param  {object} args action's arguments.
       * @return {object}      The action object.
       */
      var _create_action = function(name, args){
        
        if ( !args ){
          args = {}
        }

        return {
          'name': name,
          'arguments': args
        }
      }

      /**
       * Adds an action to the sequence
       * @param {String} type action's type name.
       * @param {object} args action's arguments
       */
      var _add_action = function(type, args)
      {
        _actions.push(
          _create_action(
            type,
            args
          )
        );
      }

      /**
       * Adds a derivative action.
       * @param  {String} type        derivative action's name.
       * @param  {number} kernel_size size of the kernel.
       */
      var _derivative = function(type, kernel_size) {
        _add_action(
          type,
          { kernel_size: kernel_size }
        );
      }

      /**
       * Adds a gray action to the sequence.
       * @return {object} current object.
       */
      this.gray = function() {
        _add_action('gray');
        return this;
      };

      /**
       * Adds the x derivative action to the sequence.
       * @param  {number} kernel_size size of the kernel.
       * @return {object} current object.
       */
      this.dx = function(kernel_size) {
        _derivative('dx', kernel_size);
        return this;
      };

      /**
       * Adds the y derivative action to the sequence.
       * @param  {number} kernel_size size of the kernel.
       * @return {object} current object.
       */
      this.dy = function(kernel_size) {
        _derivative('dy', kernel_size);
        return this;
      };

      /**
       * Adds the resize action to the sequence.
       * @param  {number} width  width the image will be resized.
       * @param  {number} height height the image will be resized.
       * @return {object} current object.
       */
      this.resize = function(width, height)
      {
        _add_action(
          'resize',
          {
            width: width,
            height: height
          }
        );
        return this;
      };


      /**
       * Finds the canny edges from a given image.
       * @param  {number} first_threshold   first threshold.
       * @param  {number}} second_threshold second threshold.
       * @return {object} current object.
       */
      this.canny_edges = function(
        first_threshold,
        second_threshold
      )
      {
        _add_action(
          'canny_edges',
          {
            first_threshold: first_threshold,
            second_threshold: second_threshold
          }
        );
        return this;
      };


      /**
       * Finds the binary representation from a given image.
       * @param  {number} first_threshold   first threshold.
       * @param  {number}} second_threshold second threshold.
       * @return {object} current object.
       */
      this.binary = function(
        first_threshold,
        second_threshold
      )
      {
        _add_action(
          'binary',
          {
            first_threshold: first_threshold,
            second_threshold: second_threshold
          }
        );
        return this;
      };


       /**
       * Finds the inverted binary representation from a given image.
       * @param  {number} first_threshold   first threshold.
       * @param  {number}} second_threshold second threshold.
       * @return {object} current object.
       */
      this.binary_inverted = function(
        first_threshold,
        second_threshold
      )
      {
        _add_action(
          'binary_inverted',
          {
            first_threshold: first_threshold,
            second_threshold: second_threshold
          }
        );
        return this;
      };

    /**
     * Applies all the added actions to the given image.
     * @param  {String}   src      image's source.
     * @param  {Function} callback Callback function that 
     *         is going to receive the result of the actions.
     */
    
    this.apply_actions = function(src, callback){
      load_image(src, function(data){
        var request_data = {
          data: data,
          actions: JSON.stringify(
            _actions
          )
        };
        that.requester(
          API_URL,
          request_data,
          function(response_data){
            callback(response_data);
        });
      });
    };
  };

  /*
   * Requester function that
   * is going to make the
   * http request to the API.
   */
  ActionsSequence.prototype.requester = null;
  /**
   * [set_requester Sets the requester function]
   * @param {[object]} requester requester function.
   */
  ActionsSequence.set_requester = function(requester){
    ActionsSequence.prototype.requester = requester;
  }
  
  return {
    ActionsSequence: ActionsSequence,
    load_image: _load_image,
    set_url: function(url)
    {
      API_URL = url;
    }
  };

})();


