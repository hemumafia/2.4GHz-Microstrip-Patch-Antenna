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

## 📐 Antenna Design Calculations

The initial dimensions of the rectangular microstrip patch antenna were
calculated using standard microstrip antenna design equations.

### Design Parameters

| Parameter | Symbol | Value |
|---|---|---:|
| Design frequency | 2.4 GHz |
| Relative dielectric constant | 4.3 |
| Substrate thickness | 1.6 mm |
| Speed of light | 300,000,000 m/s |
| Target impedance | 50 Ω |

---

### 7. Analytical Design vs Final Simulation Model

The analytical calculation provides the starting dimensions. The final
simulation model was tuned to obtain resonance close to 2.4 GHz.

| Parameter | Analytical Starting Value | Final Simulation Model |
|---|---:|---:|
| Patch Width | 38.37 mm | 38.37 mm |
| Patch Length | ~29.76 mm | 28.95 mm |
| Substrate Width | — | 58 mm |
| Substrate Length | — | 65 mm |
| Substrate Thickness | 1.6 mm | 1.6 mm |
| Feed Width | — | 2 mm |
| Feed Length | — | 10 mm |
| Inset Depth | — | 8 mm |
| Inset Gap | — | 1 mm |
| Port Resistance | — | 50 Ω |

The difference between the analytical length and final simulated length
is due to the fact that the analytical equations provide an initial
design approximation. The final geometry was evaluated using full-wave
electromagnetic simulation.

---

## 📐 Antenna Design Calculations

The initial dimensions of the rectangular microstrip patch antenna were
calculated using standard microstrip patch antenna design equations.

### Design Parameters

| Parameter | Symbol | Value |
|---|---|---:|
| Design frequency | \(f_0\) | 2.4 GHz |
| Relative dielectric constant | \(\epsilon_r\) | 4.3 |
| Substrate thickness | \(h\) | 1.6 mm |
| Speed of light | \(c\) | 299,792,458 m/s |
| Target impedance | \(Z_0\) | 50 Ω |

---

### 1. Free-Space Wavelength

The free-space wavelength is calculated using:

$$
\lambda_0 = \frac{c}{f_0}
$$

Substituting the design frequency:

$$
\lambda_0 =
\frac{299792458}
{2.4\times10^9}
$$

Therefore:

$$
\boxed{\lambda_0 \approx 124.91\ \text{mm}}
$$

The free-space wavelength at 2.4 GHz is approximately **124.91 mm**.

---

### 2. Patch Width

The initial patch width is calculated using:

$$
W =
\frac{c}{2f_0}
\sqrt{\frac{2}{\epsilon_r+1}}
$$

Substituting:

$$
W =
\frac{299792458}
{2(2.4\times10^9)}
\sqrt{\frac{2}{4.3+1}}
$$

Therefore:

$$
\boxed{W \approx 38.37\ \text{mm}}
$$

The calculated patch width is approximately **38.37 mm**.

---

### 3. Effective Dielectric Constant

The electromagnetic field exists partly inside the dielectric substrate and
partly in the air above the patch. Therefore, an effective dielectric
constant is used.

The effective dielectric constant is calculated using:

$$
\epsilon_{eff}
=
\frac{\epsilon_r+1}{2}
+
\frac{\epsilon_r-1}{2}
\left(
1+\frac{12h}{W}
\right)^{-1/2}
$$

Using:

$$
\epsilon_r = 4.3
$$

$$
h = 1.6\ \text{mm}
$$

$$
W = 38.37\ \text{mm}
$$

Substituting:

$$
\epsilon_{eff}
=
\frac{4.3+1}{2}
+
\frac{4.3-1}{2}
\left(
1+\frac{12(1.6)}{38.37}
\right)^{-1/2}
$$

Therefore:

$$
\boxed{\epsilon_{eff} \approx 3.997}
$$

or approximately:

$$
\boxed{\epsilon_{eff} \approx 4.00}
$$

---

### 4. Effective Patch Length

The effective resonant length is calculated using:

$$
L_{eff}
=
\frac{c}
{2f_0\sqrt{\epsilon_{eff}}}
$$

Substituting:

$$
L_{eff}
=
\frac{299792458}
{2(2.4\times10^9)\sqrt{3.997}}
$$

