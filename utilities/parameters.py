

class parameters : 
    
    def __init__(self) :
        pass

    #define acceptance of the reconstructed clusters
    minEta_C3d = float(1.47)
    maxEta_C3d = float(3.0)
    minPt_C3d = float(7.0) # in GeV

    #define acceptance, type and status of the gen-particle
    minEta_gen = float(1.47)
    maxEta_gen = float(3.0)
    minPt_gen = float(7.0) # in GeV
    particle_type = int(22)
    particle_status = int(1)
