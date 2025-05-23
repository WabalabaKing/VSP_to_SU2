# -*- coding: utf-8 -*-
"""
Created on Thu May 22 21:16:23 2025

@author: wz10
"""
import os
def write_blockMeshDict(farfield, nx=20, ny=10, nz=20, filename="blockMeshDict"):
    os.chdir("system")
    halfY = farfield / 2
    verts = [
        [-farfield, 0,       -farfield],  # 0
        [ farfield, 0,       -farfield],  # 1
        [ farfield, halfY,   -farfield],  # 2
        [-farfield, halfY,   -farfield],  # 3
        [-farfield, 0,        farfield],  # 4
        [ farfield, 0,        farfield],  # 5
        [ farfield, halfY,    farfield],  # 6
        [-farfield, halfY,    farfield],  # 7
    ]

    block = "hex (0 1 2 3 4 5 6 7) (%d %d %d) simpleGrading (1 1 1)" % (nx, ny, nz)

    boundary_patches = f"""
boundary
(
    sym
    {{
        type symmetryPlane;
        faces
        (
            (0 1 4 5)
        );
    }}

    farfield
    {{
        type patch;
        faces
        (
            (2 3 7 6)  // y = farfield/2
            (0 3 7 4)  // -x side
            (1 5 6 2)  // +x side
            (0 1 2 3)  // -z side
            (4 5 6 7)  // +z side
        );
    }}
);
"""

    with open(filename, 'w') as f:
        f.write("FoamFile\n{\n    version 2.0;\n    format ascii;\n    class dictionary;\n    object blockMeshDict;\n}\n\n")
        f.write("scale 1.0;\n\n")
        f.write("vertices\n(\n")
        for v in verts:
            f.write("    (%.6f %.6f %.6f)\n" % tuple(v))
        f.write(");\n\n")

        f.write("blocks\n(\n    %s\n);\n\n" % block)

        f.write("edges\n(\n);\n\n")
        f.write(boundary_patches)
        f.write("\nmergePatchPairs\n(\n);\n")

    print(f"blockMeshDict written to {filename}")
