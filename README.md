

# Glass-Imaging Assignment

## Requirements
This code has been tested on python 3.8

## Run de code 
To run the code, do:

python run.py --D 125  --R1 50  --T 5 --R2 50 --OD 12.1   --D2 70  --_lambda 500 --N 15 --M 128 --h 100

The output is a png file in the same folder.

The parameters D, R1, T, R2, OD, D2, h are in mm. _lambda is in nm. Default values are in the file run.py (See function main())

## Analysis

- -- **Sampling effect** : Since it is a stochastic process, we need many ray per pixel to reduce noise and aliasing. Sampling affects the distribution of noise. 
- -- **Aberrations** : 
1. Defocus: D2 is set as an input parameter. Therefore, the detection surface is not automatically aligned with the focus. Light rays from the lens not coming to a perfect focus when imaging a point source. It is also known as disk of confusion or blur spot.

2. Chromatic aberration due to the inherent wavelength (red, green, blue) at which light travels, color do not converge at the same 
point behind the lens, resulting in a different circle of confusion.

- -- **Varying lambda** : When lamda increases, the blur spot becomes bigger.

- -- **Advantages Limitations of classical deconvolution filtering**:
The problem is formulated as an inverse filtering problem, where a blurred image is modeled as the result of the convolution with blur kernels, either spatially invariant or spatially varying. 
Some approaches assume that the blur kernel is known, and adopt classical image deconvolution algorithms such as Lucy-Richardson, or Wiener deconvolution. 
More realistically the blur kernel is unknown and has to be estimated with the sharp image, which it is not always easy.
They do not work very well in some scenario such as strong blur.

- -- **Advantages Limitations of NN**:

1. NN require paired blurry and sharp images for training. It is difficult to collect large-scale high-quality datasets with ground-truth. However blurry inputs can be artificially synthesized. However, there is still a gap between these synthetic images and real-world blurry images as the blur models are oversimplified.

2. Real-world images are not only corrupted due to lens aberrations, but also due to quantization, sensor noise, and other factors like low-resolution. One way to address this problem is to develop a unified image restoration model to recover high-quality images from the inputs corrupted by various nuisance factors.

3. Contrary to clasical deconvolution who estimate the actual distorsion kernel, NN trained on general images may perform poorly on images from domains that have different characteristics.

4. Computational cost: It requires significant effort to develop efficient deblurring algorithms directly on mobile devices. 





### Some Notes
