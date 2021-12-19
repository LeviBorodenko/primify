import math
from pathlib import Path
from typing import Literal, Union
import logging
from PIL import Image, ImageFilter
from sympy import nextprime

logging.basicConfig()
logger = logging.getLogger(__file__)

GLYPH_ASPECT_RATIO = 0.45
BRIGHTNESS_ORDERED_DIGITS = [1, 7, 3, 9, 8]


class PrimeImage:
    """
    This class provides methods to convert any image into a prime number.

    We use the python package Pillow to do all the image processing
    and sympy to check for primality.


    Arguments:

        image_path (Path): Path to image.

        max_digits (int): Maximal number of digits in the resulting prime.

        converion_method (int): number between 0 and 2. Play around to see
            which one produces the clearest image.

        verbose (bool): Verbose status reporting in terminal if True

        output_file (Path): Output file (default: "./prime.txt")

    Note:

        The computational complexity is O(d*log(d)^3) in the number of digits

    Example:

        if you have the source image at `./source.png` and you want to convert it into a prime contained in `./prime/prime.txt` which has at most 5000 digits and using conversion method 0 (other options are 1 or 2). Then you should run:

        `primify -v --image ./source.png --max_digits 5000 --method 0 --output_dir ./prime/ --output_file prime.txt`



    """

    def __init__(
        self,
        image_path: Union[Path, str] = Path("./prime.png"),
        max_digits: int = 5000,
        conversion_method: Literal[0, 1, 2, 3] = 1,
        output_file_path: Union[Path, str] = Path("./prime.txt"),
        verbose: bool = False,
    ):

        self.image_path = Path(image_path)
        self.max_digits = max_digits

        # saving conversion method.
        self.conversion_method = conversion_method

        if verbose:
            logger.setLevel(logging.DEBUG)

        # check if verbose is boolean
        if not isinstance(verbose, bool):
            raise ValueError("Verbosity must be True or False")

        # check if max_digits is and integer and greater than 10
        if not (isinstance(self.max_digits, int) or (self.max_digits < 10)):
            raise ValueError("max_digits should be an integer and > 10")

        # loading the Pillow image object
        self.im = Image.open(self.image_path)

        # saving output file path
        self.output_file_path = Path(output_file_path)

    @staticmethod
    def resize_for_pixel_limit(image: Image.Image, max_pixels: int) -> Image.Image:
        """
        We resize the image to contain at most max_size pixels

        description:
            The reason is that we don't want to find too large primes
        """

        image = image.copy()
        x, y = image.size

        # we need to squash y since a number is usually higher than it is wide
        y = int(y * GLYPH_ASPECT_RATIO)

        # to make sure that the image has less than max_pixels pixels, we need to scale.
        scale_factor = (x * y / max_pixels) ** 0.5
        x_scaled, y_scaled = int(x / scale_factor), int(y / scale_factor)

        image = image.resize((x_scaled, y_scaled))

        logger.debug(f"Resized image to be {image.size[0]}x{image.size[1]} pixels.")
        return image

    @staticmethod
    def reshape_number(number: int, width: int) -> str:

        result = ""
        for index, digit in enumerate(str(number)):

            # take a line break after we reach the width
            if index % width == 0 and index > 0:
                result += "\n"

            result += digit

        return result

    @staticmethod
    def image_to_number(image: Image.Image):
        n_levels = len(BRIGHTNESS_ORDERED_DIGITS)

        # smooth the image to have better regions of constancy after quanitsation
        image = image.filter(ImageFilter.MinFilter)

        # now convert to quantized greyscale
        grey_scale_image = image.convert("L").quantize(n_levels)

        grey_scale_image.show()


if __name__ == "__main__":

    instance = PrimeImage(
        image_path="examples/images/tao.png", max_digits=10000, verbose=True
    )
    PrimeImage.image_to_number(instance.im)
