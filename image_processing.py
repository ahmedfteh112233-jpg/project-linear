import numpy as np


def convert_to_grayscale(image):
    """
    Convert RGB image to Grayscale.
    """

    image = image.astype(np.float32)

    red = image[:, :, 0]
    green = image[:, :, 1]
    blue = image[:, :, 2]

    gray = (
        0.299 * red +
        0.587 * green +
        0.114 * blue
    )

    gray = np.clip(gray, 0, 255).astype(np.uint8)

    return np.stack((gray, gray, gray), axis=2)


def adjust_brightness(image, value):
    """
    Increase or decrease image brightness.
    """

    image = image.astype(np.int16)

    result = image + int(value)

    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)


def horizontal_flip(image):
    """
    Flip image horizontally.
    """

    return image[:, ::-1, :].copy()


def convert_to_black_white(image, threshold=127):
    """
    Convert image to pure Black and White.
    """

    gray_image = convert_to_grayscale(image)

    gray = gray_image[:, :, 0]

    result = np.where(
        gray >= threshold,
        255,
        0
    ).astype(np.uint8)

    return np.stack((result, result, result), axis=2)