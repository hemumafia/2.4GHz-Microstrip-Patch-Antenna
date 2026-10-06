import os
import numpy as np
import matplotlib.pyplot as plt

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

substrate_width = 58.0
substrate_length = 65.0
substrate_height = 1.6

patch_width = 38.37
patch_length = 28.95

feed_width = 2.0
feed_length = 10.0

inset_depth = 8.0
inset_gap = 1.0

notch_half_width = (
    feed_width / 2 +
    inset_gap
)


# ============================================================
# 3. CALCULATE POSITIONS
# ============================================================

patch_y_start = -patch_length / 2
patch_y_end = patch_length / 2

feed_y_start = (
    patch_y_start -
    feed_length
)

inset_y = (
    patch_y_start +
    inset_depth
)


print()
print("Antenna parameters loaded.")
print(f"Patch width  : {patch_width} mm")
print(f"Patch length : {patch_length} mm")
print(f"Feed width   : {feed_width} mm")
print(f"Feed length  : {feed_length} mm")
print(f"Inset depth  : {inset_depth} mm")


# ============================================================
# 4. CREATE SUBSTRATE
# ============================================================

substrate = CSX.AddMaterial('FR4', epsilon=epsilon_r)

substrate.AddBox(
    start=[-substrate_width / 2, -substrate_length / 2, 0],
    stop=[substrate_width / 2, substrate_length / 2, substrate_height]
)


# ============================================================
# 5. CREATE GROUND
# ============================================================

ground = CSX.AddMetal('Ground')

ground.AddBox(
    start=[-substrate_width / 2, -substrate_length / 2, 0],
    stop=[substrate_width / 2, substrate_length / 2, 0],
    priority=10
)


# ============================================================
# 6. RECREATE PATCH
# ============================================================

patch = CSX.AddMetal('Patch')

patch.AddBox(
    [-patch_width / 2, patch_y_start, substrate_height],
    [-notch_half_width, inset_y, substrate_height],
    priority=10
)

patch.AddBox(
    [notch_half_width, patch_y_start, substrate_height],
    [patch_width / 2, inset_y, substrate_height],
    priority=10
)

patch.AddBox(
    [-patch_width / 2, inset_y, substrate_height],
    [patch_width / 2, patch_y_end, substrate_height],
    priority=10
)


# ============================================================
# 7. RECREATE FEED
# ============================================================

feed = CSX.AddMetal('Feed')

feed.AddBox(
    [-feed_width / 2, feed_y_start, substrate_height],
    [feed_width / 2, inset_y, substrate_height],
    priority=10
)


# ============================================================
# 8. CREATE FDTD
# ============================================================

FDTD = openEMS.openEMS()
FDTD.SetCSX(CSX)

print()
print("CSX structure connected to FDTD.")


# ============================================================
# 9. RECREATE 50-OHM PORT
# ============================================================

port = FDTD.AddLumpedPort(
    1, 50,
    [-feed_width / 2, feed_y_start, 0],
    [feed_width / 2, feed_y_start, substrate_height],
    'z', 1,
    priority=5,
    edges2grid='xy'
)

print("50-ohm lumped port recreated.")


# ============================================================
# 10. RECREATE MESH
# ============================================================

simbox_x = 160.0
simbox_y = 170.0
simbox_z = 120.0

mesh = CSX.GetGrid()
mesh.SetDeltaUnit(1e-3)

mesh.AddLine('x', [-simbox_x / 2, simbox_x / 2])
mesh.AddLine('y', [-simbox_y / 2, simbox_y / 2])
mesh.AddLine('z', [-simbox_z / 2, simbox_z / 2])

mesh.AddLine('x', [
    -substrate_width / 2, -patch_width / 2, -notch_half_width,
    -feed_width / 2, 0, feed_width / 2, notch_half_width,
    patch_width / 2, substrate_width / 2
])

mesh.AddLine('y', [
    -substrate_length / 2, feed_y_start, patch_y_start,
    inset_y, 0, patch_y_end, substrate_length / 2
])

mesh.AddLine('z', [0, 0.4, 0.8, 1.2, substrate_height])

FDTD.AddEdges2Grid(dirs='xy', properties=patch, metal_edge_res=1.0)
FDTD.AddEdges2Grid(dirs='xy', properties=ground)
FDTD.AddEdges2Grid(dirs='xy', properties=feed, metal_edge_res=1.0)

