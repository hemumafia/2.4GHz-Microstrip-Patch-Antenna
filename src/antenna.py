import os
import numpy as np

from CSXCAD import ContinuousStructure
import openEMS


# ============================================================
# 1. SIMULATION FOLDER
# ============================================================

sim_path = os.path.abspath("simulation")

print("Simulation folder:")
print(sim_path)


# ============================================================
# 2. ANTENNA PARAMETERS
# ============================================================

CSX = ContinuousStructure()

frequency = 2.4e9
epsilon_r = 4.3

# ------------------------------------------------------------
# Substrate
# ------------------------------------------------------------

substrate_width = 58.0
substrate_length = 65.0
substrate_height = 1.6

# ------------------------------------------------------------
# Patch
# ------------------------------------------------------------

patch_width = 38.37
patch_length = 28.95

# ------------------------------------------------------------
# Feed
# ------------------------------------------------------------

feed_width = 2.0
feed_length = 10.0

# ------------------------------------------------------------
# Inset
# ------------------------------------------------------------

inset_depth = 8.0
inset_gap = 1.0

notch_half_width = (
    feed_width / 2 + inset_gap
)


# ============================================================
# 3. CALCULATE POSITIONS
# ============================================================

patch_y_start = -patch_length / 2
patch_y_end = patch_length / 2

feed_y_start = (
    patch_y_start - feed_length
)

inset_y = (
    patch_y_start + inset_depth
)


print("Antenna geometry parameters loaded.")

print(f"Patch width  : {patch_width} mm")
print(f"Patch length : {patch_length} mm")
print(f"Feed width   : {feed_width} mm")
print(f"Feed length  : {feed_length} mm")
print(f"Inset depth  : {inset_depth} mm")


# ============================================================
# 4. CREATE FR-4 SUBSTRATE
# ============================================================

substrate = CSX.AddMaterial(
    'FR4',
    epsilon=epsilon_r
)

substrate.AddBox(
    start=[
        -substrate_width / 2,
        -substrate_length / 2,
        0
    ],
    stop=[
        substrate_width / 2,
        substrate_length / 2,
        substrate_height
    ]
)

print("Substrate created.")


# ============================================================
# 5. CREATE GROUND PLANE
# ============================================================

ground = CSX.AddMetal('Ground')

ground.AddBox(
    start=[
        -substrate_width / 2,
        -substrate_length / 2,
        0
    ],
    stop=[
        substrate_width / 2,
        substrate_length / 2,
        0
    ],
    priority=10
)

print("Zero-thickness ground plane created.")


# ============================================================
# 6. CREATE PATCH WITH 8-MM INSET
# ============================================================

patch = CSX.AddMetal('Patch')


# ------------------------------------------------------------
# Left side of patch
# ------------------------------------------------------------

patch.AddBox(
    [
        -patch_width / 2,
        patch_y_start,
        substrate_height
    ],
    [
        -notch_half_width,
        inset_y,
        substrate_height
    ],
    priority=10
)


# ------------------------------------------------------------
# Right side of patch
# ------------------------------------------------------------

patch.AddBox(
    [
        notch_half_width,
        patch_y_start,
        substrate_height
    ],
    [
        patch_width / 2,
        inset_y,
        substrate_height
    ],
    priority=10
)


# ------------------------------------------------------------
# Back/main portion of patch
# ------------------------------------------------------------

patch.AddBox(
    [
        -patch_width / 2,
        inset_y,
        substrate_height
    ],
    [
        patch_width / 2,
        patch_y_end,
        substrate_height
    ],
    priority=10
)

print("8-mm inset patch created.")


# ============================================================
# 7. CREATE MICROSTRIP FEED
# ============================================================

feed = CSX.AddMetal('Feed')

feed.AddBox(
    [
        -feed_width / 2,
        feed_y_start,
        substrate_height
    ],
    [
        feed_width / 2,
        inset_y,
        substrate_height
    ],
    priority=10
)

print("Microstrip feed created.")


# ============================================================
# 8. CREATE FDTD SOLVER
# ============================================================

FDTD = openEMS.openEMS()

FDTD.SetCSX(CSX)

print("FDTD solver created and connected to CSX.")


# ============================================================
# 9. CREATE 50-OHM LUMPED PORT
# ============================================================

