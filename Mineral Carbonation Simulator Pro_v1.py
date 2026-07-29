# ============================================================
# Mineral Carbonation Simulator Pro
# Version: 1.1.0
# Website: AIBrothersTools.ir
# Organization: AiBrothers Tools
# Author: Parviz Tajdari
# ============================================================

import sys
import os
import math
import sqlite3
import csv
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox,
    QTextEdit, QSplitter, QStatusBar, QMessageBox,
    QFileDialog, QCheckBox, QSlider, QProgressBar,
    QHeaderView, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush, QPen
import pyqtgraph as pg
import numpy as np

# ── App Identity ──────────────────────────────────────────────
APP_NAME    = "Mineral Carbonation Simulator Pro"
APP_VERSION = "1.1.0"
APP_ORG     = "AiBrothers Tools"
APP_WEB     = "AIBrothersTools.ir"
WATERMARK   = "© kwork.com/user/parvizt"

# ── MEIPASS asset resolver ─────────────────────────────────────
def _asset(name: str) -> str:
    """Resolve asset path for both dev and PyInstaller --onefile."""
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    local = os.path.join(base, name)
    if os.path.exists(local):
        return local
    # fallback: d:/ drive (dev environment)
    drive = os.path.join("d:/", name)
    if os.path.exists(drive):
        return drive
    return local  # return path even if missing (QPixmap handles gracefully)

ICO_PATH = _asset("l.ico")
QR_PATH  = _asset("qr.png")
LOGO_PATH= _asset("l.png")

# ── Color Palette ─────────────────────────────────────────────
BG       = "#1a1a1a"
TXT      = "#00ff00"
INP      = "#2a2a2a"
BRD      = "#444444"
PINK     = "#ff69b4"
DARK2    = "#141414"
ACCENT   = "#00cc00"
RED      = "#ff4444"
AMBER    = "#ffaa00"
BLUE     = "#4488ff"

# ── Classic (default) theme ────────────────────────────────────
STYLE_CLASSIC = f"""
QMainWindow, QWidget {{
    background-color: {BG};
    color: {TXT};
    font-family: 'Consolas', 'Courier New', monospace;
}}
QTabWidget::pane {{
    border: 1px solid {BRD};
    background: {BG};
}}
QTabBar::tab {{
    background: {INP};
    color: {TXT};
    padding: 8px 18px;
    border: 1px solid {BRD};
    border-bottom: none;
    font-size: 11px;
}}
QTabBar::tab:selected {{
    background: {DARK2};
    color: {PINK};
    border-bottom: 2px solid {PINK};
}}
QGroupBox {{
    border: 1px solid {BRD};
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 8px;
    color: {PINK};
    font-size: 11px;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}}
QLabel {{ color: {TXT}; font-size: 11px; }}
QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox {{
    background: {INP};
    color: {TXT};
    border: 1px solid {BRD};
    border-radius: 3px;
    padding: 4px 6px;
    font-size: 11px;
}}
QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {PINK};
}}
QPushButton {{
    background: {INP};
    color: {TXT};
    border: 1px solid {BRD};
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 11px;
}}
QPushButton:hover {{
    background: #3a3a3a;
    border: 1px solid {PINK};
    color: {PINK};
}}
QPushButton:pressed {{ background: {DARK2}; }}
QPushButton#btn_run {{
    background: #003300;
    color: {TXT};
    border: 1px solid {ACCENT};
    font-weight: bold;
    font-size: 12px;
}}
QPushButton#btn_run:hover {{
    background: #004400;
    border-color: {TXT};
}}
QPushButton#btn_reset {{
    background: #330000;
    color: {RED};
    border: 1px solid {RED};
}}
QPushButton#btn_export {{
    background: #001133;
    color: {BLUE};
    border: 1px solid {BLUE};
}}
QTableWidget {{
    background: {INP};
    color: {TXT};
    border: 1px solid {BRD};
    gridline-color: {BRD};
    font-size: 10px;
}}
QTableWidget::item:selected {{ background: #2a4a2a; color: {TXT}; }}
QHeaderView::section {{
    background: {DARK2};
    color: {PINK};
    border: 1px solid {BRD};
    padding: 4px;
    font-size: 10px;
}}
QTextEdit {{
    background: {INP};
    color: {TXT};
    border: 1px solid {BRD};
    font-family: 'Consolas', monospace;
    font-size: 10px;
}}
QProgressBar {{
    background: {INP};
    border: 1px solid {BRD};
    border-radius: 3px;
    text-align: center;
    color: {TXT};
    font-size: 10px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #003300, stop:1 {ACCENT});
    border-radius: 3px;
}}
QStatusBar {{
    background: {DARK2};
    color: {TXT};
    border-top: 1px solid {BRD};
    font-size: 10px;
}}
QSlider::groove:horizontal {{
    height: 4px; background: {BRD}; border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {PINK};
    width: 14px; height: 14px;
    margin: -5px 0; border-radius: 7px;
}}
QCheckBox {{ color: {TXT}; font-size: 11px; spacing: 6px; }}
QCheckBox::indicator {{
    width: 16px; height: 16px;
    border: 1px solid {BRD};
    background: {INP}; border-radius: 3px;
}}
QCheckBox::indicator:checked {{
    background: {PINK}; border-color: {PINK};
}}
QSplitter::handle {{ background: {BRD}; }}
"""

