# ENGSCI233: Lab - Sampled Data
# sdlab_functions.py

# PURPOSE:
# To IMPLEMENT cubic spline interpolation.

# PREPARATION:
# Notebook sampling.ipynb, ESPECIALLY Section 1.3.1 theory of cubic splines.

# SUBMISSION:
# - YOU MUST submit this file to complete the lab. 
# - DO NOT change the file name.

# TO DO:
# - COMPLETE the functions spline_coefficient_matrix(), spline_rhs() and spline_interpolation().
# - COMPLETE the docstrings for each of these functions.
# - TEST each method is working correctly by passing the asserts in sdlab_practice.py.
# - DO NOT modify the other functions.

import numpy as np


# **this function is incomplete**
#					 ----------
def spline_coefficient_matrix(xi):
    ''' Evaluate the coefficient matrix for interpolate for a range of data point

    '''

    # create an array of zeros with the correct dimensions
    #   **what are the correct dimensions? how to determine this from xi?**
    #   **use np.zeros() to create the array**

    # Loop over the subintervals, add matrix coefficients for equations:
    # - polynomial passes through lefthand point of subinterval
    # - polynomial passes through righthand point of subinterval
    #   **how many subintervals should there be (in terms of length of xi)?**
    #   **how to modify loop index so it jumps along a row in increments of 4?**
    #   **how to define width of the subinterval in terms of indices of xi?**
    #   **what values go into matrix A and how do they relate to subinterval width?**

    # Loop over neighbouring subintervals, add matrix coefficients for equations:
    # - polynomial gradient continuous at shared point
    # - polynomial second derivative continuous at shared point
    #   **how many shared points should there be (in terms of length of xi)?**
    #   **what values go into matrix A and how do they relate to subinterval width?**

    # For the beginning and end points, add matrix coefficients for equations:
    # - the polynomial second derivative is zero
    A=np.zeros((4*(len(xi)-1),4*(len(xi)-1)))
    initial=0
    index=0
    #Obtain the polynimal for the first half of the coefficient matrix
    for i in range((len(xi)-1)):
        y0 = [1, 0, 0, 0]
        y1 = [1, (xi[i + 1] - xi[i]), (xi[i + 1] - xi[i]) ** 2, (xi[i + 1] - xi[i]) ** 3]
        for j in range(4):
            A[2*i][initial+j]=y0[j]
            A[2*i+1][initial+j]=y1[j]
        initial=initial+4
        index+=1
    ini=0
    # Obtain the first derivate of polynimal at shared point
    for i in range(len(xi)-2):
        derivate=[1,2*(xi[i+1]-xi[i]),3*(xi[i+1]-xi[i])**2,0,-1]
        for j in range(5):
            A[2*(len(xi)-1)+i][j+1+ini]=derivate[j]
        ini=ini+4
    #Obtain the second derivate at shared points
    INI=0
    for i in range(len(xi)-2):
        secondderivate=[2,6*(xi[i+1]-xi[i]),0,0,-2]
        for j in range(len(secondderivate)):
            A[2*(len(xi)-1)+len(xi)-2+i][j+2+INI]=secondderivate[j]
        INI=INI+4
    #Obtain the second to last row in coefficient matrix
    A[2*(len(xi)-1)+len(xi)-2+len(xi)-2][2]=2
    #Obtain the last row in coefficient matrix
    last_derivate=[0,0,2,6*(xi[len(xi)-1]-xi[len(xi)-2])]
    for i in range(len(last_derivate)):
        A[2*(len(xi)-1)+len(xi)-2+len(xi)-1,((len(xi)-2)*4+i)]=last_derivate[i]
        
    return A

