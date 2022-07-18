

# Glass-Imaging Assignment

## Requirements
This code has been tested on python 3.8

## Run de code 
To run the code, do:

python run.py --D 125  --R1 50  --T 5 --R2 50 --OD 12.1   --D2 70  --_lambda 500 --N 15 --M 128 --h 100

The output is a png file in the same folder.

The parameters D, R1, T, R2, OD, D2, h are in mm. _lambda is in nm. Default values are in the file run.py (See function main())

## Analysis

- -- **Sampling effect** : Since it is a stochastic process, we need many ray per pixel to reduce noise and aliasing. Sampling affect the distribution of noise. 
- -- **Aberrations** : 
1. Defocus: The detection surface is not aligned with the focus. Light rays from the lens not coming to a perfect focus when imaging a point source. It is also known as disk of confusion or blur spot.

2. Chromatic aberration due to the inherent wavelength (red, green, blue) at which light travels, color do not converge at the same 
point behind the lens, resulting in a different circle of confusion.

- -- **Varying lambda** : When lamda increases, the blur spot becomes bigger.

- -- **Algorithms** :







### Some Notes
