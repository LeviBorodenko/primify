from PIL import Image

from primify.base import PrimeImage


def test_resize_with_pixel_limit(test_image: Image.Image, test_max_digits: int):
    resized_image = PrimeImage.resize_for_pixel_limit(test_image, test_max_digits)
    assert (
        test_max_digits * 0.8
        <= resized_image.width * resized_image.height
        <= test_max_digits
    )
