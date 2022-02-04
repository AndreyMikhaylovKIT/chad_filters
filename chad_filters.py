"""
Created by Mikhaylov Andrey. 
Last update 03.01.2022.

andrey.mikhaylov@kit.edu

Simple filltration for multi-contrast data or tomography data.

Local median filtering, similar to salt/pepper filtration. 

"""

__version__ = '1.06_04.02.2022'



def chad_filter_tomo(image,f=3,vmin = 0,vmax = 4):
    """
    filtration with -log for tomography.

    Parameters
    ----------
    image : 2D numpy array of floats
        Your image.
    f : int, optional
        Radius of the filtration. The default is 3.
    vmin : float, optional
        minimum value, everething bellow will be considered as pepper. The default is 0.
    vmax : float, optional
        maximum value, everething higher will be considered as salt. The default is 4.

    Returns
    -------
    corr_log : 2D numpy array of floats 
        filtered -log of the image.

    """
    import numpy as np
    from skimage.filters import median
    from skimage.morphology import disk
    
    corr_log = -np.log(image)
    nan_check = np.isnan(corr_log)
    if np.any(nan_check):
        print('NaN values are present. Initiating correction precedure.')
        corr_log[nan_check] = vmax + 1
    else:
        print('NaN values are not present. No need for NaN correction.')
        
    filter_mask = np.logical_or(image > vmax,image < vmin)
    
    k = np.count_nonzero(filter_mask)
    
    print('Number of filter centers is ' + str(k))
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if filter_mask[i,j]:
                corr_log[i-f:i+f,j-f:j+f] = median(corr_log[i-f:i+f,j-f:j+f],disk(f))
                
    return corr_log
    
    

def chad_filter_MC(image,f=3,vmin = 0,vmax = 4):
    """
    filtration with general purpose

    Parameters
    ----------
    image : 2D numpy array of floats
        Your image.
    f : int, optional
        Radius of the filtration. The default is 3.
    vmin : float, optional
        minimum value, everething bellow will be considered as pepper. The default is 0.
    vmax : float, optional
        maximum value, everething higher will be considered as salt. The default is 4.

    Returns
    -------
    corr_log : 2D numpy array of floats 
        filtered image.

    """
    import numpy as np
    from skimage.filters import median
    from skimage.morphology import disk
    
    nan_check = np.isnan(image)
    if np.any(nan_check):
        print('NaN values are present. Initiating correction precedure.')
        image[nan_check] = vmax + 1
    else:
        print('NaN values are not present. No need for NaN correction.')
    
    filter_mask = np.logical_or(image > vmax,image < vmin)
    k = np.count_nonzero(filter_mask)
    
    print('Number of filter centers is ' + str(k))

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if filter_mask[i,j]:
                image[i-f:i+f,j-f:j+f] = median(image[i-f:i+f,j-f:j+f],disk(f))  
    
    image[image<0] = 0
    
    return image
    
    
