# -*- coding: utf-8 -*-
"""
Created on Thu May 22 21:16:55 2025

@author: wz10
"""
import openvsp as vsp
import fileinput
def run_cfd_mesh(vsp_file, minedge,maxedge, sym=False, 
                 farfield_scale= 2.0, farfield= False):
    if sym:
        f = fileinput.input(vsp_file,inplace=1)
        for line in f:
            if 'SymmetrySplitting' in line:
                print(line[0:34] + '1' + line[35:-1])
            else:
                print(line)
    vsp.ClearVSPModel()
    vsp.ReadVSPFile(vsp_file)
    vsp.SetCFDMeshVal(vsp.CFD_MIN_EDGE_LEN, minedge )
    vsp.SetCFDMeshVal( vsp.CFD_MAX_EDGE_LEN, maxedge)
    vsp.SetCFDMeshVal( vsp.CFD_GROWTH_RATIO , 1.2 )
    vsp.SetCFDMeshVal( vsp.CFD_HALF_MESH_FLAG , sym)
    vsp.SetCFDMeshVal( vsp.CFD_FAR_FIELD_FLAG  , farfield)
    if farfield:
        vsp.SetCFDMeshVal( vsp.CFD_FAR_MAX_EDGE_LEN , 20)
        vsp.SetCFDMeshVal( vsp.CFD_FAR_X_SCALE  , farfield_scale)
        vsp.SetCFDMeshVal( vsp.CFD_FAR_Y_SCALE  , farfield_scale)
        vsp.SetCFDMeshVal( vsp.CFD_FAR_Z_SCALE  , 5*farfield_scale)
        
    vsp.SetCFDMeshVal( vsp.CFD_INTERSECT_SUBSURFACE_FLAG , True)
    vsp.SetComputationFileName(vsp.CFD_STL_FILE_NAME ,vsp_file)
    vsp.ComputeCFDMesh(vsp.SET_ALL,vsp.SET_NONE,vsp.CFD_STL_TYPE)
    