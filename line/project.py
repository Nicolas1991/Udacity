from copy import deepcopy

I = [[1, 2, 3, 4],
     [2, 3, 4, 5],
     [3, 4, 5, 6],
     [4, 5, 6, 7]]


def shape(M):
    return len(M[0]), len(M)


def matxRound(M, decPts=4):
    i = 0
    while i < len(M):
        j = 0
        while j < len(M[i]):
            M[i][j] = round(M[i][j], decPts)
            j += 1
        i += 1
    return M


# TODO 计算矩阵的转置
def transpose(M):
    M1 = deepcopy(M)
    i = 0
    while i < len(M):
        j = 0
        while j < len(M[i]):
            M1[j][i] = M[i][j]
            j += 1
        i += 1
    M = M1
    return M

# TODO 计算矩阵乘法 AB，如果无法相乘则raise ValueError
# def matxMultiply(A, B):
#     try:
#         if not len(A) == len(B[0]):
#             raise ValueError
#         C = []
#         for i in A:
#             for j in B:
#
#
#     except Exception:
#         raise ValueError