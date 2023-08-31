import numpy as np
cimport cython


cdef int[::1] VDIRS = np.array(
    (
         1,  0,
         0,  1,
        -1,  1,
        -1,  0,
         0, -1,
         1, -1, 
    ),
    dtype=np.dtype('i')
)
    

#@cython.boundscheck(False)
#@cython.wraparound(False)
def fill_sinks(
    double[:, ::1] vZ0, int[:, ::1] vedges,
    double inf, int eps
):
    # Determine matrix shape
    cdef Py_ssize_t qs = vZ0.shape[0]
    cdef Py_ssize_t rs = vZ0.shape[1]
    cdef Py_ssize_t qi, ri
    
    # Check input memory view shapes
    assert vedges.shape[0] == qs
    assert vedges.shape[1] == rs
     
    # Step 1: fill with water
    Zf = np.ndarray((qs, rs))
    cdef double[:, ::1] vZf = Zf
    for qi in range(qs):
        for ri in range(rs):
            vZf[qi, ri] = vZ0[qi, ri] if vedges[qi, ri] else inf

    # Step 2: remove excess
    cdef cython.bint proceed = 1
    cdef double alt
    cdef int qn, rn
    cdef Py_ssize_t di
    while proceed:
        proceed = 0
        for qi in range(qs):
            for ri in range(rs):
                if vedges[qi, ri] or vZf[qi, ri] == vZ0[qi, ri]:
                    continue
                for di in range(6):
                    qn = qi + VDIRS[2 * di]
                    rn = ri + VDIRS[2 * di + 1]
                    if not (0 <= qn < qs and 0 <= rn < rs):
                        continue
                    if np.isnan(vZf[qn, rn]):
                        continue
                    alt = vZf[qn, rn] + eps
                    if vZ0[qi, ri] >= alt:
                        vZf[qi, ri] = vZ0[qi, ri]
                        proceed = True
                        break
                    elif vZf[qi, ri] > alt and alt > vZ0[qi, ri]:
                        vZf[qi, ri] = alt
                        proceed = True
    return Zf
