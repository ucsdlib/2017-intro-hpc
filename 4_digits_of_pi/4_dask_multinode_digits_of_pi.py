#!/usr/bin/env python3
import sys
import numpy as np
import dask.array as da

np.random.seed(2017)

def inside_circle(total_count):

    x = da.random.uniform(size=total_count, chunks=100000)
    y = da.random.uniform(size=total_count, chunks=100000)

    radii_square = x**2 + y**2

    count = (radii_square<=1.0).sum().compute()

    return count

def estimate_pi(n_samples):

    return (4.0 * inside_circle(n_samples) / n_samples)

if __name__=='__main__':

    n_samples = 10000
    if len(sys.argv) > 1:
        n_samples = int(sys.argv[1])

    from distributed import Client
    client = Client('127.0.0.1:8786')

    my_pi = estimate_pi(n_samples)
    sizeof = np.dtype(np.float64).itemsize

    print("[dask version] pi is {} from {} samples".format(my_pi,n_samples))
    print("[dask version] got {} digits right".format(int(np.ceil(-np.log10(abs(my_pi - np.pi))))))
