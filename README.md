# 2.4 GHz Microstrip Patch Antenna — Design & Simulation

A 2.4 GHz rectangular microstrip patch antenna designed and simulated using
Python and openEMS.

The project focuses on antenna design calculations, electromagnetic simulation,
impedance matching, S-parameter analysis, VSWR, and far-field radiation
characteristics.

---

## 📌 Project Overview

This project implements and analyzes a rectangular microstrip patch antenna
operating around the 2.4 GHz ISM band.

The antenna was designed using standard microstrip patch antenna equations and
then modeled and simulated using the openEMS electromagnetic solver through
Python.

The final design uses an inset-fed rectangular patch with a 50 Ω lumped port.

### Project Flow

Design equations
      ↓
Calculate initial dimensions
      ↓
Create antenna geometry in Python
      ↓
Define substrate, ground and patch
      ↓
Add inset feed and 50 Ω port
      ↓
Generate simulation mesh
      ↓
Run FDTD electromagnetic simulation
      ↓
Calculate S11 and VSWR
      ↓
Calculate far-field radiation characteristics
      ↓
Analyze and tune the antenna

---

## 🎯 Objectives

- Design a rectangular microstrip patch antenna for 2.4 GHz.
- Calculate initial patch dimensions using standard antenna equations.
- Implement the antenna geometry using Python and openEMS.
- Understand electromagnetic simulation using the FDTD method.
- Analyze input matching using S11.
- Calculate and analyze VSWR.
- Obtain far-field radiation characteristics.
- Analyze E-plane and H-plane radiation patterns.
- Calculate directivity, efficiency and gain from simulation results.
- Understand the effect of changing antenna dimensions on resonance.

---

## 🛠️ Tools & Technologies

- Python
- NumPy
- Matplotlib
- CSXCAD
- openEMS
- FDTD electromagnetic simulation
- Antenna Theory
- Microstrip Patch Antenna Design
- S-Parameter Analysis

---

## 📐 Antenna Specifications

| Parameter | Value |
|---|---:|
| Operating Frequency | 2.4 GHz |
| Substrate | FR4 model |
| Relative Permittivity (εr) | 4.3 |
| Substrate Thickness | 1.6 mm |
| Substrate Width | 58 mm |
| Substrate Length | 65 mm |
| Patch Width | 38.37 mm |
| Patch Length | 28.95 mm |
| Feed Width | 2 mm |
| Feed Length | 10 mm |
| Inset Depth | 8 mm |
| Inset Gap | 1 mm |
| Port Resistance | 50 Ω |

---

## 📚 Antenna Design

The initial patch dimensions were calculated using standard rectangular
microstrip patch antenna equations.

### Free-Space Wavelength

For an operating frequency of 2.4 GHz:

λ₀ = c / f₀

The free-space wavelength is approximately:

**λ₀ ≈ 124.9 mm**

### Patch Width

The initial patch width was calculated using:

W = c / (2f₀) × √(2 / (εr + 1))

### Effective Dielectric Constant

The effective dielectric constant was calculated to account for the
field distribution between the substrate and air.

### Effective Length

The effective resonant length was calculated using the effective dielectric
constant.

### Fringing-Field Correction

Because electromagnetic fields extend beyond the physical edges of the patch,
a fringing-field correction was applied to obtain the physical patch length.

The calculated length was then used as the starting point for simulation
and tuning.

---

## 🧱 Antenna Structure

The antenna consists of:

1. FR4 substrate
2. Conductive ground plane
3. Rectangular patch
4. Inset feed
5. 50 Ω lumped port

The inset feed moves the feed point into the patch to obtain a better input
impedance match.

---

## 💻 Simulation Methodology

The antenna geometry is created programmatically using Python.

The electromagnetic simulation is performed using openEMS and the
Finite-Difference Time-Domain (FDTD) method.

### Simulation steps

1. Define antenna parameters.
2. Create the substrate material.
3. Create the ground plane.
4. Create the inset-fed patch.
5. Add the feed structure.
6. Define a 50 Ω lumped port.
7. Generate the simulation mesh.
8. Define absorbing boundary conditions.
9. Create the near-field-to-far-field calculation box.
10. Run the FDTD simulation.
11. Calculate S-parameters.
12. Calculate VSWR.
13. Calculate far-field radiation characteristics.
14. Generate E-plane, H-plane and 3D radiation results.

---

## 📊 Simulation Results

The simulated antenna produced a resonance close to the target
frequency.

| Parameter | Simulated Result |
|---|---:|
| Resonant Frequency | ~2.405 GHz |
| Minimum S11 | ~−13.71 dB |
| VSWR at Resonance | ~1.52 |
| Maximum Directivity | ~6.56 dBi |
| Simulated Radiation Efficiency | ~95.51% |
| Simulated Gain | ~6.36 dBi |
| E-plane 3 dB beamwidth | ~90.48° |
| H-plane 3 dB beamwidth | ~91.37° |

> **Note:** The efficiency result is based on the simulation model. The current
> model uses a lossless FR4 representation and does not include physical
> fabrication losses or measurement using a VNA. Therefore, this value should
> not be interpreted as measured real-world antenna efficiency.

---

## 📈 Plots

| S11 | VSWR |
|---|---|
| ![S11](results/S11_plot.png) | ![VSWR](results/VSWR_plot.png) |

| E-plane | H-plane |
|---|---|
| ![E-plane](results/E_plane.png) | ![H-plane](results/H_plane.png) |

| E-plane (polar) | H-plane (polar) |
|---|---|
| ![E-plane](results/E_plane_polar.png) | ![H-plane](results/H_plane_polar.png) |

---

## 📁 Project Structure

```text
2.4GHz-Microstrip-Patch-Antenna/
│
├── README.md
│
├── src/
│   ├── antenna.py
│   └── analyze.py
│
├── results/
│   ├── S11.png
│   ├── VSWR.png
│   ├── E_plane.png
│   ├── H_plane.png
│   └── 3D_pattern.png
│
├── docs/
│   └── Project_Report.pdf
│
├── simulation/
│   └── README.md
│
└── .gitignore
