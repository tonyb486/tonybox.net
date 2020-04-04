import math, random
import numpy as np
from Crypto.Cipher import AES
from PIL import Image

# Quick and dirty function to ECB a raw image, so useful!
def ecb_image(imobj):
    crypt = AES.new(b"SEE THE PENGUIN!", AES.MODE_ECB)
    # Convert to array
    imarray = np.asarray(imobj)
    imshape = imarray.shape
    # Pad and encrypt
    padbytes = (math.ceil(imarray.size/128)*128)-imarray.size
    imbytes = imarray.tobytes() + (b"\xff"*padbytes)
    encrypted = crypt.encrypt(imbytes)
    # Unpad and return
    imarray = np.frombuffer(encrypted, dtype=np.uint8)
    imarray = np.reshape(imarray[0:imarray.size-padbytes], imshape)
    return Image.fromarray(imarray, mode=imobj.mode)

def noise_image(imobj, level):
    # Convert to array
    imarray = np.asarray(imobj)
    imshape = imarray.shape
    # Convert to one-dimensional
    imarray = np.reshape(imarray, imarray.size)
    # Add some noise at random
    imarray = np.uint8([ i^1 if random.random()>(1-level) else i for i in imarray ])
    # Return an image
    imarray = np.reshape(imarray, imshape)
    return Image.fromarray(imarray, mode=imobj.mode)


# Read the Image
image = Image.open("tux.png")

# Encrypt the Image
encimage = ecb_image(image)
encimage.save("tux-enc.png")

# Add some noise
noisyimage = noise_image(image, 0.15)
noisyimage.save("tux-noisy.png")

# Encrypt the noisy
nencimage = ecb_image(noisyimage)
nencimage.save("tux-noisy-enc.png")

# Add slightly less noise
noisyimage = noise_image(image, 0.03)
noisyimage.save("tux-slightly-noisy.png")

# Encrypt the noisy
nencimage = ecb_image(noisyimage)
nencimage.save("tux-slightly-noisy-enc.png")
