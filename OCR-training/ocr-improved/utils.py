import cv2
def read(image):
    image = cv2.imread(image)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def resize_image(image, max_scale, max_size):
    """Obtain the optimal resized image subject to a maximum scale
    and maximum size.

    Args:
        image: The input image
        max_scale: The maximum scale to apply
        max_size: The maximum size to return
    """
    if max(image.shape) * max_scale > max_size:
        # We are constrained by the maximum size
        scale = max_size / max(image.shape)
    else:
        # We are contrained by scale
        scale = max_scale
    return cv2.resize(
            image, dsize=(int(image.shape[1] * scale), int(image.shape[0] * scale))
        )
    