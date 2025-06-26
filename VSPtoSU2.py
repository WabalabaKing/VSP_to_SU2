
import os
import numpy as np
import subprocess
import run_cfd_mesh as R
import STL_Gmesh as G
#sysdir = "c:/users/wz10/desktop/vsp_su2/system"
#Run VSP API for aircraft half mesh    
vsp_loc = "Example"
os.chdir(vsp_loc)
R.run_cfd_mesh("TestAircraft.vsp3", 0.02,0.2, sym=True,farfield_scale=50.0,farfield=True)


#Gmesh subroutine, it is only good for Euler
#G.stl_to_su2("TestAircraft.stl", "TestAircraft.su2")
