# Primify

_Transform any image into a prime number that looks like the image if glanced upon from far away._

![result](https://i.imgur.com/UoMYkVS.png)
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## How does it work

We proceed in 5 steps:

1. We resize the image to contain at most a `--max_digits` amount of pixels.

2. Run various image processing steps like edge enhancement and smoothing before converting the image into grey-scale.

3. We then quantise the image into just having 5 to 10 greyness levels.

4. Now we map each greyness level to a digit, et voila, we have embedded the picture into a number.

5. It now remains to tweak some of the digits until we find a prime number that still looks like the image.

_Note: According to the prime number theorem, the density of prime numbers is asymptotically of order 1/log(n). Hence, if we have some number n with m digits, the number of primality tests that we expect to do until we hit a prime number is roughly proportional to m. Since we use the Baillie–PSW primality test, the overall expected computational complexity of our prime searching procedure is O(n\*log(n)³)._

## How to use

Simply get the `primify` command line tool via `pip install primify`.
You can also import the `PrimeImage` class from `primify.base` or use `cli.py` as a command-line script.

### Command-line tool

```
usage: primify [-h] [--image IMAGE_PATH] [--max_digits MAX_DIGITS] [--output_file OUTPUT_FILE] [-v]

Command-line tool for converting images to primes

optional arguments:
  -h, --help            show this help message and exit
  --image IMAGE_PATH    Source image to be converted
  --max_digits MAX_DIGITS
                        Maximal number of digits the prime can have
  --output_file OUTPUT_FILE
                        File name of the file containing the prime.
  -v                    Verbose output

Made by Levi B.
```

Thus, if you have the source image at `./source.png` and you want to convert it into a prime contained in `./prime/prime.txt` which has at most 5000 digits. Then you should run:

`primify -v --image ./source.png --max_digits 5000 --output_file prime/prime.txt`

### Importing the PrimeImage class

You can also simply import the `PrimeImage` class from `primify.base` and use that class in your own code. Check the [documentation](https://primify.readthedocs.io/) for details on how to interact with the underlying API.

### Additional Material

[Daniel Temkin](http://danieltemkin.com/) wrote a lovely article on his blog [esoteric.codes](https://esoteric.codes) giving some interesting insight and background for this tool. You can read it [here](https://esoteric.codes/blog/primify).
