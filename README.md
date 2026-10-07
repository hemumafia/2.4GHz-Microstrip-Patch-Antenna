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

### 1. Free-Space Wavelength

The wavelength corresponding to the operating frequency is:

\[
\lambda_0 = \frac{c}{f_0}
\]

Substituting:

\[
\lambda_0 =
\frac{299792458}{2.4\times10^9}
\]

\[
\boxed{\lambda_0 \approx 124.91\ mm}
\]

The free-space wavelength is approximately **124.91 mm**.

---

### 2. Patch Width

The initial patch width is calculated using:

\[
W =
\frac{c}{2f_0}
\sqrt{\frac{2}{\epsilon_r+1}}
\]

Substituting:

\[
W =
\frac{299792458}
{2(2.4\times10^9)}
\sqrt{\frac{2}{4.3+1}}
\]

\[
\boxed{W \approx 38.37\ mm}
\]

Therefore, the initial patch width was approximately **38.37 mm**.

---

### 3. Effective Dielectric Constant

The electromagnetic fields are partly contained inside the dielectric
substrate and partly in the surrounding air. Therefore, the antenna does
not behave as if it were completely inside a material having
\(\epsilon_r=4.3\).

An effective dielectric constant is therefore used:

\[
\epsilon_{eff}
=
\frac{\epsilon_r+1}{2}
+
\frac{\epsilon_r-1}{2}
\left(1+\frac{12h}{W}\right)^{-1/2}
\]

Using:

\[
\epsilon_r=4.3
\]

\[
h=1.6\ mm
\]

\[
W=38.37\ mm
\]

we obtain:

\[
\epsilon_{eff}
=
\frac{4.3+1}{2}
+
\frac{4.3-1}{2}
\left(
1+\frac{12(1.6)}{38.37}
\right)^{-1/2}
\]

\[
\boxed{\epsilon_{eff}\approx3.997}
\]

Therefore:

\[
\boxed{\epsilon_{eff}\approx4.00}
\]

---

### 4. Effective Patch Length

The effective resonant length is calculated as:

\[
L_{eff}
=
\frac{c}
{2f_0\sqrt{\epsilon_{eff}}}
\]

Substituting:

\[
L_{eff}
=
\frac{299792458}
{2(2.4\times10^9)\sqrt{3.997}}
\]

\[
\boxed{L_{eff}\approx31.24\ mm}
\]

This is the **electrical/effective length**, not yet the physical patch
length.

---

### 5. Fringing-Field Length Extension

The electric field does not stop exactly at the physical edge of the patch.
It extends slightly into the surrounding air. This is called the
**fringing field**.

The length extension is calculated using:

\[
\frac{\Delta L}{h}
=
0.412
\frac{
(\epsilon_{eff}+0.3)
\left(\frac{W}{h}+0.264\right)
}{
(\epsilon_{eff}-0.258)
\left(\frac{W}{h}+0.8\right)
}
\]

Using:

\[
\epsilon_{eff}=3.997
\]

\[
W=38.37\ mm
\]

\[
h=1.6\ mm
\]

First:

\[
\frac{W}{h}
=
\frac{38.37}{1.6}
\approx23.98
\]

Then:

\[
\frac{\Delta L}{h}
\approx0.463
\]

Therefore:

\[
\Delta L
=
0.463(1.6)
\]

\[
\boxed{\Delta L\approx0.741\ mm}
\]

So the fringing field effectively adds approximately **0.741 mm** to
each radiating edge.

---

### 6. Physical Patch Length

The physical patch length is obtained by subtracting the fringing-field
extension from both radiating edges:

\[
L=L_{eff}-2\Delta L
\]

Substituting:

\[
L=31.24-2(0.741)
\]

\[
\boxed{L\approx29.76\ mm}
\]

Therefore, the analytically calculated starting dimensions are:

\[
\boxed{W\approx38.37\ mm}
\]

\[
\boxed{L\approx29.76\ mm}
\]

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
calculated using standard microstrip antenna design equations.

### Design Parameters

| Parameter | Symbol | Value |
|---|---|---:|
| Design frequency | \(f_0\) | 2.4 GHz |
| Relative dielectric constant | \(\epsilon_r\) | 4.3 |
| Substrate thickness | \(h\) | 1.6 mm |
| Speed of light | \(c\) | 299,792,458 m/s |
| Target impedance | \(Z_0\) | 50 Ω |

---

## 🔄 Design Calculation Summary

| Quantity | Formula / Method | Result |
|---|---|---:|
| Free-space wavelength | \(\lambda_0=c/f_0\) | 124.91 mm |
| Patch width | Standard rectangular patch equation | 38.37 mm |
| Effective dielectric constant | Microstrip effective-\(\epsilon\) equation | 3.997 |
| Effective length | \(L_{eff}=c/(2f_0\sqrt{\epsilon_{eff}})\) | 31.24 mm |
| Fringing extension | \(\Delta L/h\) equation | 0.741 mm |
| Analytical patch length | \(L=L_{eff}-2\Delta L\) | 29.76 mm |
| Final simulated patch length | 28.95 mm |
| Resonant frequency | ~2.405 GHz |
| Minimum S11 | ~−13.71 dB |
| VSWR | ~1.52 |
| Maximum directivity | ~6.56 dBi |
| Radiation efficiency | ~95.51% |
| Gain | ~6.36 dBi |

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

## 📡 Inset Feed

An inset feed is used to improve the impedance matching between the
antenna and the 50 Ω source.

The feed is moved into the patch by an inset depth rather than connecting
directly at the patch edge.

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

The final feed position was evaluated through full-wave electromagnetic
simulation using the S11 response.

---

## 🔌 50 Ω Lumped Port

The antenna is excited using a lumped port with a reference impedance of:

$$
Z_0 = 50\ \Omega
$$

A 50 Ω reference impedance is commonly used in RF systems to evaluate
the impedance matching of the antenna.

The lumped port is placed across the feed and ground and is used to
excite the antenna during the FDTD simulation.

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
