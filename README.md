# README #



### Introduction ###

Vision Web API: An API for applying Computer Vision and Image Processing tasks to Images.


### Goals ###

The purpose of this project is to provide a simple and platform independent way to manipulate images by using a web API.
You can manipulate images from your website, mobile or desktop application as it is only necessary to make http calls.

### Dependencies ###

This project was developed in Python using Flask to create API and OpenCV for the image processing tasks.

### Setup ###
Before getting the project running first install the following dependencies:
* Python 2.7 [https://www.python.org/downloads/](https://www.python.org/downloads/)
* OpenCV 2 [https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
* Flask [http://flask.pocoo.org/](http://flask.pocoo.org/)

Or using Docker (with docker and docker-compose):

* Assuming you have docker and docker compose installed, you just run docker-compose build.

### How to start it ###
If you setup your project manually, run: 

```
python server/start.py
```

If you setup with docker, run:

```
docker-compose up
```

In both cases your server will start at port 3005.


### Example of use ###
Using Fetch:

```
fetch(
  'http://localhost:3005/',
  {
    method: 'post',
    headers: {
      Accept: 'application/json, text/plain, */*',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      data: 'data:image/gif;base64,....', // Image in base64
      actions: [
        {
          name: 'gray',
        },
        {
          name: 'dx',
          arguments: { kernel_size: 3 },
        },
      ],
    }),
  }
).then((res) => {
  return res.text();
}).then((result) => {
  Console.log("Resulting Image", result); // Image in Base 64
});
```

This will convert the image into gray scale and then apply the dx derivative to find edges in the x direction.


### Supported Image Processing tasks (so far) ###

* Derivative dx and dy.
* Canny Edges
* Binary and Binary Inverted
* Transform image in to gray scale.

Feel free to add more tasks if interested!
