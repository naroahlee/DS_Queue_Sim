def P2R(radii, angles):
    return radii * exp(1j*angles)

def R2P(x):
    return abs(x), angle(x)