port = FDTD.AddLumpedPort(
    1,
    50,
    [
        -feed_width / 2,
        feed_y_start,
        0
    ],
    [
        feed_width / 2,
        feed_y_start,
        substrate_height
    ],
    'z',
    1,
    priority=5,
    edges2grid='xy'
)

print("50-ohm lumped port created.")


# ============================================================
# 10. SIMULATION DOMAIN
# ============================================================

simbox_x = 160.0
simbox_y = 170.0
simbox_z = 120.0


# ============================================================
# 11. CREATE INITIAL MESH
# ============================================================

mesh = CSX.GetGrid()

mesh.SetDeltaUnit(1e-3)


# ------------------------------------------------------------
# Simulation box
# ------------------------------------------------------------

mesh.AddLine(
    'x',
    [
        -simbox_x / 2,
        simbox_x / 2
    ]
)

mesh.AddLine(
    'y',
    [
        -simbox_y / 2,
        simbox_y / 2
    ]
)

mesh.AddLine(
    'z',
    [
        -simbox_z / 2,
        simbox_z / 2
    ]
)


# ------------------------------------------------------------
# Important antenna mesh lines
# ------------------------------------------------------------

mesh.AddLine(
    'x',
    [
        -substrate_width / 2,
        -patch_width / 2,
        -notch_half_width,
        -feed_width / 2,
        0,
        feed_width / 2,
        notch_half_width,
        patch_width / 2,
        substrate_width / 2
    ]
)


mesh.AddLine(
    'y',
    [
        -substrate_length / 2,
        feed_y_start,
        patch_y_start,
        inset_y,
        0,
        patch_y_end,
        substrate_length / 2
    ]
)


# ------------------------------------------------------------
# Substrate thickness mesh
# ------------------------------------------------------------

mesh.AddLine(
    'z',
    [
        0,
        0.4,
        0.8,
        1.2,
        substrate_height
    ]
)

print("Initial mesh created.")


# ============================================================
# 12. ALIGN METAL EDGES TO MESH
# ============================================================

FDTD.AddEdges2Grid(
    dirs='xy',
    properties=patch,
    metal_edge_res=1.0
)

FDTD.AddEdges2Grid(
    dirs='xy',
    properties=ground
)

FDTD.AddEdges2Grid(
    dirs='xy',
    properties=feed,
    metal_edge_res=1.0
)

print("Metal edges aligned with FDTD mesh.")


# ============================================================
# 13. SMOOTH THE MESH
# ============================================================

mesh_res = 2.0

mesh.SmoothMeshLines(
    'all',
    mesh_res,
    1.4
)

print("Mesh finalized.")


# ============================================================
# 14. EXCITATION
# ============================================================

FDTD.SetGaussExcite(
    frequency,
    1.0e9
)


# ============================================================
# 15. BOUNDARY CONDITIONS
# ============================================================

FDTD.SetBoundaryCond(
    [
        'PML_8',
        'PML_8',
        'PML_8',
        'PML_8',
        'PML_8',
        'PML_8'
    ]
)

print("Simulation boundaries created.")


# ============================================================
# 16. NF2FF RECORDING BOX
# ============================================================
#
# IMPORTANT:
# This MUST be created before FDTD.Run().
#
# It records the electromagnetic fields around the antenna.
# analyze.py later converts these near fields into far fields.
#
# ============================================================

nf2ff = FDTD.CreateNF2FFBox()

print("NF2FF recording box created.")


# ============================================================
# 17. SIMULATION TIME
# ============================================================

FDTD.SetNumberOfTimeSteps(30000)

FDTD.SetEndCriteria(1e-4)

print("Simulation time configured.")


# ============================================================
# 18. CREATE SIMULATION DIRECTORY
# ============================================================

if not os.path.exists(sim_path):
    os.makedirs(sim_path)


# ============================================================
# 19. SAVE ANTENNA GEOMETRY
# ============================================================

xml_path = os.path.join(
    sim_path,
    "antenna.xml"
)

CSX.Write2XML(xml_path)

print("Antenna geometry saved to:")
print(xml_path)


# ============================================================
# 20. RUN ELECTROMAGNETIC SIMULATION
# ============================================================

print()
print("==============================================")
print("Starting electromagnetic simulation...")
print("NF2FF field recording is ENABLED.")
print("This may take several minutes.")
print("==============================================")
print()


FDTD.Run(
    sim_path,
    verbose=3
)


print()
print("==============================================")
print("Electromagnetic simulation completed.")
print("NF2FF field data has been recorded.")
print("==============================================")