Therefore:

$$
\boxed{L_{eff} \approx 31.24\ \text{mm}}
$$

This is the **effective electrical length** of the patch before correcting
for the fringing fields.

---

### 5. Fringing-Field Length Extension

The electric field extends slightly beyond the physical edges of the patch.
This phenomenon is called the **fringing field**.

The length extension is calculated using:

$$
\frac{\Delta L}{h}
=
0.412
\frac{
(\epsilon_{eff}+0.3)
\left(
\frac{W}{h}+0.264
\right)
}{
(\epsilon_{eff}-0.258)
\left(
\frac{W}{h}+0.8
\right)
}
$$

First, calculate the width-to-height ratio:

$$
\frac{W}{h}
=
\frac{38.37}{1.6}
$$

$$
\frac{W}{h} \approx 23.98
$$

Substituting the values:

$$
\frac{\Delta L}{h}
=
0.412
\frac{
(3.997+0.3)(23.98+0.264)
}{
(3.997-0.258)(23.98+0.8)
}
$$

This gives approximately:

$$
\frac{\Delta L}{h} \approx 0.463
$$

Therefore:

$$
\Delta L
=
0.463(1.6)
$$

$$
\boxed{\Delta L \approx 0.741\ \text{mm}}
$$

The fringing-field extension is approximately **0.741 mm per radiating
edge**.

---

### 6. Physical Patch Length

Because the effective length includes the extension caused by fringing
fields, the physical patch length is calculated as:

$$
L = L_{eff} - 2\Delta L
$$

Substituting:

$$
L = 31.24 - 2(0.741)
$$

Therefore:

$$
\boxed{L \approx 29.76\ \text{mm}}
$$

Thus, the analytically calculated starting dimensions are:

$$
\boxed{W \approx 38.37\ \text{mm}}
$$

$$
\boxed{L \approx 29.76\ \text{mm}}
$$

---

## 📊 Analytical Dimensions vs Final Simulation Dimensions

The analytical equations provide the **initial dimensions**. The antenna was
then implemented in openEMS and evaluated using full-wave electromagnetic
simulation.

The final geometry was adjusted to obtain resonance close to the target
frequency.

| Parameter | Analytical Starting Value | Final Simulation Model |
|---|---:|---:|
| Patch Width | 38.37 mm | 38.37 mm |
| Patch Length | 29.76 mm | 28.95 mm |
| Substrate Width | — | 58 mm |
| Substrate Length | — | 65 mm |
| Substrate Thickness | 1.6 mm | 1.6 mm |
| Feed Width | — | 2 mm |
| Feed Length | — | 10 mm |
| Inset Depth | — | 8 mm |
| Inset Gap | — | 1 mm |
| Port Resistance | — | 50 Ω |

The difference between the analytical patch length and the final simulated
length is expected because the analytical equations provide an initial
approximation, while the final design is evaluated using a full-wave
electromagnetic solver.

---

## 📡 Inset Feed

An inset feed is used to improve the impedance matching between the antenna
and the 50 Ω source.

Instead of feeding the patch only at its edge, the feed is extended into the
patch by a specific distance.

### Inset Feed Parameters

$$
\text{Inset depth} = 8\ \text{mm}
$$

$$
\text{Inset gap} = 1\ \text{mm}
$$

$$
\text{Feed width} = 2\ \text{mm}
$$

The feed position affects the input impedance of the antenna. The final feed
position was evaluated using the full-wave simulation and S11 response.

---

## 🔌 50 Ω Lumped Port

The antenna is excited using a lumped port with a reference impedance of:

$$
Z_0 = 50\ \Omega
$$

The lumped port is connected between the feed and ground and provides the
electromagnetic excitation for the FDTD simulation.

A 50 Ω reference impedance is used to evaluate how well the antenna is
matched to a typical RF source or transmission system.

---

## 📉 S11

S11 represents the reflection coefficient at the antenna input.

The magnitude of the reflection coefficient is related to S11 in dB by:

$$
S_{11(dB)}
=
20\log_{10}|\Gamma|
$$

where:

$$
\Gamma =
\frac{Z_{in}-Z_0}
{Z_{in}+Z_0}
$$

Here:

