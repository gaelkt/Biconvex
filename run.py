
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import argparse
from random import shuffle

from utils import Biconvex, Ray



def plot_psf(lens, name='output.png'):
    
    delta_h = lens.delta_h  # size of each pixel (h/M)
    r_CoC = 0.5*lens.d_CoC/delta_h # Radius of the CoC normaized by pixel width
          
    # Object is located at distance D, and aperture lens is OD
    # Maximum angle for ray is given by
    alpha_max = np.arctan(0.5*lens.OD/lens.D)
    
    # Uniform sampling in angle grid
    alphas = np.linspace(-alpha_max, alpha_max, lens.N)
    
    # For each ray leaving the point object, we evaluate the image ray at sensor plane
    radius = []
    for alpha in alphas:
        
        # Ray at point object on the axis(y=0, n=1) 
        rp = Ray(y=0, alpha=alpha, n=1)
        vp = rp.vector_representation()
        
        # Path point object-->lens(surface1)
        Tp = lens.object_lens_matrix()
        vi = np.dot(Tp, vp)
        
        # Path surface1--->surface2
        A = lens.refraction_matrix()
        vo = np.dot(A, vi)
        
        # Path surface2---> sensor plane
        Ts = lens.lens_sensor_plane_matrix()
        vs = np.dot(Ts, vo)
        
        # radius on sensor plane normalized by pixel sensor
        radii_alpha = vs[1]/delta_h
        radius.append(radii_alpha)
        
    
    # We arbitrary choose to analyse abberations at the pixel located at the center of the sensor
    center = (0.5 + lens.M//2, 0.5 + lens.M//2) 
        
    fig, ax = plt.subplots()
        
    # Plot circle of confusion on sensor plane
    ax.add_patch(plt.Circle(center, r_CoC, fill=False))  
        

    # We want to represent sensor plane in 2D
    # We assign a random angle to each image
    angles = list((np.linspace(0, 2*np.pi, lens.N)))
    shuffle(angles) 

    # Plots image point on sensor plane
    sampled_points = [(radius[i]*np.cos(angles[i]), radius[i]*np.sin(angles[i])) for i in range(len(radius))]
    for k in sampled_points:
        plt.scatter(center[0] + k[0], center[1] + k[1], 30)

    plt.xlim([center[0]-3, center[0]+3])
    plt.ylim([center[1]-3, center[1]+3])
    plt.grid(True)
    plt.xlabel('Pixel number along X')
    plt.ylabel('Pixel number along Y')
    plt.title("Sensor plane with CoC and sampled points")
    fig.set_size_inches(6, 6)
        
    plt.show()
    fig.savefig(name)
        
    return 0
    


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("--D", type=float, default=125,
                    help="point source distance in mm")
    
    ap.add_argument("--R1", type=float, default=50,
                    help="radius R1 on the subject side in mm")    
    
    ap.add_argument("--T", type=float, default=5,
                    help="Thickness in mm")    
    
    ap.add_argument("--R2", type=float, default=50,
                    help="radius R2 in mm") 
    
    ap.add_argument("--D2", type=float, default=70,
                    help="Distance between surface2 and sensor plane in mm")   
    
    ap.add_argument("--OD", type=float, default=12.195,
                    help="Aperture in mm")  


    ap.add_argument("--_lambda", type=float, default=500,
                    help="Lambda in nm")  

    ap.add_argument("--N", type=int, default=15,
                    help="uniformly sampled in angle grid of N rays")  

    ap.add_argument("--h", type=int, default=100,
                    help="Size of sensor in mm")      
 
    ap.add_argument("--M", type=int, default=128,
                    help="Number of pixels per axis") 
    
    ap.add_argument("--name", type=str, default='psf.png',
                    help="Image name")
   
    args = ap.parse_args()

    D = args.D 
    R1 = args.R1 
    T = args.T 
    R2 = args.R2 
    D2 = args.D2 
    OD = args.OD
    _lambda = args._lambda
    N = args.N
    M = args.M
    h = args.h 
    name = args.name 
    
    # Instance of the lens
    lens = Biconvex(D, R1, T, R2, OD, D2,_lambda, N, M, h)
    
    # Plot psf
    plot_psf(lens, name=name)
    

if __name__ == '__main__':
    main()