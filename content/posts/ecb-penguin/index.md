---
title: "Exploring an Encrypted Penguin with AES-ECB"
date: 2020-04-04
tags: ["Security", "Programming"]
description: "Exploring the Penguin in AES-ECB Mode"
summary: "We've seen the image of a penguin encrypted with AES-ECB on Wikipedia before, but what happens if we add a tiny bit of noise to the equation?"
ogimage: https://tonybox.net/posts/ecb-penguin/tux-enc.png
---

<small>**Quick Warning**: don't roll your own crypto, and don't use ECB mode unless you *really* know what you're doing. The example below illustrates some interesting properties of AES in ECB mode, but shouldn't be taken to minimize the risk of using a mode like ECB.  There are other risks apart from seeing penguins, like [chosen prefix oracles](https://cryptopals.com/sets/2/challenges/12) that can reveal plaintext.</small>

# Encrypting a Penguin

The simplest way to encrypt large amounts of data with a block cipher like AES is to divide your data into blocks of equal size (in AES, the size being the key size), and to encrypt each block individually.  This is called [ECB (Electronic Codebook)](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#ECB) mode, and while it is simple, it suffers from some major drawbacks.  Specifically, AES in ECB mode leaks information about patterns in your plain text. Here, we're going to explore what kind of patterns are leaked, and what kind of patterns are not leaked.

The reason AES (and other algorithms) in ECB mode leak information is simple: they encrypt blocks of data, and if they encounter the same block of data twice, they will produce the same encrypted result twice. This leaks information, showing you when two identical and aligned (usually 128-bit or 256-bit) blocks of data are the same, and opening up some avenues of attack (including active attacks, like replay attacks).  

On wikipedia and elsewhere, a diagram is often shown to illustrate this point. In this diagram, we take an image of a penguin and encrypt it using AES with 128 bit blocks in ECB mode, revealing that the penguin is still very visible underneath:

{{% svg "drawing.svg"  %}}

But here, we used a perfect image of a penguin - an uncompressed image, with a background of perfect white, with clearly defined areas of higher and lower noise.  We can see some interesting properties about the penguin in the ciphertext - the white background is pure white, and appears as identical repeating blocks when encrypted with ECB; the belly is a bit noisy, and appears much noisier as the diffusion of AES amplifies the noise significantly; and the detail of the face is gone completely.

Keep in mind that a regular photograph may exhibit some of these characteristics as well, and have some discernable patterns, possibly as a result of image compressing reducing the entropy in some areas of an image, but the real world tends to be noisy, and a real image will tend to be much noisier than our perfect image of a penguin.

# Diffusion of Input Data

AES is a fairly secure algorithm designed to exhibit the property of [diffusion](https://en.wikipedia.org/wiki/Confusion_and_diffusion). In an ideal encryption algorithm exhibiting diffusion, flipping any one bit in the input should have a 50% chance of impacting *each* bit in the output.  That is, changing a *single bit* in the input *completely scrambles* the output.  

The issue with AES in ECB mode is that this diffusion occurs with respect to each block individually. In ECB, flipping a bit in one block has no chance of flipping any bits in another block, whereas with modes like [CBC](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_(CBC)), flipping a bit can effectively scramble the output of all later blocks.

But, for us, the property of diffusion also means that adding a tiny bit of uniform noise *to the entire image* will completely scramble the output, even in ECB mode.  

# Hiding a Penguin in the Noise

Here, I've applied a simple algorithm that flips the least significant bit of 15% of the bytes that make up the image of a penguin.  This is similar to a common [steganographic](https://en.wikipedia.org/wiki/Steganography) technique, except I'm only adding a little bit of noise to the image.  You can see the whole code [here](https://github.com/tonyb486/tonybox.net/blob/master/content/posts/ecb-penguin/penguin.py), although here is the relevant chunk:

{{< highlight py>}}
imarray = np.uint8([ i^1 if random.random()>0.85 else i for i in imarray ])
{{< / highlight >}}

With that change, the original image is left looking virtually identical to the naked eye, but the small amount of uniform noise has seemingly completely scrambled the resulting encrypted image:

{{% svg "drawing2.svg"  %}} 

And with that, you can see the property of diffusion, and slightly better understand the nuance of the risks of using AES-ECB.  ECB still reveals information about the ciphertext of your image, and small amounts of information can still break cryptosystems, so **please don't take this as a reason to use ECB**.  

# Hiding Some of a Penguin

Keep in mind that adding the noise uniformly to 15% of the bytes means that most blocks will end up getting a bit flipped, and so we effectively spread the noise out to affect every block, scrambling the penguin.

Here, we can see what happens if we add slightly less noise, flipping the least significant bit in about 3% of the bytes.  As shown below, the penguin is more scrambled than without the noise, as the uniform noise is amplified in the blocks where it is present, but the noise doesn't affect every block and the penguin is still somewhat visible underneath:

{{% svg "drawing3.svg"  %}}

Finally, even if your input data is noisy, even if you intentionally make it noisy, ECB is usually not a good idea, particularly when we have better modes available for most, if not all, applications.

Security is hard, and small changes and nuance can make a big difference.


