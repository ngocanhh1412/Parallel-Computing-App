import numpy as np
from numba import cuda
import cupy as cp
# CUDA kernel for vector-matrix multiplication
@cuda.jit
def vecmatmul_kernel(vec, mat, result):
    col = cuda.grid(1)
    if col < result.shape[1]:
        tmp = 0
        for k in range(vec.shape[0]):
            tmp += vec[k] * mat[k, col]
        result[0, col] = tmp

# Function to perform vector-matrix multiplication using CUDA
def vecmatmul_cuda(vec, mat):
    rows_vec = 1
    cols_vec = vec.shape[0]
    rows_mat, cols_mat = mat.shape

    if cols_vec != rows_mat:
        raise ValueError("Vector and matrix dimensions do not match for multiplication")

    vec_global = cuda.to_device(vec)
    mat_global = cuda.to_device(mat)
    result_global = cuda.device_array((1, cols_mat))

    # Define the grid and block dimensions
    threads_per_block = 512
    blocks_per_grid = (cols_mat + threads_per_block - 1) // threads_per_block

    # Call the CUDA kernel
    vecmatmul_kernel[blocks_per_grid, threads_per_block](vec_global, mat_global, result_global)

    # Copy the result back to the host
    result = result_global.copy_to_host()

    return result