mesh_res = 2.0
mesh.SmoothMeshLines('all', mesh_res, 1.4)


# ============================================================
# 11. BOUNDARY CONDITIONS
# ============================================================

FDTD.SetBoundaryCond([
    'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8'
])


# ============================================================
# 12. RECREATE NF2FF BOX
# ============================================================

nf2ff = FDTD.CreateNF2FFBox()

print("NF2FF box recreated.")


# ============================================================
# 13. FREQUENCY RANGE
# ============================================================

f = np.linspace(1.4e9, 3.4e9, 401)


# ============================================================
# 14. READ EXISTING PORT DATA
# ============================================================

print()
print("Reading existing simulation results...")

port.CalcPort(sim_path, f)

print("Port data calculated.")


# ============================================================
# 15. S11
# ============================================================

s11 = port.uf_ref / port.uf_inc
s11_magnitude = np.abs(s11)
s11_dB = 20.0 * np.log10(s11_magnitude)


# ============================================================
# 16. VSWR
# ============================================================

gamma = np.minimum(s11_magnitude, 0.999999)
vswr = (1.0 + gamma) / (1.0 - gamma)


# ============================================================
# 17. FIND RESONANCE
# ============================================================

min_index = np.argmin(s11_dB)
resonant_frequency = f[min_index]
minimum_s11 = s11_dB[min_index]
resonant_vswr = vswr[min_index]


# ============================================================
# 17b. IMPEDANCE BANDWIDTH (-10 dB and VSWR <= 2)
# ============================================================

def find_band_edges(x, y, threshold, center_index, below=True):
    """
    Walk outward from center_index in both directions and find
    where y crosses `threshold`. `below=True` means the passband
    is where y < threshold (used for S11 dB); `below=False` means
    the passband is where y < threshold on a non-dB metric like VSWR
    (VSWR <= 2 is still 'below', so below=True works for both here).
    """
    # Walk left
    left_index = center_index
    while left_index > 0 and y[left_index] < threshold:
        left_index -= 1
    if left_index == center_index:
        left_edge = x[center_index]
    else:
        left_edge = np.interp(
            threshold,
            [y[left_index], y[left_index + 1]],
            [x[left_index], x[left_index + 1]]
        )

    # Walk right
    right_index = center_index
    n = len(y)
    while right_index < n - 1 and y[right_index] < threshold:
        right_index += 1
    if right_index == center_index:
        right_edge = x[center_index]
    else:
        right_edge = np.interp(
            threshold,
            [y[right_index - 1], y[right_index]],
            [x[right_index - 1], x[right_index]]
        )

    return left_edge, right_edge


# --- S11 <= -10 dB bandwidth ---
s11_low_f, s11_high_f = find_band_edges(
    f, s11_dB, -10.0, min_index
)
s11_bandwidth_hz = s11_high_f - s11_low_f
s11_bandwidth_pct = (s11_bandwidth_hz / resonant_frequency) * 100.0

# --- VSWR <= 2 bandwidth ---
vswr_low_f, vswr_high_f = find_band_edges(
    f, vswr, 2.0, min_index
)
vswr_bandwidth_hz = vswr_high_f - vswr_low_f
vswr_bandwidth_pct = (vswr_bandwidth_hz / resonant_frequency) * 100.0

print()
print("========================================")
print("          BANDWIDTH RESULTS")
print("========================================")
print(
    f"-10 dB band  : {s11_low_f/1e9:.4f} - {s11_high_f/1e9:.4f} GHz "
    f"({s11_bandwidth_hz/1e6:.2f} MHz, {s11_bandwidth_pct:.2f} %)"
)
print(
    f"VSWR<=2 band : {vswr_low_f/1e9:.4f} - {vswr_high_f/1e9:.4f} GHz "
    f"({vswr_bandwidth_hz/1e6:.2f} MHz, {vswr_bandwidth_pct:.2f} %)"
)
print("========================================")


# ============================================================
# 18. DISPLAY S11 RESULTS
# ============================================================

print()
print("========================================")
print("          ANTENNA RESULTS")
print("========================================")
print(f"Resonant frequency : {resonant_frequency / 1e9:.4f} GHz")
print(f"Minimum S11        : {minimum_s11:.2f} dB")
print(f"VSWR at resonance  : {resonant_vswr:.3f}")
print("========================================")


# ============================================================
# 19. S11 PLOT
# ============================================================