- \(Z_{in}\) = antenna input impedance
- \(Z_0\) = reference impedance
- \(\Gamma\) = reflection coefficient

For a 50 Ω system:

$$
Z_0 = 50\ \Omega
$$

A more negative S11 value indicates that less power is reflected back toward
the source.

For example:

$$
S_{11}=-10\ \text{dB}
$$

corresponds to approximately 10% reflected power.

The simulated antenna achieved:

$$
\boxed{S_{11,min}\approx-13.71\ \text{dB}}
$$

at approximately:

$$
\boxed{f_r\approx2.405\ \text{GHz}}
$$

---

## 📊 VSWR

Voltage Standing Wave Ratio (VSWR) indicates the quality of impedance
matching between the antenna and the transmission system.

It is calculated from the magnitude of the reflection coefficient:

$$
VSWR =
\frac{1+|\Gamma|}
{1-|\Gamma|}
$$

For a perfectly matched antenna:

$$
\boxed{VSWR=1}
$$

The simulated antenna produced approximately:

$$
\boxed{VSWR\approx1.52}
$$

at the resonant frequency.

---

## 📡 Radiation Pattern

The radiation pattern describes how the antenna radiates electromagnetic
energy in different directions.

The simulation calculates the far-field radiation pattern using the
near-field-to-far-field transformation provided by openEMS.

The project analyzes:

- E-plane radiation pattern
- H-plane radiation pattern
- 3D radiation pattern

---

## 🎯 Directivity

Directivity describes how concentrated the radiated power is in a particular
direction compared with an isotropic radiator.

The maximum simulated directivity was approximately:

$$
\boxed{D_{max}\approx6.56\ \text{dBi}}
$$

When directivity is available in linear form, it can be converted to dBi
using:

$$
D_{dBi}=10\log_{10}(D)
$$

---

## ⚡ Radiation Efficiency

Radiation efficiency is the ratio of radiated power to accepted input power:

$$
\eta =
\frac{P_{rad}}
{P_{accepted}}
$$

where:

- \(P_{rad}\) = total radiated power
- \(P_{accepted}\) = power accepted by the antenna

The simulation produced approximately:

$$
\boxed{\eta\approx95.51\%}
$$

> **Important:** This is a result from the current simulation model. The FR4
> material is modeled as lossless in this project, and no fabricated antenna
> has been measured using a VNA. Therefore, this value should not be
> interpreted as the measured real-world efficiency of a fabricated FR4
> antenna.

---

## 📶 Antenna Gain

Antenna gain combines directivity and radiation efficiency:

$$
G = D\eta
$$

When expressed in dB:

$$
G_{dBi}
=
D_{dBi}
+
10\log_{10}(\eta)
$$

The simulated antenna produced approximately:

$$
\boxed{G\approx6.36\ \text{dBi}}
$$

---

## 🧮 Final Design Calculation Summary

| Quantity | Formula / Method | Result |
|---|---|---:|
| Free-space wavelength | \(\lambda_0=c/f_0\) | 124.91 mm |
| Patch width | Standard rectangular patch equation | 38.37 mm |
| Effective dielectric constant | Effective-\(\epsilon\) equation | 3.997 |
| Effective length | \(L_{eff}=c/(2f_0\sqrt{\epsilon_{eff}})\) | 31.24 mm |
| Fringing extension | \(\Delta L/h\) equation | 0.741 mm |
| Analytical patch length | \(L=L_{eff}-2\Delta L\) | 29.76 mm |
| Final patch length | Full-wave simulation tuning | 28.95 mm |
| Inset depth | Simulation parameter | 8 mm |
| Inset gap | Simulation parameter | 1 mm |
| Feed width | Simulation parameter | 2 mm |
| Port impedance | Simulation parameter | 50 Ω |
| Resonant frequency | Minimum S11 | ~2.405 GHz |
| Minimum S11 | Simulation | ~−13.71 dB |
| VSWR | \((1+|\Gamma|)/(1-|\Gamma|)\) | ~1.52 |
| Maximum directivity | NF2FF simulation | ~6.56 dBi |
| Radiation efficiency | \(P_{rad}/P_{accepted}\) | ~95.51% |
| Gain | \(D\eta\) | ~6.36 dBi |

