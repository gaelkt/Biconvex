
# -*- coding: utf-8 -*-

import numpy as np


class Ray(object):
    
    '''
        At a given point along the optical axis, each ray can
        be uniquely represented by three numbers:
            y: Distance from optical axis (y=0 if point on axis)
        alpha: Angle with respect to optical axis
            n: Refractive index of the material where the point is located (n=1 for air)
    
    '''
    
    def __init__(self, y, alpha, n):
        super(Ray, self).__init__()


        self.y = y
        self.alpha = alpha 
        self.n = n  
        
    
    def vector_representation(self):
        
        '''
        Vector representation of the ray at a given point for mathematical purpose
        v = [n*alpha, y]
        
        '''
        
        return [self.n*self.alpha, self.y]


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
        self.delta_h = self.h/self.M  # size of each pixel (h/M)

        
        
        # Checking input parameters range
        self.checking_input_parameters()
        
        print(f"Calculated refractive index = {np.round(self.n, 3)}")
        print(f"Calculated focal length = {np.round(1000*self.f, 3)} mm")
        print(f"Calculated f-Number = {np.round(self.f_N, 3)}")
        print(f"Calculated point object image distance {np.round(1000*self.D_, 3)}mm")
        print(f"Calculated circle confusion diameter  {np.round(1000*self.d_CoC, 3)}mm")
        print(f"Calculated pixel size   {np.round(1000*self.delta_h, 3)}mm")
        
        
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



    def object_lens_matrix(self):
        
        '''
        This functions gives the matrix that models how to get the input ray ri at the lens from the ray rp at point object
        
        Ray at point object: rp (refractive index np=1)
        Input ray at surface 1: ri (refractive index ni=1)
        
        With Snell law we have: 1*alpha_i = 1*alpha_p     (alpha does not change)
        With paraxial approximation: yi = D*alpha_p + yp, point object is locacated at a distance D from surface 1
        
        vector representation: Let's vp = [1*alpha_p, y_p] , vi = [1*alpha_i, yi]  
                                        
                                    vi = T*vp
        
                                    Tp = [[1, 0],
                                          [D, 1]]
                                    
                                    
        
        '''
             
        return [[1, 0], [self.D, 1]]
    
    def refraction_matrix(self):
        
        '''
        
        This functions gives the matrix that transforms an input ray at the lens to an output ray
        

        ri: Input ray at surface 1 (refractive index ni=1)
        
        ro: Output ray at surface 2 (refractive index no=1)
        
        
        Intermediate rays
        - Input ray ri will be first refracted at surfaced 1 to give ray r1 (refractive index n):
            With Snell law we have: n*alpha_1 = 1*alpha_i - (n-1)*y1/R1
                                            y1 = yi
              
            vector representation: Let's vi = [1*alpha_i, y_i]  and v1 = [n*alpha_1, y1]   
            
                                            R1 = [[1, -(n-1)/R1],
                                                   [0,       1]]                     
            ==> v1 = R1*vi  
            
       
        - Ray r1 will be transfered to surface 2 and will give r2(refractive index n)
            With Snell law we have: n*alpha_2 = n*alpha_1
            With paraxial approximation: y2 = d*alpha1 + y1
            
            T = [[1, 0], [d/n, 1]]
            
            ==> v2 = T*v1
            
           
        - Ray r2 will be refracted at surface 2 to give output ray ro (refractive index 1):
            With Snell law we have: 1*alpha_o = n*alpha_2 - (1-n)*y2/R2
                                           yo = y2
                                           
             R2 = [[1, (n-1)/R2],
                  [0,       1]]       

        
            ==> vo = R2*v2    


        Finally:
             vo = R2*T*R1*vi = A*vi

            ===> A = [[1+ (n-1)d/(n*R2), -1/f],
                          [d/n,     1-(n-1)d/(n*R1)]]                     
            
        '''
        
        a11 = 1+ self.T * (self.n - 1)/(self.n * self.R2)
        a12 = -1/self.f
        a21 = self.T/self.n
        a22 = 1- self.T * (self.n - 1)/(self.n * self.R1)
        
        
        return [[a11, a12], [a21, a22]]
    


    def lens_sensor_plane_matrix(self):
        
        '''
        This functions gives the matrix that models how to get the ray rs at the sensor plane from the output ray ro at the lens
        
        Output ray ray at surface 2: ro (refractive index no=1)
        Input ray at sensor plane: rs (refractive index ns=1)
        
        With Snell law we have: 1*alpha_s = 1*alpha_o 
        With paraxial approximation: ys = D2*alpha_s + ys, sensor plabe is locacated at a distance D2 from surface 2
        
        vector representation: Let's vs = [1*alpha_s, y_s] , vo = [1*alpha_o, yo]  
                                        
                                    vs = Ts*vo
        
                                    Tp = [[1, 0],
                                          [D2, 1]]
                                    
                                    
        
        '''
             
        return [[1, 0], [self.D2, 1]]
    


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
    
    
    

 

        