plt.figure(figsize=(10, 7))
plt.plot(f / 1e9, s11_dB, label='S11')
plt.axhline(-10, linestyle='--', label='-10 dB reference')
plt.scatter(resonant_frequency / 1e9, minimum_s11, label='Resonance')
plt.xlabel("Frequency (GHz)")
plt.ylabel("S11 (dB)")
plt.title("2.4 GHz Microstrip Patch Antenna - S11")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(sim_path, "S11_plot.png"), dpi=300)
plt.close()


# ============================================================
# 20. VSWR PLOT (cropped to the useful band)
# ============================================================

plt.figure(figsize=(10, 7))
plt.plot(f / 1e9, vswr, label='VSWR')
plt.axhline(2, linestyle='--', label='VSWR = 2 reference')
plt.scatter(resonant_frequency / 1e9, resonant_vswr, label='Resonance')
plt.xlabel("Frequency (GHz)")
plt.ylabel("VSWR")
plt.title("2.4 GHz Microstrip Patch Antenna - VSWR")
plt.xlim(2.2, 2.6)
plt.ylim(1, 5)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(sim_path, "VSWR_plot.png"), dpi=300)
plt.close()


# ============================================================
# 21. NF2FF ANGLE GRID
# ============================================================

print()
print("Preparing radiation-pattern calculation...")

theta = np.arange(0.0, 181.0, 2.0)
phi = np.arange(-180.0, 181.0, 2.0)


# ============================================================
# 22. CALCULATE FAR FIELD
# ============================================================

print("Calculating 3D far field...")

nf2ff_res = nf2ff.CalcNF2FF(
    sim_path,
    resonant_frequency,
    theta,
    phi,
    center=[0, 0, 0],
    read_cached=False,
    verbose=1
)

print("3D far-field calculation completed.")


# ============================================================
# 23. EXTRACT SCALAR NF2FF RESULTS
# ============================================================

directivity_linear = float(np.real(np.squeeze(nf2ff_res.Dmax)))
radiated_power = float(np.real(np.squeeze(nf2ff_res.Prad)))

print()
print("NF2FF physical check:")
print(f"Dmax linear       : {directivity_linear:.6e}")
print(f"Radiated power    : {radiated_power:.6e} W")

if not np.isfinite(directivity_linear):
    raise RuntimeError("NF2FF error: Dmax is NaN or infinite.")

if not np.isfinite(radiated_power):
    raise RuntimeError("NF2FF error: Prad is NaN or infinite.")

if directivity_linear <= 0:
    raise RuntimeError("NF2FF error: Dmax <= 0.")

if radiated_power <= 0:
    raise RuntimeError("NF2FF error: Prad <= 0 W.")


# ============================================================
# 24. DIRECTIVITY
# ============================================================

directivity_dBi = 10.0 * np.log10(directivity_linear)

print()
print("Directivity:")
print(f"Linear : {directivity_linear:.6f}")
print(f"dBi    : {directivity_dBi:.3f}")


# ============================================================
# 25. ACCEPTED INPUT POWER
# ============================================================

accepted_power = float(
    np.interp(resonant_frequency, f, np.real(port.P_acc))
)

print()
print("Accepted input power:")
print(f"{accepted_power:.6e} W")

if not np.isfinite(accepted_power):
    raise RuntimeError("Accepted power is NaN or infinite.")

if accepted_power <= 0:
    raise RuntimeError("Accepted power is <= 0 W.")


# ============================================================
# 26. RADIATION EFFICIENCY
# ============================================================

radiation_efficiency = radiated_power / accepted_power

print()
print("Radiation efficiency:")
print(f"{radiation_efficiency * 100:.3f} %")

if radiation_efficiency <= 0:
    raise RuntimeError("Radiation efficiency is <= 0.")

if radiation_efficiency > 1.0:
    print("WARNING: Radiation efficiency is greater than 100%.")


# ============================================================
# 27. GAIN
# ============================================================

gain_linear = directivity_linear * radiation_efficiency
gain_dBi = 10.0 * np.log10(gain_linear)


# ============================================================
# 28. DISPLAY FAR-FIELD RESULTS
# ============================================================

print()
print("========================================")
print("       FAR-FIELD ANTENNA RESULTS")
print("========================================")
print(f"Frequency           : {resonant_frequency / 1e9:.4f} GHz")
print(f"Radiated power      : {radiated_power:.6e} W")
print(f"Accepted power      : {accepted_power:.6e} W")
print(f"Radiation efficiency: {radiation_efficiency * 100:.2f} %")
print(f"Directivity         : {directivity_dBi:.2f} dBi")
print(f"Gain                : {gain_dBi:.2f} dBi")
print("========================================")


