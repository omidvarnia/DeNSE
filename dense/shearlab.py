### Shearlab module for Shearlab.jl backend in python

# Import libraries
from julia.api import Julia
import matplotlib.pyplot as plt
import pylab
from numpy import ceil
from numpy.fft import fft2, ifft2, fftshift, ifftshift
import numpy as np

__all__ = ('load_julia_with_Shearlab','load_image','imageplot','Shearlabsystem2D','getshearletsystem2D',
            'sheardec2D','shearrec2D','sheardecadjoint2D','shearrecadjoint2D')

# Python library for shearlab.jl

# Function to load Shearlab
def load_julia_with_Shearlab():
        
    j = Julia(compiled_modules=False)
    # Importing base
    j.eval('using Shearlab') # Importing Shearlab in Julia
    j.eval('using PyPlot') # Importing PyPlot in Julia
    j.eval('using Images') # Importing Images in Julia
    return j


j = load_julia_with_Shearlab()


# Function to load images with certain size
def load_image(name, n, m=None, gpu=None, square=None):
    if m is None:
        m = n
    if gpu is None:
        gpu = 0
    if square is None:
        square = 0
    command = ('Shearlab.load_image("{}", {}, {}, {}, {})'.format(name,
               n, m, gpu, square))
    return j.eval(command)


# Function to plot images
def imageplot(f, str=None, sbpt=None):
    """
        Plot an image generated by the library
    """
    if str is None:
        str = ''
    if sbpt is None:
        sbpt = []
    if sbpt != []:
        plt.subplot(sbpt[0], sbpt[1], sbpt[2])
    imgplot = plt.imshow(f, interpolation='nearest')
    imgplot.set_cmap('gray')
    plt.axis('off')
    if str != '':
        plt.title(str)


# Class of shearlet system in 2D
class Shearletsystem2D:
    def __init__(self, shearlets, size, shearLevels, full, nShearlets,
                 shearletIdxs, dualFrameWeights, RMS, isComplex):
        self.shearlets = shearlets
        self.size = size
        self.shearLevels = shearLevels
        self.full = full
        self.nShearlets = nShearlets
        self.shearletIdxs = shearletIdxs
        self.dualFrameWeights = dualFrameWeights
        self.RMS = RMS
        self.isComplex = isComplex


# Function to generate de 2D system
def getshearletsystem2D(rows, cols, nScales, shearLevels=None,
                        full=None,
                        directionalFilter=None,
                        quadratureMirrorFilter=None):
    if shearLevels is None:
        shearLevels = [float(ceil(i / 2)) for i in range(1, nScales + 1)]
    if full is None:
        full = 0
    if directionalFilter is None:
        directionalFilter = 'Shearlab.filt_gen("directional_shearlet")'
    if quadratureMirrorFilter is None:
        quadratureMirrorFilter = 'Shearlab.filt_gen("scaling_shearlet")'
    j.eval('rows=' + str(rows))
    j.eval('cols=' + str(cols))
    j.eval('nScales=' + str(nScales))
    j.eval('shearLevels=' + str(shearLevels))
    j.eval('full=' + str(full))
    j.eval('directionalFilter=' + directionalFilter)
    j.eval('quadratureMirrorFilter=' + quadratureMirrorFilter)
    j.eval('shearletsystem=Shearlab.getshearletsystem2D(rows, '
           'cols, nScales, shearLevels, full, directionalFilter, '
           'quadratureMirrorFilter) ')
    shearlets = j.eval('shearletsystem.shearlets')
    size = j.eval('shearletsystem.size')
    shearLevels = j.eval('shearletsystem.shearLevels')
    full = j.eval('shearletsystem.full')
    nShearlets = j.eval('shearletsystem.nShearlets')
    shearletIdxs = j.eval('shearletsystem.shearletIdxs')
    dualFrameWeights = j.eval('shearletsystem.dualFrameWeights')
    RMS = j.eval('shearletsystem.RMS')
    isComplex = j.eval('shearletsystem.isComplex')
    j.eval('shearletsystem = 0')
    return Shearletsystem2D(shearlets, size, shearLevels, full, nShearlets,
                            shearletIdxs, dualFrameWeights, RMS, isComplex)


# Shearlet Decomposition function
def sheardec2D(X, shearletsystem):
    coeffs = np.zeros(shearletsystem.shearlets.shape, dtype=complex)
    Xfreq = fftshift(fft2(ifftshift(X)))
    for i in range(shearletsystem.nShearlets):
        coeffs[:, :, i] = fftshift(ifft2(ifftshift(Xfreq * np.conj(
                                   shearletsystem.shearlets[:, :, i]))))
    return coeffs.real


# Shearlet Recovery function
def shearrec2D(coeffs, shearletsystem):
    X = np.zeros(coeffs.shape[:2], dtype=complex)
    for i in range(shearletsystem.nShearlets):
        X = X + fftshift(fft2(
            ifftshift(coeffs[:, :, i]))) * shearletsystem.shearlets[:, :, i]
    return (fftshift(ifft2(ifftshift((
            X / shearletsystem.dualFrameWeights))))).real


# Shearlet Decomposition adjoint function
def sheardecadjoint2D(coeffs, shearletsystem):
    X = np.zeros(coeffs.shape[:2], dtype=complex)
    for i in range(shearletsystem.nShearlets):
        X = X + fftshift(fft2(
            ifftshift(coeffs[:, :, i]))) * np.conj(
            shearletsystem.shearlets[:, :, i])
    return (fftshift(ifft2(ifftshift(
            X / shearletsystem.dualFrameWeights)))).real


# Shearlet Recovery adjoint function
def shearrecadjoint2D(X, shearletsystem):
    coeffs = np.zeros(shearletsystem.shearlets.shape, dtype=complex)
    Xfreq = fftshift(fft2(ifftshift(X)))
    for i in range(shearletsystem.nShearlets):
        coeffs[:, :, i] = fftshift(ifft2(ifftshift(
            Xfreq * shearletsystem.shearlets[:, :, i])))
    return coeffs.real


