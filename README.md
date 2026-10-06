# 2.4 GHz Microstrip Patch Antenna — Design & FDTD Simulation

Design, FDTD electromagnetic simulation, and radiation-pattern analysis of an
inset-fed rectangular microstrip patch antenna for the 2.4 GHz ISM band
(Wi-Fi / Bluetooth / IoT), built entirely in Python using
[openEMS](https://openems.de/) and CSXCAD.

> Academic/independent simulation project — not fabricated or
> hardware-measured. All results below are simulation outputs.

---

## 📊 Final Results

| Parameter | Value |
|---|---|
| Resonant frequency | **2.405 GHz** (0.21% off 2.4 GHz target) |
| Minimum S11 | **-13.71 dB** |
| VSWR at resonance | **1.52** |
| -10 dB bandwidth | 28.86 MHz (1.20%) |
| VSWR ≤ 2 bandwidth | 35.37 MHz (1.47%) |
| Directivity | 6.56 dBi |
| Gain | 6.36 dBi |
| Radiation efficiency | 95.51% *(idealized model — see Limitations)* |
| E-plane 3 dB beamwidth | 90.48° |
| H-plane 3 dB beamwidth | 91.37° |

### Plots

<!-- Add these images to an assets/ folder in your repo root -->
| S11 | VSWR |
|---|---|
| ![S11](assets/S11_plot.png) | ![VSWR](assets/VSWR_plot.png) |

| E-plane (polar) | H-plane (polar) |
|---|---|
| ![E-plane](assets/E_plane_polar.png) | ![H-plane](assets/H_plane_polar.png) |

---

## 🧩 Design Parameters

| Parameter | Value |
|---|---|
| Substrate | FR4, εᵣ = 4.3, 1.6 mm thick |
| Substrate footprint | 58 × 65 mm |
| Patch dimensions | 38.37 × 28.95 mm |
| Feed type | Inset microstrip |
| Feed dimensions | 2.0 × 10.0 mm |
| Inset depth / gap | 8.0 mm / 1.0 mm each side |
| Conductors | Zero-thickness PEC |
| Port | 50 Ω lumped port |

---

## 🛠️ Simulation Setup

- **Solver:** openEMS (open-source FDTD), driven via Python/CSXCAD
- **Mesh:** non-uniform, edge-aligned to all metal boundaries, 2 mm max cell size
- **Boundaries:** PML_8 on all six faces
- **Excitation:** Gaussian pulse, 2.4 GHz center, 1.0 GHz bandwidth
- **Far field:** NF2FF box, recorded during the run and post-processed for
  directivity, gain, and E/H-plane radiation patterns

```
antenna.py   → builds geometry, mesh, port, boundaries; runs the FDTD solve
analyze.py   → reads port + NF2FF data; computes S11, VSWR, bandwidth,
               directivity, gain, efficiency, beamwidth; generates all plots
```

### Running it

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

- Conductors are modeled as perfect electric conductors (PEC) — zero
  conductor loss.
- The FR4 substrate is modeled with εᵣ = 4.3 only, no dielectric loss
  tangent — i.e., a lossless dielectric.
- As a result, the 95.5% radiation efficiency reflects how completely the
  FDTD simulation's stored energy had radiated out by the solver's end
  criterion, **not** a hardware efficiency prediction. A fabricated FR4
  antenna with a realistic loss tangent (~0.02) would show lower efficiency
  and somewhat wider bandwidth.
- S11, VSWR, and radiation pattern *shape* (lobe direction, beamwidth, null
  positions) are geometry/resonance-driven and expected to transfer more
  directly to a real prototype than the efficiency/gain figures.

---

## 📚 References

1. C. A. Balanis, *Antenna Theory: Analysis and Design*, 4th ed., Wiley, 2016.
2. [openEMS](https://openems.de/) — open-source FDTD electromagnetic solver.
3. [CSXCAD](https://openems.de/) — geometry library used with openEMS.