# ============================================================
# 29. FAR-FIELD DATA
# ============================================================

print()
print("Preparing radiation-pattern data...")

E_norm = np.squeeze(nf2ff_res.E_norm[0])
P_rad = np.squeeze(nf2ff_res.P_rad[0])

print("E_norm shape:", E_norm.shape)
print("P_rad shape :", P_rad.shape)
print("Expected shape:", (len(theta), len(phi)))

if E_norm.shape != (len(theta), len(phi)):
    raise RuntimeError("Unexpected E_norm shape.")

if P_rad.shape != (len(theta), len(phi)):
    raise RuntimeError("Unexpected P_rad shape.")

if not np.all(np.isfinite(E_norm)):
    raise RuntimeError("E_norm contains NaN or infinity.")

if not np.all(np.isfinite(P_rad)):
    raise RuntimeError("P_rad contains NaN or infinity.")

print("Far-field data ready.")


# ============================================================
# 30. TRUE DIRECTIVITY PATTERN (from P_rad, not E_norm)
# ============================================================

directivity_pattern_linear = (
    4.0 * np.pi * P_rad / radiated_power
)

directivity_pattern_linear = np.maximum(
    directivity_pattern_linear, 0.0
)

directivity_pattern_dBi = np.full_like(
    directivity_pattern_linear, -100.0
)

positive_mask = directivity_pattern_linear > 0

directivity_pattern_dBi[positive_mask] = (
    10.0 * np.log10(directivity_pattern_linear[positive_mask])
)

print("Directivity pattern calculated.")


# ============================================================
# 31. E-PLANE / H-PLANE CUTS
# ============================================================
#
# Patch: width -> X, length -> Y, broadside -> Z
# E-plane -> YZ -> phi = 90 deg
# H-plane -> XZ -> phi = 0 deg
#
# ============================================================

phi_e_index = np.argmin(np.abs(phi - 90.0))
phi_h_index = np.argmin(np.abs(phi - 0.0))

E_plane = directivity_pattern_dBi[:, phi_e_index]
H_plane = directivity_pattern_dBi[:, phi_h_index]

# ============================================================
# 31b. 3 dB BEAMWIDTH (E-plane and H-plane)
# ============================================================

def find_3dB_beamwidth(theta_deg, pattern_dB, peak_dB):
    """
    theta_deg starts at 0 (boresight) and increases.
    Finds the angle where pattern drops 3 dB below peak on the
    rising side of theta, then doubles it for full beamwidth
    (assumes a roughly symmetric main lobe about theta=0, valid
    here since boresight is the array's first sample).
    """
    target = peak_dB - 3.0

    # Walk outward from theta=0 until pattern drops below target
    idx = 0
    n = len(pattern_dB)
    while idx < n - 1 and pattern_dB[idx] > target:
        idx += 1

    if idx == 0:
        half_angle = theta_deg[0]
    else:
        half_angle = np.interp(
            target,
            [pattern_dB[idx], pattern_dB[idx - 1]],
            [theta_deg[idx], theta_deg[idx - 1]]
        )

    return 2.0 * half_angle


E_plane_peak = E_plane[0]
H_plane_peak = H_plane[0]

E_plane_beamwidth = find_3dB_beamwidth(theta, E_plane, E_plane_peak)
H_plane_beamwidth = find_3dB_beamwidth(theta, H_plane, H_plane_peak)

print()
print("========================================")
print("       3 dB BEAMWIDTH RESULTS")
print("========================================")
print(f"E-plane peak       : {E_plane_peak:.2f} dBi at theta=0")
print(f"H-plane peak       : {H_plane_peak:.2f} dBi at theta=0")
print(f"E-plane beamwidth  : {E_plane_beamwidth:.2f} degrees")
print(f"H-plane beamwidth  : {H_plane_beamwidth:.2f} degrees")
print("========================================")

print(f"E-plane extracted at phi = {phi[phi_e_index]:.1f} degrees")
print(f"H-plane extracted at phi = {phi[phi_h_index]:.1f} degrees")


# ============================================================
# 32. E-PLANE PLOT (linear, kept for reference)
# ============================================================

