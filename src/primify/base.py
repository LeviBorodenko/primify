from dataclasses import dataclass
import multiprocessing as mp
import math
from pathlib import Path
from typing import Iterator, List, Literal, Tuple, Union
import logging
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from sympy import nextprime

logging.basicConfig()
logger = logging.getLogger(__file__)

GLYPH_ASPECT_RATIO = 0.45
BRIGHTNESS_ORDERED_DIGITS: List[int] = [1, 7, 3, 9, 8]


@dataclass
class ImageNumber:
    value: int
    image_width: int

    def __str__(self) -> str:

        result = ""
        for index, digit in enumerate(str(self.value)):

            # take a line break after we reach the width
            if index % self.image_width == 0 and index > 0:
                result += "\n"

            result += digit

        return result


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
    def quantize_image(image: Image.Image) -> Image.Image:

        n_levels = len(BRIGHTNESS_ORDERED_DIGITS)

        # enhance it for better contrast
        # enhancer = ImageEnhance.Contrast(image)
        # image = enhancer.enhance(contrast)

        # smooth the image to have better regions of constancy after quanitsation
        image = image.filter(ImageFilter.MinFilter)

        # now convert to quantized greyscale
        grey_scale_image = image.convert("L")

        # make sure we use the entire digit pallet
        grey_scale_image = ImageOps.autocontrast(grey_scale_image)

        quantized_image = grey_scale_image.quantize(n_levels)
        quantized_image.show()
        return quantized_image

    @staticmethod
    def quantized_image_to_number(image: Image.Image) -> ImageNumber:
        # use quantized levels as lookup indexes into BRIGHTNESS_ORDERED_DIGITS
        digits = ""
        for brightness_index in image.getdata():
            digits += f"{BRIGHTNESS_ORDERED_DIGITS[brightness_index]}"

        return ImageNumber(value=int(digits), image_width=image.width)

    def _get_raw_number(self) -> ImageNumber:

        quantized_image = PrimeImage.quantize_image(self.im)
        # first we resize the image to only contain at most as many pixels as we want digits in the prime
        resized_image = PrimeImage.resize_for_pixel_limit(
            quantized_image, self.max_digits
        )

        # now we read the image as a number
        image_number = PrimeImage.quantized_image_to_number(resized_image)

        return image_number

    def get_prime(self) -> ImageNumber:

        raw_image_number = self._get_raw_number()
        next_prime = nextprime(raw_image_number.value)
        assert isinstance(next_prime, int)

        return ImageNumber(next_prime, raw_image_number.image_width)

    @staticmethod
    def find_next_prime_sharded(
        raw_image_number: ImageNumber, n_shard: int = 0
    ) -> ImageNumber:

        raw_number_shard = (
            raw_image_number.value + math.log(raw_image_number.value) * n_shard
        )
        next_prime = nextprime(raw_number_shard)
        assert isinstance(next_prime, int)

        return ImageNumber(next_prime, raw_image_number.image_width)

    @staticmethod
    def find_next_prime_worker(
        raw_image_number: ImageNumber, n_shard: int, found_prime: mp._EventType
    ):
        if not found_prime:
            next_primePrimeImage.find_next_prime_sharded(raw_image_number, n_shard)


class NextPrimeFinder:
    def __init__(self, value: int, n_workers: int = 1):
        self.value = int(value)
        self.n_workers = n_workers

    def prime_candidates(self) -> Iterator[int]:
        candidate = self.value
        while True:
            if candidate % 6 in [1, 5]:
                yield candidate
            else:
                candidate += 1


if __name__ == "__main__":

    instance = PrimeImage(
        image_path="examples/images/tao.png", max_digits=2500, verbose=True
    )

    prime, width = instance.get_prime()
    print(PrimeImage.reshape_number(prime, width))
