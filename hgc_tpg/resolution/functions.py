#!/usr/bin/python

import ROOT
from ROOT import std
import math as m 

class functions :
    
    def __init__(self) :
        pass

    def deltaPhi( self, phi1, phi2) :    
        dPhi = phi1-phi2
        pi = m.acos(-1.0)
        if dPhi <= -pi : 
            dPhi += 2.0*pi
        elif dPhi > pi : 
            dPhi-=2.0*pi;           
        return dPhi

    def deltaEta(self, eta1, eta2) :
        dEta = eta1-eta2
        return dEta

    def deltaR(self, eta1, eta2, phi1, phi2) :
        dEta = self.deltaEta(eta1, eta2)
        dPhi = self.deltaPhi(phi1, phi2)
        return m.sqrt(dEta*dEta+dPhi*dPhi)
