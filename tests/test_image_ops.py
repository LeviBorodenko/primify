from PIL import Image
from sympy import isprime

from primify.base import PrimeImage
from primify.prime_finder import NextPrimeFinder


def test_prime_finder():
    almost_prime = 2 ** 67 - 2
    instance = NextPrimeFinder(almost_prime, n_workers=1)
    assert isprime(instance.find_next_prime())


def test_resize_with_pixel_limit(test_image: Image.Image, test_max_digits: int):
    resized_image = PrimeImage.resize_for_pixel_limit(test_image, test_max_digits)
    assert (
        test_max_digits * 0.8
        <= resized_image.width * resized_image.height
        <= test_max_digits
    )