plt.figure(figsize=(10, 7))
plt.plot(theta, E_plane, label='E-plane (YZ)')
plt.xlabel("Theta (degrees)")
plt.ylabel("Directivity (dBi)")
plt.title("2.4 GHz Microstrip Patch Antenna - E-plane")
plt.ylim(-40, max(directivity_dBi + 2, 10))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(sim_path, "E_plane.png"), dpi=300)
plt.close()


# ============================================================
# 33. H-PLANE PLOT (linear, kept for reference)
# ============================================================

plt.figure(figsize=(10, 7))
plt.plot(theta, H_plane, label='H-plane (XZ)')
plt.xlabel("Theta (degrees)")
plt.ylabel("Directivity (dBi)")
plt.title("2.4 GHz Microstrip Patch Antenna - H-plane")
plt.ylim(-40, max(directivity_dBi + 2, 10))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(sim_path, "H_plane.png"), dpi=300)
plt.close()


# ============================================================
# 34. E-PLANE / H-PLANE POLAR PLOTS
#     (replaces the unreliable 3D Cartesian surface)
# ============================================================
#
# Full 0-360 degree cut built by mirroring theta 0-180 across
# phi and phi+180, which is the standard way to build a full
# polar antenna pattern from a half-plane NF2FF cut.
#
# ============================================================

# 3D pattern built from the P_rad-derived directivity (NOT E_norm)

THETA, PHI = np.meshgrid(
    np.deg2rad(theta),
    np.deg2rad(phi),
    indexing='ij'
)

floor_dB_3d = -20.0

pattern_3d = np.maximum(directivity_pattern_dBi, floor_dB_3d)

# radius = normalised, floor-shifted dB (standard for 3D pattern plots)
# radius = linear directivity, normalised (clear lobe shape for report figures)
R = directivity_pattern_linear / np.max(directivity_pattern_linear)

X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(
    X, Y, Z,
    facecolors=plt.cm.viridis(
        (pattern_3d - floor_dB_3d) / (np.max(pattern_3d) - floor_dB_3d)
    ),
    linewidth=0,
    antialiased=True,
    shade=False
)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title(
    "2.4 GHz Microstrip Patch Antenna\n"
    "3D Radiation Pattern (directivity, -20 dB floor)"
)
ax.set_box_aspect([1, 1, 1])

plt.tight_layout()
plt.savefig(os.path.join(sim_path, "Radiation_3D.png"), dpi=300)
plt.close()

print("3D radiation pattern generated.")

results_file = os.path.join(sim_path, "far_field_results.txt")

with open(results_file, "w") as file:
    file.write("2.4 GHz Microstrip Patch Antenna\n")
    file.write("================================\n")
    file.write(f"Resonant frequency : {resonant_frequency / 1e9:.6f} GHz\n")
    file.write(f"Minimum S11        : {minimum_s11:.4f} dB\n")
    file.write(f"VSWR               : {resonant_vswr:.4f}\n")
    file.write(f"Radiated power     : {radiated_power:.8e} W\n")
    file.write(f"Accepted power     : {accepted_power:.8e} W\n")
    file.write(f"Radiation efficiency: {radiation_efficiency * 100:.4f} %\n")
    file.write(f"Directivity        : {directivity_dBi:.4f} dBi\n")
    file.write(f"Gain               : {gain_dBi:.4f} dBi\n")
    file.write(f"-10 dB bandwidth   : {s11_bandwidth_hz/1e6:.2f} MHz ({s11_bandwidth_pct:.2f} %)\n")
    file.write(f"VSWR<=2 bandwidth  : {vswr_bandwidth_hz/1e6:.2f} MHz ({vswr_bandwidth_pct:.2f} %)\n")
    file.write(f"E-plane beamwidth  : {E_plane_beamwidth:.2f} degrees\n")
    file.write(f"H-plane beamwidth  : {H_plane_beamwidth:.2f} degrees\n")

# ============================================================
# 36. FINISHED
# ============================================================

print()
print("========================================")
print("Radiation analysis completed.")
print("========================================")

print()
print("Generated files:")
print(os.path.join(sim_path, "S11_plot.png"))
print(os.path.join(sim_path, "VSWR_plot.png"))
print(os.path.join(sim_path, "E_plane.png"))
print(os.path.join(sim_path, "H_plane.png"))
print(os.path.join(sim_path, "E_plane_polar.png"))
print(os.path.join(sim_path, "H_plane_polar.png"))
print(os.path.join(sim_path, "far_field_results.txt"))