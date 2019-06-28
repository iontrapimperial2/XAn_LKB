# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:41:14 2018

@author: JohannesMHeinrich
"""

import numpy as np
import matplotlib.pyplot as plt
alpha = 5
beta = 3
N = 500
DIM = 2

#np.random.seed(2)
#
## Generate random points on the unit circle by sampling uniform angles
#theta = np.random.uniform(0, 2*np.pi, (N,1))
#eps_noise = 0.2 * np.random.normal(size=[N,1])
#circle = np.hstack([np.cos(theta), np.sin(theta)])
#
## Stretch and rotate circle to an ellipse with random linear tranformation
#B = np.random.randint(-3, 3, (DIM, DIM))
#noisy_ellipse = circle.dot(B) + eps_noise
#
## Extract x coords and y coords of the ellipse as column vectors
#X = noisy_ellipse[:,0:1]
#Y = noisy_ellipse[:,1:]
#
## Formulate and solve the least squares problem ||Ax - b ||^2
#A = np.hstack([X**2, X * Y, Y**2, X, Y])
#b = np.ones_like(X)
#x = np.linalg.lstsq(A, b)[0].squeeze()
#
## Print the equation of the ellipse in standard form
#print('The ellipse is given by {0:.3}x^2 + {1:.3}xy+{2:.3}y^2+{3:.3}x+{4:.3}y = 1'.format(x[0], x[1],x[2],x[3],x[4]))
#
## Plot the noisy data
#plt.scatter(X, Y, label='Data Points')
#
## Plot the original ellipse from which the data was generated
#phi = np.linspace(0, 2*np.pi, 1000).reshape((1000,1))
#c = np.hstack([np.cos(phi), np.sin(phi)])
#ground_truth_ellipse = c.dot(B)
#plt.plot(ground_truth_ellipse[:,0], ground_truth_ellipse[:,1], 'k--', label='Generating Ellipse')
#
## Plot the least squares ellipse
#x_coord = np.linspace(-5,5,10)
#y_coord = np.linspace(-5,5,10)
#X_coord, Y_coord = np.meshgrid(x_coord, y_coord)
#Z_coord = x[0] * X_coord ** 2 + x[1] * X_coord * Y_coord + x[2] * Y_coord**2 + x[3] * X_coord + x[4] * Y_coord
#plt.contour(X_coord, Y_coord, Z_coord, levels=[1], colors=('r'), linewidths=2)
#plt.grid()
#
#plt.legend()
#plt.xlabel('X')
#plt.ylabel('Y')
#plt.show()
#
#
#
#ell_a = x[0]
#ell_b = x[1]
#ell_c = x[2]
#ell_d = x[3]
#ell_e = x[4]
#
#x_center = -ell_c/(2.0 * ell_a)
#y_center = -ell_d/(2.0 * ell_b)
#
#print(x_center)
#print(y_center)
#
#
#value = ell_a * (ell_c/(2*ell_a))**2 + ell_b * (ell_d/(2*ell_b))**2 - ell_e
#
#x_a = np.sqrt(value/ell_a)
#x_b = np.sqrt(value/ell_b)
#
#print(x_a)
#print(x_b)





N = 300
t = np.linspace(0, 2*np.pi, N)
x = 5*np.cos(t) + 0.2*np.random.normal(size=N) + 1
y = 4*np.sin(t+0.5) + 0.2*np.random.normal(size=N)
plt.plot(x, y, '.')     # given points

#xmean, ymean = x.mean(), y.mean()
#x -= xmean
#y -= ymean
#U, S, V = np.linalg.svd(np.stack((x, y)))
#
#tt = np.linspace(0, 2*np.pi, 1000)
#circle = np.stack((np.cos(tt), np.sin(tt)))    # unit circle
#transform = np.sqrt(2/N) * U.dot(np.diag(S))   # transformation matrix
#fit = transform.dot(circle) + np.array([[xmean], [ymean]])
#plt.plot(fit[0, :], fit[1, :], 'r')
#plt.show()