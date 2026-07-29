# 🧪 Mineral Carbonation Simulator Pro
**v1.1.0 | AIBrothersTools.ir | Parviz Tajdari — Geologist & AI Architect**

[![Python](https://img.shields.io/badge/Python-3.9-blue)](https://python.org)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![CCUS](https://img.shields.io/badge/Domain-CCUS%2FCCS-orange)]()

A scientific desktop simulator for **CO₂ mineral carbonation** processes, built with PyQt5 and Avrami–Erofeev kinetic models. Designed for CCUS research, lab data management, and storage capacity estimation.

---

## 📸 Screenshots

<table>
<tr>
<th>Simulator Tab</th>
<th>Results & Plots</th>
</tr>
<tr>
<td><img width="540" alt="simulator" src="https://github.com/user-attachments/assets/c78c87e9-1e25-475e-af34-ad1691b944c8" /></td>
<td><img width="540" alt="result" src="https://github.com/user-attachments/assets/8d64adce-f297-42d2-9761-9adad4a64eff" /></td>
</tr>
</table>


## ⚙️ Supported Minerals

| Mineral | Formula | Reference |
|---|---|---|
| Olivine | Mg₂SiO₄ | Hanchen et al. (2006) |
| Serpentine | Mg₃Si₂O₅(OH)₄ | — |
| Wollastonite | CaSiO₃ | Huijgen & Comans (2005) |
| Basalt | Composite | — |
| Dolomite | CaMg(CO₃)₂ | — |

---

## 🔬 Kinetic Model

Uses the **Avrami–Erofeev** solid-state kinetic equation:

$$\alpha(t) = 1 - \exp\left[-(k \cdot t)^n\right]$$

Where:
- $\alpha$ = conversion fraction
- $k$ = rate constant (temperature & pressure dependent)
- $n$ = Avrami exponent (mineral-specific)

Rate constant follows Arrhenius:

$$k = A \cdot \exp\left(\frac{-E_a}{RT}\right) \cdot P^{0.5} \cdot C_{CO_2}^{0.8}$$

---

## 🚀 Features

- Real-time dynamic plots (Conversion α(t) & CO₂ Stored kg/t)
- Process timers: injection phase & absorption milestones
- SQLite database for run records
- CSV export
- Manual lab data entry tab
- Dark professional UI with 3D/font toggle

---

## 📦 Installation
```bash
pip install -r requirements.txt
python "Mineral Carbonation Simulator Pro.py"

---

## 👤 Author

**Parviz Tajdari** — Geologist, Python/PyQt5 Developer, AI Architect  
🔗 [kwork.com/user/parvizt](https://kwork.com/user/parvizt) | [github.com/parvizt](https://github.com/parvizt) | Parvizt@gmail.com
