# Primify
_Transform any image into a prime number that looks like the image if glanced upon from far away._

![result](https://i.imgur.com/UoMYkVS.png)
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## How does it work

We proceed in 5 steps:

1. We resize the image to contain at most a `--max_digits` amount of pixels.

2. Run various image processing steps like edge enhancement and smoothing before converting the image into grey-scale.

3. We then quantise the image into just having 5 to 10 greyness levels.

_Note: There are multiple different methods for quantising the color levels and some methods will produces better results for some images. Make sure to play around with the `--method` parameter to get the best result._

4. Now we map each greyness level to a digit, et voila, we have embedded the picture into a number.

5. It now remains to tweak some of the digits until we find a prime number that still looks like the image.

_Note: According to the prime number theorem, the density of prime numbers is  asymptotically of order 1/log(n). Hence, if we have a number with m digits, the number of primality tests that we expect to do until we hit a prime number is roughly proportional to m. Since we use the Baillie–PSW primality test, the overall expected computational complexity of our prime searching procedure is O(n*log(n)³)._

## How to use

You can either import the `PrimeImage` class from `primify.py` or use `primify.py` as a command-line tool.

### Requirements
Make sure you meet all the dependencies inside the `requirements.txt`. I would recommend to use pypy, as it seems to decrease compiling time by about 20%.

### Command-line tool
```
usage: primify.py [-h] [--image IMAGE_PATH] [--max_digits MAX_DIGITS]
                  [--method {0,1,2}] [--output_dir OUTPUT_DIR]
                  [--output_file OUTPUT_FILE] [-v]

Command-line tool for converting images to primes

optional arguments:
  -h, --help            show this help message and exit
  --image IMAGE_PATH    Source image to be converted.
  --max_digits MAX_DIGITS
                        Maximal number of digits the prime can have.
  --method {0,1,2}      Method for converting image. Tweak 'till happy
  --output_dir OUTPUT_DIR
                        Directory of the output text file
  --output_file OUTPUT_FILE
                        File name of the text file containing the prime.
  -v                    Verbose output (Recommended!)
```
Thus, if you have the source image at `./source.png` and you want to convert it into a prime contained in `./prime/prime.txt` which has at most 5000 digits and using conversion method 0 (other options are 1 or 2). Then you should run:

`python primify.py -v --image ./source.png --max_digits 5000 --method 0 --output_dir ./prime/ --output_file prime.txt`

### Importing the PrimeImage class

you can also simply import the `PrimeImage` class from `primify.py` and use that class in your own code. Take a look at the source code to see what methods and attributes there are.