# **this function is incomplete**
#					 ----------
def spline_rhs(xi, yi):
    ''' **complete the docstring**
    '''
    b = np.zeros((4 * (len(xi) - 1)))
    b[0] = yi[0]
    b[4 * (len(xi) - 1) // 2 - 1] = yi[-1]
    for i in range(1, len(xi) - 1):
        b[2 * i - 1] = yi[i]
        b[2 * i] = yi[i]
    return b







# **this function is incomplete**
#					 ----------
def spline_interpolate(xj, xi, ak):
    ''' **complete the docstring**'''
    index=0
    initial=0
    size=0
    for i in range(len(xj)):
        if xj[i] <= np.max(xi):
            size+=1;
    yj = np.zeros(size)
    for i in range(size):
        if xj[i]>=xi[index]and xj[i]<=xi[index+1]:
            a=ak[initial:initial+4]
            s=(xj[i]-xi[index])
            yj[i]=a[0]+a[1]*s+a[2]*s**2+a[3]*s**3
        else:
            while (xj[i]>=xi[index] and xj[i]<=xi[index+1])==False:
                index+=1
                initial+=4
            if xj[i]>=xi[index]and xj[i]<=xi[index+1]:
                s = (xj[i] - xi[index])
                a=ak[initial:initial+4]
                yj[i]=a[0]+a[1]*s+a[2]*s**2+a[3]*s**3
    return yj



    # a=np.zeros((4))
    # y = np.zeros((len(xj)))
    # index = 0
    # initial = 0
    # for i in range(len(xj)):
    #     if xj[i] < xi[index + 1] and xj[i] > xi[index]:
    #         for j in range(4):
    #             a[j] = ak[initial + j]
    #         y[i] = a[0] + a[1] * (xj[i] - xi[index]) + a[2] * (xj[i] - xi[index]) ** 2 + a[3] * (xj[i] - xi[index]) ** 3
    #     else:
    #         while (xj[i] < xi[index + 1] and xj[i] > xi[index]) == False:
    #             index = index + 1
    #             initial = initial + 4
    #             if xj[i] < xi[index + 1] and xj[i] > xi[index]:
    #                 for j in range(4):
    #                     a[j] = ak[initial + j]
    #                 y[i] = a[0] + a[1] * (xj[i] - xi[index]) + a[2] * (xj[i] - xi[index]) ** 2 + a[3] * (
    #                         xj[i] - xi[index]) ** 3
    # return y


# this function is complete
def display_matrix_equation(A, b):
    ''''Prints the matrix equation Ax=b to the screen. '''
    #
    #     Parameters
    #     ----------
    #     A : np.array
    #         Matrix.
    #     b : np.array
    #         RHS vector.
    #
    #     Notes
    #     -----
    #     This will look horrendous for anything more than two subintervals.
    # '''

    # problem dimension
    n = A.shape[0]

    # warning
    if n > 8:
        print('this will not format well...')

    print(' _' + ' ' * (9 * n - 1) + '_  _       _   _        _')
    gap = ' '
    for i in range(n):
        if i == n - 1:
            gap = '_'
        str = '|{}'.format(gap)
        str += ('{:+2.1e} ' * n)[:-1].format(*A[i, :])
        str += '{}||{}a_{:d}^({:d})'.format(gap, gap, i % 4, i // 4 + 1) + '{}|'.format(gap)
        if i == n // 2 and i % 2 == 0:
            str += '='
        else:
            str += ' '
        if b is None:  # spline_rhs has not been implemented
            str += '|{}{}{}|'.format(gap, 'None', gap)
        else:
            str += '|{}{:+2.1e}{}|'.format(gap, b[i], gap)
        print(str)


# this function is complete
def get_data():
    # returns a data vector used during this lab
    xi = np.array([2.5, 3.5, 4.5, 5.6, 8.6, 9.9, 13.0, 13.5])
    yi = np.array([24.7, 21.5, 21.6, 22.2, 28.2, 26.3, 41.7, 54.8])
    return xi, yi


# this function is complete
def ak_check():
    # returns a vector of predetermined values
    out = np.array([2.47e+01, -4.075886048665986e+00, 0., 8.758860486659859e-01, 2.15e+01,
                    -1.448227902668027e+00, 2.627658145997958e+00, -1.079430243329928e+00, 2.16e+01,
                    5.687976593381042e-01, -6.106325839918264e-01, 5.358287012458253e-01, 2.22e+01,
                    1.170464160078432e+00, 1.157602130119396e+00, -2.936967278262911e-01, 2.82e+01,
                    1.862652894849505e-01, -1.485668420317224e+00, 1.677900564431842e-01, 2.63e+01,
                    -2.825777017172887e+00, -8.312872001888050e-01, 1.079137281294699e+00, 4.17e+01,
                    2.313177016138269e+01, 9.204689515851896e+00, -6.136459677234598e+00])
    return out


# this function is complete
def polyval(a, xi):
    ''' Evaluates a polynomial.

        Parameters
        ----------
        a : np.array
            Vector of polynomial coefficients.
        xi : np.array
            Points at which to evaluate polynomial.

        Returns
        -------
        yi : np.array
            Evaluated polynomial.

        Notes
        -----
        Polynomial coefficients assumed to be increasing order, i.e.,

        yi = Sum_(i=0)^len(a) a[i]*xi**i

    '''
    # initialise output at correct length
    yi = 0. * xi

    # loop over polynomial coefficients
    for i, ai in enumerate(a):
        yi = yi + ai * xi ** i

    return yi