---

## 🔄 Design-to-Simulation Flow

The overall design process can be summarized as:

$$
f_0,\epsilon_r,h
\rightarrow
W
\rightarrow
\epsilon_{eff}
\rightarrow
L_{eff}
\rightarrow
\Delta L
\rightarrow
L
$$

The calculated dimensions were then used as the starting point for the
full-wave openEMS simulation:

$$
\text{Analytical Design}
\rightarrow
\text{Geometry}
\rightarrow
\text{Mesh}
\rightarrow
\text{FDTD Simulation}
\rightarrow
S_{11},VSWR,\text{Radiation}
$$

The final simulated geometry was evaluated and tuned around the target
frequency of 2.4 GHz.

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

### S11

![S11](results/S11_plot.png)

S11 is used to evaluate how much of the input signal is reflected from the
antenna.

A lower S11 value indicates better impedance matching at that frequency.

---

### VSWR

![VSWR](results/VSWR_plot.png)

VSWR describes the quality of impedance matching between the antenna and the
50 Ω feed.

---

### E-Plane Radiation Pattern

![E-Plane](results/E_plane.png)

---

### H-Plane Radiation Pattern

![H-Plane](results/H_plane.png)

---

### 3D Radiation Pattern

![3D Radiation Pattern](results/3D_pattern.png)

Simulated 3D Radiation Pattern is spherical which is not desirable for proper 
of the results below are the polar plots of E-plane and H-plane.

---

### E-Plane (Polar)

![E-plane](results/E_plane_polar.png)

---

### H-Plane (Polar)

![H-plane](results/H_plane_polar.png)

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
└── docs/
    └── Project_Report.pdf
```

## Running it

```bash
python antenna.py     # runs the EM simulation (several minutes)
python analyze.py     # post-processes results, generates plots + report.txt
```

`analyze.py` can be re-run on its own after the first simulation — it only
reads the saved field data, so you don't need to re-run the FDTD solve to
regenerate plots or tweak post-processing.

**Dependencies:** `openEMS`, `CSXCAD`, `numpy`, `matplotlib`, `h5py`

---

## 🔍 What I Actually Learned

This project taught me more about antennas than any single antenna I'd
studied before. Antenna parameters are crucial, but antenna design alone
isn't enough — real-world performance also depends on the operating
environment, the radiation field, the specific use case the antenna is
built for, and noise. It's not just about designing an antenna on paper;
it's about correctly fitting it to practical use. Plots like S11, VSWR, and
radiation pattern aren't just outputs for a report — they're what let you
verify a design will actually hold up outside the simulator.

A few concrete debugging lessons from this build, in case they save someone
else time:

- **A tiny mesh cell anywhere tanks your FDTD timestep.** Modeling finite
  (35 µm) copper thickness forced a CFL-limited timestep around 1e-13 s,
  making every run painfully slow. Since skin depth at 2.4 GHz (~1.3 µm) is
  already far thinner than real copper, zero-thickness PEC is both faster
  *and* a more accurate idealization.
- **An inset feed only works if the notch is an actual gap.** My first
  version had the feed touching the patch on both sides of the "notch,"
  so changing inset depth did nothing to S11. Changing inset depth is
  meaningless until you verify the gap geometry is real.
- **Don't trust a derived plot without checking it against raw data.**
  My first 3D radiation pattern looked nearly spherical despite a real
  ~15 dB front-to-back ratio, because it was built from the wrong field
  array. Cross-checking it against `P_rad`-derived directivity (which the
  E/H-plane cuts already agreed with) caught the bug.

---

## ⚠️ Limitations

The current simulation has several limitations:
- The FR4 model is treated as lossless.
- No fabricated antenna was measured using a Vector Network Analyzer (VNA).
- Connector and cable losses are not included.
- Manufacturing tolerances are not included.
- The simulated results may differ from a physically fabricated antenna.

---

## 👨‍💻 Author

- Hemanth Kumar Akkala
- B.Tech — Electronics and Communication Engineering
- Interested in Embedded Systems, Electronics, RF/Antennas and Robotics.

<p align="left">
  <a href="https://www.linkedin.com/in/hemanth-kumar-akkala/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
  <a href="mailto:hemanthboy21gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
</p>
