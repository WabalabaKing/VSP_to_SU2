# -*- coding: utf-8 -*-
"""
Created on Thu May 22 23:16:27 2025

@author: wz10
"""

import gmsh
import os

def stl_to_su2(stl_path, su2_output_path):
    gmsh.initialize()
    
    # Step 1: Load STL
    gmsh.merge(stl_path)

    # Step 2: Classify and build geometry
    # Step 3: Create surface loop and volume
    surface_entities = gmsh.model.getEntities(2)
    surface_tags = [tag for (dim, tag) in surface_entities]
    sL = gmsh.model.geo.addSurfaceLoop(surface_tags, -1)
    print(sL)
    gmsh.model.geo.addVolume([sL])
    gmsh.model.geo.synchronize()
    with open("boundary_marker.txt", "w") as f:
    # Step 4: Assign physical names using STL names
        cleannameL = {}
        for (dim, tag) in surface_entities:
            name = gmsh.model.getEntityName(dim, tag)
            if name:
                cleanname = name.split("_S_Surf")[0].strip()
                if cleanname not in list(cleannameL.keys()):
                    cleannameL.update({cleanname:[tag]})
                    print(list(cleannameL.keys()))
                elif cleanname in list(cleannameL.keys()):
                    tag_old = cleannameL[cleanname]
                    tag_old.append(tag)
                    cleannameL[cleanname]=tag_old
        
        for name in list(cleannameL.keys()):
            print(cleannameL[name])
            print(name)
            pg = gmsh.model.addPhysicalGroup(2, cleannameL[name])
            gmsh.model.setPhysicalName(2, pg, name)
            f.write(f"Assigned Physical Surface '{name}' to tag {str(cleannameL[name])}\n")
        

    # Step 5: Assign physical volume
    gmsh.model.addPhysicalGroup(3, [1], 1)
    gmsh.model.setPhysicalName(3, 1, "fluid")

    # Step 6: Generate mesh and write .su2
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.optimize("Netgen")
    print("Mesh optimized using Netgen.")
    gmsh.write(su2_output_path)
    print(f"SU2 mesh written to: {su2_output_path}")

    gmsh.finalize()