# 3D addon (applied on top of classic)
STYLE_3D_ADDON = f"""
QPushButton {{
    border: 2px outset {BRD};
    border-radius: 6px;
    font-size: 12px;
}}
QPushButton:pressed {{ border: 2px inset {BRD}; }}
QGroupBox {{ border: 2px groove {BRD}; font-size: 12px; }}
QLabel {{ font-size: 12px; }}
QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox {{
    border: 2px inset {BRD}; font-size: 12px;
}}
QTabBar::tab {{ font-size: 12px; padding: 9px 20px; }}
"""

# ─────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("carbonation_sim.db")
        self._init_tables()

    def _init_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS simulations (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp    TEXT,
                mineral      TEXT,
                temperature  REAL,
                pressure     REAL,
                co2_conc     REAL,
                liquid_ratio REAL,
                duration     REAL,
                conversion   REAL,
                co2_stored   REAL,
                inject_time  REAL,
                absorb_time  REAL,
                notes        TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS manual_data (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp  TEXT,
                label      TEXT,
                time_h     REAL,
                conversion REAL,
                co2_kg     REAL
            )
        """)
        # migrate: add timer columns if upgrading from v1.0
        for col in ("inject_time", "absorb_time"):
            try:
                c.execute(f"ALTER TABLE simulations ADD COLUMN {col} REAL DEFAULT 0")
            except Exception:
                pass
        self.conn.commit()

    def save_simulation(self, params: dict):
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO simulations
            (timestamp,mineral,temperature,pressure,co2_conc,liquid_ratio,
             duration,conversion,co2_stored,inject_time,absorb_time,notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            params["mineral"], params["temperature"], params["pressure"],
            params["co2_conc"], params["liquid_ratio"], params["duration"],
            params["conversion"], params["co2_stored"],
            params.get("inject_time", 0.0), params.get("absorb_time", 0.0),
            params.get("notes", "")
        ))
        self.conn.commit()

    def get_all_simulations(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM simulations ORDER BY id DESC")
        return c.fetchall()

    def save_manual(self, label, time_h, conversion, co2_kg):
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO manual_data (timestamp,label,time_h,conversion,co2_kg)
            VALUES (?,?,?,?,?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), label, time_h, conversion, co2_kg))
        self.conn.commit()

    def get_manual_data(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM manual_data ORDER BY id DESC")
        return c.fetchall()

# ─────────────────────────────────────────────────────────────
# SIMULATION ENGINE  (Avrami–Erofeev kinetic model)
# ─────────────────────────────────────────────────────────────
class CarbonationEngine:
    """
    Mineral carbonation kinetics — Avrami–Erofeev model:
        α(t) = 1 − exp(−(k·t)ⁿ)

    Arrhenius:   k(T) = A · exp(−Ea / R·T)
    Pressure:    k_eff = k · (P/P_ref)^m
    CO₂ driving: × (c/c_ref)^0.3
    L/S wetting: × (1 + 0.08·ln(L/S))

    Injection time  = time for α to reach 10 % (CO₂ breakthrough)
    Absorption time = time for α to reach 90 % (practical completion)
    """

    MINERALS = {
        "Wollastonite (CaSiO₃)": {
            "A": 2.5e6, "Ea": 65000, "n": 0.70,
            "MW": 116.16, "stoich": 1.0, "co2_factor": 380,
            "color": BLUE,
            "ref": "Huijgen & Comans (2005)"
        },
        "Serpentine (Mg₃Si₂O₅(OH)₄)": {
            "A": 1.2e5, "Ea": 72000, "n": 0.60,
            "MW": 277.11, "stoich": 3.0, "co2_factor": 460,
            "color": ACCENT,
            "ref": "Lackner et al. (1995)"
        },
        "Olivine (Mg₂SiO₄)": {
            "A": 3.8e6, "Ea": 63000, "n": 0.75,
            "MW": 140.69, "stoich": 2.0, "co2_factor": 620,
            "color": PINK,
            "ref": "Hanchen et al. (2006)"
        },
        "Basalt (Composite)": {
            "A": 1.5e5, "Ea": 58000, "n": 0.65,
            "MW": 200.0,  "stoich": 1.5, "co2_factor": 200,
            "color": AMBER,
            "ref": "Matter & Kelemen (2009) — CarbFix"
        },
        "Dolomite (CaMg(CO₃)₂)": {
            "A": 4.0e4, "Ea": 55000, "n": 0.80,
            "MW": 184.40, "stoich": 2.0, "co2_factor": 477,
            "color": RED,
            "ref": "Pokrovsky & Schott (2001)"
        },
    }

    R = 8.314  # J/mol·K

    @classmethod
    def simulate(cls, mineral: str, T_C: float, P_bar: float,
                 co2_conc: float, L_S: float, duration_h: float,
                 steps: int = 400):
        """
        Returns (time_arr, alpha_arr_pct, co2_arr, inject_h, absorb_h)
        inject_h  = estimated time to reach α = 10 %  (injection phase)
        absorb_h  = estimated time to reach α = 90 %  (absorption complete)
        """
        props  = cls.MINERALS[mineral]
        T_K    = T_C + 273.15
        P_ref  = 10.0
        m      = 0.45

        k_base  = props["A"] * math.exp(-props["Ea"] / (cls.R * T_K))
        k_eff   = k_base * (P_bar / P_ref) ** m
        co2_fac = (co2_conc / 0.05) ** 0.3
        ls_fac  = 1.0 + 0.08 * math.log(max(L_S, 1.0))
        k_final = k_eff * co2_fac * ls_fac

        t_arr   = np.linspace(0, duration_h, steps)
        n       = props["n"]
        alpha   = 1.0 - np.exp(-(k_final * t_arr) ** n)
        alpha   = np.clip(alpha, 0.0, 1.0)
        co2_arr = alpha * props["co2_factor"]

        # ── Timer estimates ───────────────────────────────────
        # Invert α(t) = 1 − exp(−(k·t)^n)  →  t = (−ln(1−α))^(1/n) / k
        def _t_at(target_alpha):
            if k_final <= 0:
                return duration_h
            val = (-math.log(1.0 - target_alpha)) ** (1.0 / n) / k_final
            return min(val, duration_h * 5)  # cap at 5× window

        inject_h = _t_at(0.10)   # 10 % = CO₂ breakthrough / start of significant uptake
        absorb_h = _t_at(0.90)   # 90 % = practical completion

        return t_arr, alpha * 100.0, co2_arr, inject_h, absorb_h

# ─────────────────────────────────────────────────────────────
# SIMULATION WORKER THREAD
# ─────────────────────────────────────────────────────────────
class SimWorker(QThread):
    progress  = pyqtSignal(int)
    finished  = pyqtSignal(object, object, object, dict)
    error_sig = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        try:
            p = self.params
            for i in range(1, 6):
                self.progress.emit(i * 18)
                self.msleep(80)
            t, alpha, co2, inject_h, absorb_h = CarbonationEngine.simulate(
                mineral    = p["mineral"],
                T_C        = p["temperature"],
                P_bar      = p["pressure"],
                co2_conc   = p["co2_conc"],
                L_S        = p["liquid_ratio"],
                duration_h = p["duration"],
            )
            self.progress.emit(100)
            result = {
                "conversion": float(alpha[-1]),
                "co2_stored": float(co2[-1]),
                "inject_time": inject_h,
                "absorb_time": absorb_h,
            }
            self.finished.emit(t, alpha, co2, result)
        except Exception as e:
            self.error_sig.emit(str(e))

# ─────────────────────────────────────────────────────────────
# TIMER PANEL  (countdown / estimate display)
# ─────────────────────────────────────────────────────────────
class TimerPanel(QFrame):
    """
    Displays two estimated timers:
      • CO₂ Injection Phase  (α → 10%)
      • CO₂ Absorption Complete (α → 90%)
    Also runs a live elapsed-seconds counter when simulation starts.
    """
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"background:{DARK2}; border:1px solid {BRD}; border-radius:4px;")
        self._inject_h  = 0.0
        self._absorb_h  = 0.0
        self._elapsed   = 0
        self._running   = False

        lay = QGridLayout(self)
        lay.setContentsMargins(8, 6, 8, 6)
        lay.setSpacing(4)

        def _lbl(txt, color=TXT, bold=False, size=10):
            l = QLabel(txt)
            w = "bold" if bold else "normal"
            l.setStyleSheet(f"color:{color}; font-size:{size}px; font-weight:{w}; background:transparent;")
            return l

        lay.addWidget(_lbl("⏱  Process Timers", PINK, bold=True, size=11), 0, 0, 1, 4)

        lay.addWidget(_lbl("CO₂ Injection Phase:", AMBER),   1, 0)
        self.lbl_inject = _lbl("—", TXT, bold=True)
        lay.addWidget(self.lbl_inject, 1, 1)

        lay.addWidget(_lbl("(α reaches 10%)", BRD, size=9),  1, 2, 1, 2)

        lay.addWidget(_lbl("CO₂ Absorption Done:", BLUE),    2, 0)
        self.lbl_absorb = _lbl("—", TXT, bold=True)
        lay.addWidget(self.lbl_absorb, 2, 1)

        lay.addWidget(_lbl("(α reaches 90%)", BRD, size=9),  2, 2, 1, 2)

        lay.addWidget(_lbl("Live Elapsed:", ACCENT),          3, 0)
        self.lbl_elapsed = _lbl("00:00:00", TXT)
        lay.addWidget(self.lbl_elapsed, 3, 1)

        self.btn_timer = QPushButton("▶ Start")
        self.btn_timer.setFixedWidth(70)
        self.btn_timer.setStyleSheet(
            f"background:#002200; color:{ACCENT}; border:1px solid {ACCENT};"
            f"border-radius:3px; font-size:10px; padding:2px 6px;"
        )
        self.btn_timer.clicked.connect(self._toggle_timer)
        lay.addWidget(self.btn_timer, 3, 2)

        self.btn_rst = QPushButton("↺")
        self.btn_rst.setFixedWidth(28)
        self.btn_rst.setStyleSheet(
            f"background:#330000; color:{RED}; border:1px solid {RED};"
            f"border-radius:3px; font-size:10px; padding:2px;"
        )
        self.btn_rst.clicked.connect(self._reset_timer)
        lay.addWidget(self.btn_rst, 3, 3)

        self._ticker = QTimer(self)
        self._ticker.timeout.connect(self._tick)

    # ── public ────────────────────────────────────────────────
    def update_estimates(self, inject_h: float, absorb_h: float):
        self._inject_h = inject_h
        self._absorb_h = absorb_h
        self.lbl_inject.setText(self._fmt_h(inject_h))
        self.lbl_absorb.setText(self._fmt_h(absorb_h))

    # ── internal ──────────────────────────────────────────────
    def _fmt_h(self, hours: float) -> str:
        if hours >= 24:
            d = hours / 24
            return f"~{d:.1f} days"
        if hours >= 1:
            return f"~{hours:.2f} h"
        m = hours * 60
        if m >= 1:
            return f"~{m:.1f} min"
        return f"~{m*60:.0f} sec"

    def _toggle_timer(self):
        if self._running:
            self._ticker.stop()
            self._running = False
            self.btn_timer.setText("▶ Start")
        else:
            self._ticker.start(1000)
            self._running = True
            self.btn_timer.setText("⏸ Pause")

    def _reset_timer(self):
        self._ticker.stop()
        self._running = False
        self._elapsed = 0
        self.btn_timer.setText("▶ Start")
        self.lbl_elapsed.setText("00:00:00")

    def _tick(self):
        self._elapsed += 1
        h = self._elapsed // 3600
        m = (self._elapsed % 3600) // 60
        s = self._elapsed % 60
        self.lbl_elapsed.setText(f"{h:02d}:{m:02d}:{s:02d}")

# ─────────────────────────────────────────────────────────────
# LOGO / QR PANEL
# ─────────────────────────────────────────────────────────────
class BrandPanel(QFrame):
    """Logo + QR code panel — assets survive PyInstaller via MEIPASS."""
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"background:{DARK2}; border:1px solid {BRD}; border-radius:4px;")
        self.setFixedHeight(80)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 4, 8, 4)
        lay.setSpacing(10)

        # logo
        self.lbl_logo = QLabel()
        self.lbl_logo.setFixedSize(64, 64)
        self.lbl_logo.setAlignment(Qt.AlignCenter)
        self.lbl_logo.setStyleSheet("background:transparent;")
        pix_logo = QPixmap(LOGO_PATH)
        if not pix_logo.isNull():
            self.lbl_logo.setPixmap(
                pix_logo.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.lbl_logo.setText("LOGO")
            self.lbl_logo.setStyleSheet(f"color:{PINK}; font-weight:bold; background:transparent;")
        lay.addWidget(self.lbl_logo)

        # text block
        txt_lay = QVBoxLayout()
        txt_lay.setSpacing(2)
        lbl_name = QLabel(APP_NAME)
        lbl_name.setStyleSheet(f"color:{PINK}; font-size:12px; font-weight:bold; background:transparent;")
        lbl_ver  = QLabel(f"v{APP_VERSION}  |  {APP_WEB}")
        lbl_ver.setStyleSheet(f"color:{AMBER}; font-size:9px; background:transparent;")
        lbl_auth = QLabel("Parviz Tajdari — Geologist & CCS Researcher")
        lbl_auth.setStyleSheet(f"color:{TXT}; font-size:9px; background:transparent;")
        txt_lay.addWidget(lbl_name)
        txt_lay.addWidget(lbl_ver)
        txt_lay.addWidget(lbl_auth)
        lay.addLayout(txt_lay)
        lay.addStretch()

        # QR code
        self.lbl_qr = QLabel()
        self.lbl_qr.setFixedSize(64, 64)
        self.lbl_qr.setAlignment(Qt.AlignCenter)
        self.lbl_qr.setStyleSheet("background:transparent;")
        pix_qr = QPixmap(QR_PATH)
        if not pix_qr.isNull():
            self.lbl_qr.setPixmap(
                pix_qr.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.lbl_qr.setText("QR")
            self.lbl_qr.setStyleSheet(f"color:{BRD}; background:transparent;")
        lay.addWidget(self.lbl_qr)

# ─────────────────────────────────────────────────────────────
# TAB 1 — SIMULATOR
# ─────────────────────────────────────────────────────────────
class SimulatorTab(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(8)

        # ── LEFT: inputs ──────────────────────────────────────
        left = QWidget()
        left.setFixedWidth(300)
        lv = QVBoxLayout(left)
        lv.setSpacing(6)

        # brand panel
        self.brand = BrandPanel()
        lv.addWidget(self.brand)

        # mineral
        grp_min = QGroupBox("Mineral Phase")
        gm = QVBoxLayout(grp_min)
        self.cb_mineral = QComboBox()
        self.cb_mineral.addItems(list(CarbonationEngine.MINERALS.keys()))
        self.lbl_ref = QLabel("")
        self.lbl_ref.setStyleSheet(f"color:{BRD}; font-size:9px;")
        self.lbl_ref.setWordWrap(True)
        gm.addWidget(self.cb_mineral)
        gm.addWidget(self.lbl_ref)
        self.cb_mineral.currentTextChanged.connect(self._update_ref)
        self._update_ref(self.cb_mineral.currentText())
        lv.addWidget(grp_min)

        # parameters
        grp_par = QGroupBox("Process Parameters")
        gp = QGridLayout(grp_par)
        gp.setSpacing(4)

        def _dspin(lo, hi, val, dec=1, suffix=""):
            w = QDoubleSpinBox()
            w.setRange(lo, hi)
            w.setValue(val)
            w.setDecimals(dec)
            w.setSuffix(suffix)
            return w

        gp.addWidget(QLabel("Temperature (°C):"), 0, 0)
        self.sp_temp = _dspin(25, 300, 150, 1, " °C")
        gp.addWidget(self.sp_temp, 0, 1)

        gp.addWidget(QLabel("Pressure (bar):"), 1, 0)
        self.sp_pres = _dspin(1, 300, 100, 1, " bar")
        gp.addWidget(self.sp_pres, 1, 1)

        gp.addWidget(QLabel("CO₂ Conc. (mol/L):"), 2, 0)
        self.sp_co2 = _dspin(0.01, 5.0, 0.5, 3, " mol/L")
        gp.addWidget(self.sp_co2, 2, 1)

        gp.addWidget(QLabel("Liquid/Solid Ratio:"), 3, 0)
        self.sp_ls = _dspin(1.0, 50.0, 10.0, 1, " L/kg")
        gp.addWidget(self.sp_ls, 3, 1)

        gp.addWidget(QLabel("Duration (hours):"), 4, 0)
        self.sp_dur = _dspin(0.1, 1000.0, 24.0, 1, " h")
        gp.addWidget(self.sp_dur, 4, 1)

        lv.addWidget(grp_par)

        # timer panel
        self.timer_panel = TimerPanel()
        lv.addWidget(self.timer_panel)

        # notes
        grp_n = QGroupBox("Notes")
        gn = QVBoxLayout(grp_n)
        self.txt_notes = QTextEdit()
        self.txt_notes.setFixedHeight(55)
        self.txt_notes.setPlaceholderText("Optional notes for this run…")
        gn.addWidget(self.txt_notes)
        lv.addWidget(grp_n)

        # buttons
        btn_row = QHBoxLayout()
        self.btn_run   = QPushButton("▶  Run Simulation")
        self.btn_run.setObjectName("btn_run")
        self.btn_reset = QPushButton("↺  Reset")
        self.btn_reset.setObjectName("btn_reset")
        self.btn_export = QPushButton("⬇  Export CSV")
        self.btn_export.setObjectName("btn_export")
        btn_row.addWidget(self.btn_run)
        btn_row.addWidget(self.btn_reset)
        btn_row.addWidget(self.btn_export)
        lv.addLayout(btn_row)

        # progress bar
        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.pbar.setFixedHeight(16)
        lv.addWidget(self.pbar)

        lv.addStretch()
        root.addWidget(left)

        # ── RIGHT: plots + results ────────────────────────────
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setSpacing(6)

        # plot area
        self.pw = pg.GraphicsLayoutWidget()
        self.pw.setBackground(BG)
        self.pw.setMinimumHeight(320)

        self.p1 = self.pw.addPlot(row=0, col=0, title="Conversion α(t)")
        self.p1.setLabel("left",   "Conversion (%)")
        self.p1.setLabel("bottom", "Time (h)")
        self.p1.showGrid(x=True, y=True, alpha=0.2)
        self.p1.getAxis("left").setPen(pg.mkPen(TXT))
        self.p1.getAxis("bottom").setPen(pg.mkPen(TXT))
        self.p1.titleLabel.setText(
            "<span style='color:#ff69b4;font-size:11pt;'>Conversion α(t)</span>"
        )

        self.p2 = self.pw.addPlot(row=0, col=1, title="CO₂ Stored (kg/t mineral)")
        self.p2.setLabel("left",   "CO₂ (kg/t)")
        self.p2.setLabel("bottom", "Time (h)")
        self.p2.showGrid(x=True, y=True, alpha=0.2)
        self.p2.getAxis("left").setPen(pg.mkPen(TXT))
        self.p2.getAxis("bottom").setPen(pg.mkPen(TXT))
        self.p2.titleLabel.setText(
            "<span style='color:#ffaa00;font-size:11pt;'>CO₂ Stored (kg/t mineral)</span>"
        )

        rv.addWidget(self.pw)

        # results summary
        grp_res = QGroupBox("Simulation Results")
        gr = QGridLayout(grp_res)
        gr.setSpacing(6)

        def _res_lbl(color=TXT):
            l = QLabel("—")
            l.setStyleSheet(f"color:{color}; font-size:12px; font-weight:bold;")
            l.setAlignment(Qt.AlignCenter)
            return l

        self.res_conv   = _res_lbl(ACCENT)
        self.res_co2    = _res_lbl(AMBER)
        self.res_inject = _res_lbl(BLUE)
        self.res_absorb = _res_lbl(PINK)

        gr.addWidget(QLabel("Final Conversion:"),         0, 0)
        gr.addWidget(self.res_conv,                        0, 1)
        gr.addWidget(QLabel("CO₂ Stored (kg/t):"),        0, 2)
        gr.addWidget(self.res_co2,                         0, 3)
        gr.addWidget(QLabel("Injection Phase (10%):"),    1, 0)
        gr.addWidget(self.res_inject,                      1, 1)
        gr.addWidget(QLabel("Absorption Done (90%):"),    1, 2)
        gr.addWidget(self.res_absorb,                      1, 3)

        rv.addWidget(grp_res)

        # log
        grp_log = QGroupBox("Run Log")
        gl = QVBoxLayout(grp_log)
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setFixedHeight(90)
        gl.addWidget(self.txt_log)
        rv.addWidget(grp_log)

        root.addWidget(right)

        # ── connect signals ───────────────────────────────────
        self.btn_run.clicked.connect(self._run)
        self.btn_reset.clicked.connect(self._reset)
        self.btn_export.clicked.connect(self._export_csv)

    # ── helpers ───────────────────────────────────────────────
    def _update_ref(self, mineral):
        ref = CarbonationEngine.MINERALS.get(mineral, {}).get("ref", "")
        self.lbl_ref.setText(f"Ref: {ref}")

    def _get_params(self):
        return {
            "mineral":      self.cb_mineral.currentText(),
            "temperature":  self.sp_temp.value(),
            "pressure":     self.sp_pres.value(),
            "co2_conc":     self.sp_co2.value(),
            "liquid_ratio": self.sp_ls.value(),
            "duration":     self.sp_dur.value(),
            "notes":        self.txt_notes.toPlainText(),
        }

    def _run(self):
        self.btn_run.setEnabled(False)
        self.pbar.setValue(0)
        params = self._get_params()
        self.worker = SimWorker(params)
        self.worker.progress.connect(self.pbar.setValue)
        self.worker.finished.connect(self._on_finished)
        self.worker.error_sig.connect(self._on_error)
        self.worker.start()

    def _on_finished(self, t_arr, alpha_arr, co2_arr, result):
        self.btn_run.setEnabled(True)
        self.pbar.setValue(100)

        mineral = self.cb_mineral.currentText()
        color   = CarbonationEngine.MINERALS[mineral]["color"]
        pen     = pg.mkPen(color=color, width=2)

        self.p1.clear()
        self.p1.plot(t_arr, alpha_arr, pen=pen)
        # injection / absorption marker lines
        for xval, lc in [(result["inject_time"], AMBER), (result["absorb_time"], BLUE)]:
            line = pg.InfiniteLine(pos=xval, angle=90,
                                   pen=pg.mkPen(color=lc, width=1, style=Qt.DashLine))
            self.p1.addItem(line)

        self.p2.clear()
        self.p2.plot(t_arr, co2_arr, pen=pg.mkPen(color=AMBER, width=2))

        self.res_conv.setText(f"{result['conversion']:.1f} %")
        self.res_co2.setText(f"{result['co2_stored']:.1f}")
        self.res_inject.setText(self.timer_panel._fmt_h(result["inject_time"]))
        self.res_absorb.setText(self.timer_panel._fmt_h(result["absorb_time"]))

        self.timer_panel.update_estimates(result["inject_time"], result["absorb_time"])

        # save to DB
        params = self._get_params()
        params.update(result)
        self.db.save_simulation(params)

        # log
        ts = datetime.now().strftime("%H:%M:%S")
        self.txt_log.append(
            f"[{ts}] {mineral} | T={params['temperature']}°C P={params['pressure']}bar "
            f"→ α={result['conversion']:.1f}% CO₂={result['co2_stored']:.1f}kg/t "
            f"| inject≈{self.timer_panel._fmt_h(result['inject_time'])} "
            f"absorb≈{self.timer_panel._fmt_h(result['absorb_time'])}"
        )

    def _on_error(self, msg):
        self.btn_run.setEnabled(True)
        QMessageBox.critical(self, "Simulation Error", msg)

    def _reset(self):
        self.p1.clear()
        self.p2.clear()
        self.res_conv.setText("—")
        self.res_co2.setText("—")
        self.res_inject.setText("—")
        self.res_absorb.setText("—")
        self.pbar.setValue(0)
        self.txt_log.clear()
        self.timer_panel._reset_timer()

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "simulation.csv",
                                               "CSV Files (*.csv)")
        if not path:
            return
        rows = self.db.get_all_simulations()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID","Timestamp","Mineral","Temp°C","P_bar","CO2_mol_L",
                         "L_S","Duration_h","Conv_%","CO2_kg_t","Inject_h","Absorb_h","Notes"])
            w.writerows(rows)
        QMessageBox.information(self, "Exported", f"Saved to:\n{path}")

# ─────────────────────────────────────────────────────────────
# TAB 2 — RECORDS
# ─────────────────────────────────────────────────────────────
class RecordsTab(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 8)

        btn_row = QHBoxLayout()
        self.btn_refresh = QPushButton("↻  Refresh")
        self.btn_del     = QPushButton("🗑  Delete Selected")
        self.btn_del.setObjectName("btn_reset")
        btn_row.addWidget(self.btn_refresh)
        btn_row.addWidget(self.btn_del)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "ID","Timestamp","Mineral","T°C","P bar","CO₂ mol/L",
            "L/S","Dur h","Conv %","CO₂ kg/t","Inject h","Absorb h","Notes"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.table)

        self.btn_refresh.clicked.connect(self.load)
        self.btn_del.clicked.connect(self._delete_selected)
        self.load()

    def load(self):
        rows = self.db.get_all_simulations()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val) if val is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, c, item)

    def _delete_selected(self):
        sel = self.table.selectedItems()
        if not sel:
            return
        row = self.table.currentRow()
        rec_id = self.table.item(row, 0).text()
        if QMessageBox.question(self, "Delete", f"Delete record ID {rec_id}?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.conn.execute("DELETE FROM simulations WHERE id=?", (rec_id,))
            self.db.conn.commit()
            self.load()

# ─────────────────────────────────────────────────────────────
# TAB 3 — MANUAL DATA
# ─────────────────────────────────────────────────────────────
class ManualDataTab(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(6)

        grp = QGroupBox("Add Lab Data Point")
        gg  = QGridLayout(grp)
        gg.setSpacing(6)

        gg.addWidget(QLabel("Label / Sample:"), 0, 0)
        self.inp_label = QLineEdit()
        self.inp_label.setPlaceholderText("e.g. Lab_Run_001")
        gg.addWidget(self.inp_label, 0, 1)

        gg.addWidget(QLabel("Time (h):"), 1, 0)
        self.sp_time = QDoubleSpinBox()
        self.sp_time.setRange(0, 10000)
        self.sp_time.setValue(1.0)
        gg.addWidget(self.sp_time, 1, 1)

        gg.addWidget(QLabel("Conversion (%):"), 2, 0)
        self.sp_conv = QDoubleSpinBox()
        self.sp_conv.setRange(0, 100)
        self.sp_conv.setValue(10.0)
        gg.addWidget(self.sp_conv, 2, 1)

        gg.addWidget(QLabel("CO₂ (kg/t):"), 3, 0)
        self.sp_co2 = QDoubleSpinBox()
        self.sp_co2.setRange(0, 2000)
        self.sp_co2.setValue(50.0)
        gg.addWidget(self.sp_co2, 3, 1)

        self.btn_add = QPushButton("➕  Add Record")
        self.btn_add.setObjectName("btn_run")
        gg.addWidget(self.btn_add, 4, 0, 1, 2)
        lay.addWidget(grp)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID","Timestamp","Label","Time h","Conv %","CO₂ kg/t"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.table)

        self.btn_add.clicked.connect(self._add)
        self._load()

    def _add(self):
        self.db.save_manual(
            self.inp_label.text() or "—",
            self.sp_time.value(),
            self.sp_conv.value(),
            self.sp_co2.value()
        )
        self._load()

    def _load(self):
        rows = self.db.get_manual_data()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val) if val is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, c, item)

# ─────────────────────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db      = Database()
        self._use_3d = False
        self._apply_theme()
        self.setWindowTitle(f"{APP_NAME}  v{APP_VERSION}  |  {APP_WEB}")
        self.setMinimumSize(1100, 720)

        # taskbar icon
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                f"AIBrothersTools.MineralCarbonation.{APP_VERSION}"
            )
        except Exception:
            pass
        icon = QIcon(ICO_PATH)
        if not icon.isNull():
            self.setWindowIcon(icon)
            QApplication.setWindowIcon(icon)

        # top bar
        top = QWidget()
        top.setFixedHeight(36)
        top.setStyleSheet(f"background:{DARK2}; border-bottom:1px solid {BRD};")
        tl = QHBoxLayout(top)
        tl.setContentsMargins(10, 0, 10, 0)
        lbl_title = QLabel(f"  {APP_NAME}   v{APP_VERSION}")
        lbl_title.setStyleSheet(f"color:{PINK}; font-size:12px; font-weight:bold;")
        lbl_wm    = QLabel(WATERMARK)
        lbl_wm.setStyleSheet(f"color:{BRD}; font-size:9px;")

        # 3D checkbox
        self.chk_3d = QCheckBox("3D UI + Larger Font")
        self.chk_3d.setStyleSheet(f"color:{AMBER}; font-size:10px;")
        self.chk_3d.stateChanged.connect(self._toggle_3d)

        tl.addWidget(lbl_title)
        tl.addStretch()
        tl.addWidget(self.chk_3d)
        tl.addSpacing(20)
        tl.addWidget(lbl_wm)

        # central
        central = QWidget()
        cv = QVBoxLayout(central)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(0)
        cv.addWidget(top)

        self.tabs = QTabWidget()
        self.tab_sim     = SimulatorTab(self.db)
        self.tab_records = RecordsTab(self.db)
        self.tab_manual  = ManualDataTab(self.db)
        self.tabs.addTab(self.tab_sim,     "⚗  Simulator")
        self.tabs.addTab(self.tab_records, "📋  Records")
        self.tabs.addTab(self.tab_manual,  "🔬  Manual Data")
        cv.addWidget(self.tabs)

        self.setCentralWidget(central)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage(
            f"{APP_NAME} v{APP_VERSION}  |  {APP_ORG}  |  {APP_WEB}  |  {WATERMARK}"
        )

    def _apply_theme(self):
        style = STYLE_CLASSIC
        if self._use_3d:
            style += STYLE_3D_AD
        QApplication.instance().setStyleSheet(style)

    def _toggle_3d(self, state):
        self._use_3d = (state == Qt.Checked)
        self._apply_theme()

# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(APP_ORG)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

# End of mineral_carbonation_sim.py
if __name__ == "__main__":
    main()
