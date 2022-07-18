# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
import argparse




class Biconvex(object):
    
    '''
    Simple biconvex lens
    

    We assume the following variables are provided as inputs (D, R1, T, R2, D2, OD, all in mm; lambda in nm; integers N, M, h):

    And also an image sensor with size h x h mm and MxM pixels 
    
    '''
    
    def __init__(self, D, R1, T, R2, OD, D2, _lambda, N, M, h):
        super(Biconvex, self).__init__()

        # Input parameters of the problem
        # All length are converted in meters
        self.D = D*1e-3
        self.R1 = R1*1e-3  # R1 given in millimeters
        self.T = T*1e-3   # T given in millimeters
        self.R2 = -R2*1e-3  # R2 given in millimeters, negative because we have a biconvex lens
        self.OD = OD*1e-3  # OD given in millimeters
        self.D2 = D2*1e-3  # D2 given in millimeters
        self._lambda = _lambda*1e-9  # lambda given in nanometer
        self.N = N
        self.M = M
        self.h = h*1e-3
        
        # Calculated parameters of the lens
        self.n = self.get_refractive_index()  # refraction index
        self.f = self.get_focal_length()      # focal length
        self.f_N = self.get_f_number()        # f-number
        self.D_ = self.get_image_point()      # image point
        self.d_CoC = self.get_circle_confusion_diameter()  # Circle of Confusion diameter
        
        
        # Checking input parameters range
        self.checking_input_parameters()
        
        print(f"Calculated refractive index = {np.round(self.n, 3)}")
        print(f"Calculated focal length = {np.round(1000*self.f, 3)} mm")
        print(f"Calculated f-Number = {np.round(self.f_N, 3)}")
        print(f"Calculated point object image distance {np.round(1000*self.D_, 3)}mm")
        print(f"Calculated circle confusion diameter  {np.round(1000*self.d_CoC, 3)}mm")
        
        
    def checking_input_parameters(self):
        
        '''
        We make sure input paramaters are in an acceptable range
        '''
            
        assert self.D2 <= self.D_, "The point image is behind the sensor. Please adjust the point object position "
        assert self.OD <= 0.5*self.R1, "Aperture is too large"
        assert self.OD <= 0.5*abs(self.R2), "Aperture is too large"
        assert self.T <= 0.4*self.R1, "Tickness is too large"
        assert self.T <= 0.4*abs(self.R2), "Tickness is too large"
        assert self.h <= 5000, "Image sensor size is too large"
        assert self.M <= 1500, "Number of pixels is too large"
        

        return 0
        
        
    def get_refractive_index(self):
        
        '''
        Calculate the refractive index of the lens with the Cauchy's' equation:
            
            n(lambda) = A + B/lambda^2  with lambda in micrometers
        
        '''
        
        # For BK7 glass we have:
        A = 1.5046
        B = 0.00420
        
        return A + B/(self._lambda*1e6)**2  
 
    
    def get_focal_length(self):
        
        '''
        Calculate the focal lenght of the lens with the Lensmaker's equation:
        
        1/f = (n-1)[1/R1 - 1/R2 + (n-1)d/(nR1R2)]
    
        
        '''
              
        inv_f = (self.n-1)*(1.0/self.R1 - 1.0/self.R2 + (self.n - 1)*(self.T)/(self.n * self.R1 * self.R2) ) 
        
        return 1/inv_f


    def get_f_number(self):
        
        '''
        Calculate the f-number of the lens:
        
        f/N = f/OD with OD the aperture of the lens
        
        '''
        
        return (self.f)/self.OD 
    

    def get_image_point(self):
        
        '''
        Return the point image object  on-axis at distance D_:
        
        D: Position of point object
        D_: Position of point image
        f: focal length
        
       1/f = 1/D + 1/D_ ==> D_ = D*f/(D-f)
        
        '''
        
        return self.D*self.f/(self.D - self.f)

    def get_circle_confusion_diameter(self):
        
        '''
        Calculate the diameter of the Circle of Confusion(CoC):
        
        D2: distance between sensor plane and surface 2
        OD: Aperture of the lens
        D: Position of point object
        D_: Position of point image
        
        Because sensor is located at D2 instead of D_, the image forms a blur circle on the sensor.
        
        The diameter is given by d_CoC = OD(1-D2/D_)
        
        '''
        
        
        return self.OD * abs(1 - self.D2 /self.D_)
    
    
    
    def plot_energy_distribution(self, name='psf.png'):

        from random import shuffle

        

        delta_h = self.h/self.M  # size of each pixel (h/M)
        r_CoC = 0.5*self.d_CoC/delta_h # Radius of the CoC normaized by pixel width
        
       
        
    
        print(f"Calculated pixel size is {np.round(1000*delta_h, 3)}mm")
        print(f"Normalized Radius is {np.round(r_CoC, 3)}pixels")
        
        
        # We arbitrary choose to analyse abberations at the pixel located at the center of the sensor
        center = (0.5 + self.M//2, 0.5 + self.M//2) 
        
        fig, ax = plt.subplots()
        
        # Plot circle of confusion on sensor plane
        ax.add_patch(plt.Circle(center, r_CoC, fill=False))
        
        # Sampling
        
        # Rays sampled uniformly correspond to points uniformly sampled on the diameter segment
        r = list(abs(r_CoC*np.linspace(-1, 1, self.N))) 
        
        # Sampling uniformly in all directions
        angles = list((np.linspace(0, 2*np.pi, self.N)))
        shuffle(angles) 

        # Plot sampled points
        sampled_points = [(r[i]*np.cos(angles[i]), r[i]*np.sin(angles[i])) for i in range(len(r))]
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
    
    ap.add_argument("--name", type=str, default='tests.png',
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
    
    

    Lens = Biconvex(D, R1, T, R2, OD, D2,_lambda, N, M, h)
    
    Lens.plot_energy_distribution(name)



if __name__ == '__main__':
    main()


        

        
