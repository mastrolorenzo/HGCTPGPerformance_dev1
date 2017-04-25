#!/usr/bin/python
# test of a python analyzer that produce response plots #
# Luca Mastrolorenzo - 25-04-2017 #
# The class provide a function that create an output file and store pt,eta,phi response#

import sys
import os
import ROOT
from ROOT import std
from math import *

class resolution :
    
    def __init__(self,input_file) :
        self.inputNtuple = ROOT.TFile.Open(input_file)
        self.chain = self.inputNtuple.Get("hgcalTriggerNtuplizer/HGCalTriggerNtuple")
    
    def deltaPhi( self, phi1, phi2) :    
        dPhi = phi1-phi2
        pi = acos(-1.0)
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
        return sqrt(dEta*dEta+dPhi*dPhi)

    def plotResponse(self) :
        output = ROOT.TFile("./response_highStat.root","RECREATE")
        h_resoPt = ROOT.TH1D("resoPt","Pt response",100, 0, 2)
        h_resoEta = ROOT.TH1D("resoEta","Eta response",100, -0.15, 0.15);
        h_resoPhi = ROOT.TH1D("resoPhi","Phi response",100, -0.15, 0.15);
        h_L1PtvsTrue2D = ROOT.TH2D("h_L1PtvsTrue2D","h_L1PtvsTrue2D",200, 0, 200, 201, -1, 200);

        self.chain.Print()
        dr = self.deltaR(1,-1,2,-2.3)
        print dr
        
        gen_pt_ = std.vector(float)()
        gen_eta_ = std.vector(float)()
        gen_phi_ = std.vector(float)()
        gen_energy_ = std.vector(float)()
        gen_status_ = std.vector(int)()
        gen_id_ = std.vector(int)()        
        c3d_pt_ = std.vector(float)()
        c3d_eta_ = std.vector(float)()
        c3d_phi_ = std.vector(float)()
        c3d_energy_ = std.vector(float)()
        
        self.chain.SetBranchAddress("gen_pt",gen_pt_);
        self.chain.SetBranchAddress("gen_eta",gen_eta_);
        self.chain.SetBranchAddress("gen_phi",gen_phi_);
        self.chain.SetBranchAddress("gen_energy",gen_energy_);
        self.chain.SetBranchAddress("gen_status",gen_status_);
        self.chain.SetBranchAddress("gen_id",gen_id_);
        self.chain.SetBranchAddress("cl3d_pt",c3d_pt_);
        self.chain.SetBranchAddress("cl3d_eta",c3d_eta_);
        self.chain.SetBranchAddress("cl3d_phi",c3d_phi_);
        self.chain.SetBranchAddress("cl3d_energy",c3d_energy_);

        # loop over the ttree ntries
        for i in range( self.chain.GetEntries() ) :
            self.chain.GetEntry( i )

            # loop over the gen particle and apply basic selection at MC-truth level
            for i_gen in range(gen_pt_.size()) :
                if ( abs( gen_eta_.at(i_gen) ) > 1.47 and abs( gen_eta_.at(i_gen) ) < 3.0 
                     and gen_pt_.at(i_gen) > 7 and abs( gen_id_.at(i_gen) ) == 22 
                     and gen_status_.at(i_gen) == 1 ) :
                    
                    hasMatched = False
                    pt_cand = -1.
                    eta_cand = -100.
                    phi_cand = -100.

                    # loop over the 3D-cluster
                    for i_c3d in range(c3d_pt_.size()) :
                        if ( abs( c3d_eta_.at(i_c3d) ) > 1.47 and  abs( c3d_eta_.at(i_c3d) ) < 3.0 
                             and c3d_pt_.at(i_c3d)>7 ) :
                            
                            dR = self.deltaR( gen_eta_.at(i_gen), c3d_eta_.at(i_c3d), gen_phi_.at(i_gen), c3d_phi_.at(i_c3d))                
                            if dR<0.5 :
                                hasMatched = True
                                if c3d_pt_.at(i_c3d) > pt_cand :
                                    pt_cand = c3d_pt_.at(i_c3d)
                                    eta_cand = c3d_eta_.at(i_c3d)
                                    phi_cand = c3d_phi_.at(i_c3d)                                                      
                    if hasMatched : 
                        print gen_pt_.at(i_gen), pt_cand
                        h_L1PtvsTrue2D.Fill(gen_pt_.at(i_gen), pt_cand)
                    elif not hasMatched :
                        print gen_pt_.at(i_gen), -1
                        h_L1PtvsTrue2D.Fill(gen_pt_.at(i_gen), -1)
                    h_resoPt.Fill( pt_cand / gen_pt_.at(i_gen) )
                    h_resoEta.Fill( eta_cand - gen_eta_.at(i_gen) )
                    h_resoPhi.Fill( phi_cand - gen_phi_.at(i_gen) )

        # write histograms into output file
        h_resoPt.Write()
        h_resoEta.Write()
        h_resoPhi.Write()
        h_L1PtvsTrue2D.Write()
