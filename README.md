# Glass Imaging

## VM
- The aitrainer is located at https://40.113.14.226:8000


## Run de code 
To run the code, do:

** python run.py --D 125  --R1 50  --T 5  --OD 12.1   --D2 70  --_lambda 500 --N 15 --M 128 --h 100  **



## Analysis

- -- **Sampling effect** : Since it is a stochastic process, many ray per pixels are needed to reduce noise and aliasing. Sampling affect the distribution of noise. 
- -- **Aberrations** : 
1. Defocus: The detection surface is not aligned with the focus. Light rays from the lens not coming to a perfect focus when imaging a point source. It is also known as disk of confusion or blur spot.

2. Chromatic aberration due to the inherent wavelength (red, green, blue) at which light travels, color do not converge at the same 
point behind the lens, resulting in a different circle of confusion.

- -- **Varying lambda** : When lamda increases, the blur spot becomes bigger.







### Some Notes
