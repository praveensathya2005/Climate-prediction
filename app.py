import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
import streamlit.components.v1 as components
from sms import send_sms

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Climate Prediction & Alert System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CUSTOM CSS – ULTRA PREMIUM DESIGN
# ===============================

st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #0a0f1c;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-purple: #8b5cf6;
    --accent-green: #10b981;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
}

/* ── Global Styles ── */
.stApp {
    background: linear-gradient(135deg, #0a0f1c 0%, #1a1040 30%, #0f172a 60%, #0c1426 100%) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Hide default elements ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Animated Particle Background ── */
.particles {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.particle {
    position: absolute;
    width: 3px; height: 3px;
    background: rgba(139, 92, 246, 0.4);
    border-radius: 50%;
    animation: particleFloat linear infinite;
}
@keyframes particleFloat {
    0% { transform: translateY(100vh) translateX(0); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(-10vh) translateX(50px); opacity: 0; }
}

/* Animated background orbs */
.stApp::before {
    content: '';
    position: fixed;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background:
        radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 50%);
    animation: orbFloat 20s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    33% { transform: translate(30px, -30px) rotate(120deg); }
    66% { transform: translate(-20px, 20px) rotate(240deg); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(25px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes barGrow {
    from { width: 0%; }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes typewriter {
    from { width: 0; }
    to { width: 100%; }
}
@keyframes blink {
    50% { border-color: transparent; }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.1); }
    50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.3); }
}

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] .stMarkdown label {
    color: #e2e8f0 !important;
}

/* ── Navigation Styling ── */
section[data-testid="stSidebar"] .stRadio > label {
    color: #94a3b8 !important;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}
section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.3rem;
}
section[data-testid="stSidebar"] .stRadio > div > label {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    padding: 0.7rem 1rem !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(139, 92, 246, 0.08) !important;
    border-color: rgba(139, 92, 246, 0.2) !important;
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
section[data-testid="stSidebar"] .stRadio > div [data-testid="stMarkdownContainer"] {
    color: #e2e8f0 !important;
}

/* ── Hero Header ── */
.hero-section {
    text-align: center;
    padding: 2.5rem 1rem 1rem 1rem;
    margin-bottom: 1rem;
    animation: fadeInUp 0.8s ease-out;
    position: relative;
}
.hero-section::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #8b5cf6, transparent);
}
.hero-icon {
    font-size: 4rem;
    margin-bottom: 0.5rem;
    animation: float 3s ease-in-out infinite;
    display: inline-block;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4, #3b82f6);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s ease-in-out infinite;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}
.hero-subtitle {
    font-size: 1rem;
    color: #64748b;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.hero-badges {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    margin-top: 1.2rem;
    flex-wrap: wrap;
}
.hero-badge {
    padding: 0.35rem 1rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    animation: fadeInUp 1s ease-out;
}
.badge-ai { background: rgba(139, 92, 246, 0.15); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3); }
.badge-rt { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-sms { background: rgba(59, 130, 246, 0.15); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3); }

/* ── How It Works Steps ── */
.steps-container {
    display: flex;
    justify-content: center;
    gap: 0;
    margin: 1.5rem 0;
    animation: fadeInUp 0.9s ease-out;
    flex-wrap: wrap;
}
.step-item {
    text-align: center;
    position: relative;
    flex: 1;
    min-width: 120px;
    padding: 1rem 0.5rem;
}
.step-item:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 28px;
    right: -5%;
    width: 60%;
    height: 2px;
    background: linear-gradient(90deg, #8b5cf6, rgba(139, 92, 246, 0.2));
}
.step-circle {
    width: 44px; height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.6rem auto;
    font-size: 1.2rem;
    font-weight: 700;
    position: relative;
    z-index: 1;
}
.step-circle.active {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    color: white;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
}
.step-circle.inactive {
    background: rgba(255, 255, 255, 0.05);
    color: #64748b;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.step-text {
    font-size: 0.72rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Glass Card ── */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.6s ease-out;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
}
.glass-card:hover {
    border-color: rgba(139, 92, 246, 0.15);
    transform: translateY(-2px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* ── Section Title ── */
.section-title {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
    animation: fadeInLeft 0.6s ease-out;
}
.section-title .icon-box {
    width: 42px; height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
}
.section-title h3 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
}
.section-title p {
    margin: 0;
    font-size: 0.78rem;
    color: #64748b;
}

/* ── Metric Cards ── */
.metric-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.5rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.6s ease-out;
}
.metric-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}
.metric-card .metric-icon { font-size: 2rem; margin-bottom: 0.4rem; }
.metric-card .metric-label {
    font-size: 0.7rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 0.2rem; font-weight: 600;
}
.metric-card .metric-value {
    font-size: 1.6rem; font-weight: 800; color: #f1f5f9;
    font-family: 'Orbitron', monospace;
}
.metric-card .metric-bar {
    height: 4px; border-radius: 2px;
    margin-top: 0.8rem;
    background: rgba(255,255,255,0.05);
    overflow: hidden;
}
.metric-card .metric-bar-fill {
    height: 100%; border-radius: 2px;
    animation: barGrow 1.5s ease-out;
}
.metric-card.temp { border-top: 3px solid #ef4444; }
.metric-card.temp .metric-value { color: #ef4444; }
.metric-card.temp .metric-bar-fill { background: linear-gradient(90deg, #ef4444, #f97316); }
.metric-card.rain { border-top: 3px solid #3b82f6; }
.metric-card.rain .metric-value { color: #3b82f6; }
.metric-card.rain .metric-bar-fill { background: linear-gradient(90deg, #3b82f6, #06b6d4); }
.metric-card.humid { border-top: 3px solid #06b6d4; }
.metric-card.humid .metric-value { color: #06b6d4; }
.metric-card.humid .metric-bar-fill { background: linear-gradient(90deg, #06b6d4, #8b5cf6); }
.metric-card.wind { border-top: 3px solid #10b981; }
.metric-card.wind .metric-value { color: #10b981; }
.metric-card.wind .metric-bar-fill { background: linear-gradient(90deg, #10b981, #3b82f6); }

/* ── Result Cards ── */
.result-card {
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin: 1rem 0;
    animation: fadeInUp 0.7s ease-out;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; right: -100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, currentColor, transparent);
    animation: shimmer 3s linear infinite;
    background-size: 200% 100%;
}
.result-card .result-icon {
    font-size: 3.5rem;
    margin-bottom: 0.8rem;
    animation: pulse 2s ease-in-out infinite;
}
.result-card h2 { font-size: 1.6rem; font-weight: 800; margin-bottom: 0.3rem; }
.result-card p { font-size: 0.95rem; opacity: 0.85; }
.result-severe {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.12), rgba(185, 28, 28, 0.08));
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #fca5a5;
    animation: fadeInUp 0.7s ease-out, pulseGlow 2s ease-in-out infinite;
}
.result-high {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(217, 119, 6, 0.08));
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #fcd34d;
}
.result-alert {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(37, 99, 235, 0.08));
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #93c5fd;
}
.result-normal {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(5, 150, 105, 0.08));
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #6ee7b7;
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.1); }
    50% { box-shadow: 0 0 40px rgba(239, 68, 68, 0.25); }
}

/* ── Risk Level Stepper ── */
.risk-stepper {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 1.5rem 0;
    animation: fadeInUp 0.8s ease-out;
}
.risk-step {
    text-align: center;
    position: relative;
    flex: 1;
}
.risk-step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px; right: 0;
    width: 100%; height: 3px;
    z-index: 0;
}
.risk-dot {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.4rem auto;
    font-size: 1rem;
    position: relative;
    z-index: 1;
    transition: all 0.3s ease;
}
.risk-dot.active {
    transform: scale(1.3);
    box-shadow: 0 0 25px currentColor;
}
.risk-dot.inactive {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    opacity: 0.4;
}
.risk-step-label {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Probability Bar Chart ── */
.prob-chart { padding: 0.5rem 0; }
.prob-bar-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.7rem;
    gap: 0.8rem;
}
.prob-bar-label {
    width: 80px;
    font-size: 0.78rem;
    color: #94a3b8;
    text-align: right;
    font-weight: 500;
}
.prob-bar-track {
    flex: 1;
    height: 24px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    overflow: hidden;
    position: relative;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 12px;
    display: flex;
    align-items: center;
    padding: 0 10px;
    font-size: 0.7rem;
    font-weight: 600;
    color: white;
    transition: width 1s ease-out;
    animation: barGrow 1.2s ease-out;
    position: relative;
    overflow: hidden;
}
.prob-bar-fill::after {
    content: '';
    position: absolute;
    top: 0; left: -200%;
    width: 200%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    animation: shimmer 3s ease-in-out infinite;
}
.prob-bar-fill.green { background: linear-gradient(90deg, #059669, #10b981); }
.prob-bar-fill.blue { background: linear-gradient(90deg, #2563eb, #3b82f6); }
.prob-bar-fill.amber { background: linear-gradient(90deg, #d97706, #f59e0b); }
.prob-bar-fill.red { background: linear-gradient(90deg, #dc2626, #ef4444); }
.prob-bar-value {
    width: 55px; font-size: 0.85rem;
    color: #e2e8f0; font-weight: 700; text-align: left;
    font-family: 'Orbitron', monospace;
}

/* ── Confidence Gauge ── */
.gauge-container { text-align: center; padding: 1rem; animation: fadeInUp 0.8s ease-out; }
.gauge-ring {
    width: 180px; height: 180px;
    border-radius: 50%;
    margin: 0 auto 1rem auto;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: glowPulse 3s ease-in-out infinite;
}
.gauge-inner {
    width: 140px; height: 140px;
    border-radius: 50%;
    background: #0f172a;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1;
}
.gauge-value {
    font-size: 2rem; font-weight: 900;
    font-family: 'Orbitron', monospace;
}
.gauge-label {
    font-size: 0.7rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 1.5px;
}

/* ── Safety Tips ── */
.tips-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.tip-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.2rem;
    transition: all 0.3s ease;
    animation: fadeInUp 0.7s ease-out;
}
.tip-card:hover {
    transform: translateY(-3px);
    border-color: rgba(139, 92, 246, 0.2);
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}
.tip-card .tip-icon { font-size: 1.6rem; margin-bottom: 0.5rem; }
.tip-card .tip-title {
    font-size: 0.85rem; font-weight: 700;
    color: #e2e8f0; margin-bottom: 0.3rem;
}
.tip-card .tip-desc {
    font-size: 0.75rem; color: #64748b; line-height: 1.4;
}

/* ── Stats Row ── */
.stats-row {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
    animation: fadeInUp 0.7s ease-out;
}
.stat-item { text-align: center; }
.stat-number {
    font-size: 1.8rem; font-weight: 900;
    font-family: 'Orbitron', monospace;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label {
    font-size: 0.7rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 1px;
    margin-top: 0.2rem;
}

/* ── Celebration Animation ── */
.climate-celebration {
    position: relative;
    padding: 2rem;
    text-align: center;
    overflow: hidden;
    border-radius: 20px;
    margin: 1rem 0;
}
.climate-celebration .symbols-rain {
    position: absolute;
    top: -20px; left: 0; right: 0;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
}
.floating-symbol {
    position: absolute;
    top: -40px;
    font-size: 1.8rem;
    animation: floatDown 3s ease-in forwards;
    opacity: 0;
}
@keyframes floatDown {
    0% { transform: translateY(0) rotate(0deg); opacity: 0; }
    10% { opacity: 1; }
    100% { transform: translateY(350px) rotate(360deg); opacity: 0; }
}
.celebration-text { position: relative; z-index: 2; }
.celebration-text h3 { font-size: 1.4rem; font-weight: 700; margin-bottom: 0.5rem; }
.celebration-text p { font-size: 0.9rem; opacity: 0.8; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 2.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 25px rgba(59, 130, 246, 0.35) !important;
    width: 100% !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 35px rgba(59, 130, 246, 0.55) !important;
}

/* ── Input Fields ── */
.stNumberInput > div > div > input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.3s ease !important;
}
.stNumberInput > div > div > input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
}

/* ── Dividers ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.4), transparent);
    margin: 2rem 0;
    border: none;
}
.fancy-divider-thick {
    height: 2px;
    background: linear-gradient(90deg, transparent, #3b82f6, #8b5cf6, #06b6d4, transparent);
    margin: 2rem 0;
    border: none;
    border-radius: 1px;
}

/* ── Labels ── */
.stMarkdown label, .stNumberInput label, p, span, h1, h2, h3, h4, h5, h6 {
    color: #e2e8f0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0f1c; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #3b82f6, #8b5cf6); border-radius: 3px; }

/* ── Alerts ── */
.stAlert { border-radius: 12px !important; border: none !important; }

/* ── Sidebar Components ── */
.sidebar-info {
    background: rgba(59, 130, 246, 0.06);
    border: 1px solid rgba(59, 130, 246, 0.15);
    border-radius: 14px;
    padding: 1rem;
    margin: 0.5rem 0;
}
.history-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 0.8rem;
    margin-bottom: 0.5rem;
    transition: all 0.3s ease;
}
.history-item:hover {
    border-color: rgba(139, 92, 246, 0.2);
    background: rgba(255, 255, 255, 0.05);
}
.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.badge-active {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 1.5rem 0;
    color: #334155;
    font-size: 0.8rem;
    position: relative;
}
.footer-inner {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 20px;
    padding: 2rem;
}
.footer-brand {
    font-size: 1.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.footer-links {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin: 0.8rem 0;
    flex-wrap: wrap;
}
.footer-links span {
    color: #475569;
    font-size: 0.75rem;
    cursor: default;
    transition: color 0.3s ease;
}
.footer-links span:hover { color: #8b5cf6; }
.footer-tech {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 0.8rem;
    flex-wrap: wrap;
}
.tech-badge {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 0.2rem 0.6rem;
    font-size: 0.65rem;
    color: #475569;
}

/* ── Feature Cards ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.2rem;
    margin: 1.5rem 0;
}
.feature-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.7s ease-out;
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 18px 18px 0 0;
}
.feature-card:hover {
    transform: translateY(-6px);
    border-color: rgba(139, 92, 246, 0.25);
    box-shadow: 0 15px 50px rgba(0,0,0,0.3);
}
.feature-card .f-icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
    display: inline-block;
    animation: float 4s ease-in-out infinite;
}
.feature-card .f-title {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.4rem;
}
.feature-card .f-desc {
    font-size: 0.8rem;
    color: #64748b;
    line-height: 1.5;
}

</style>
""", unsafe_allow_html=True)

# ── Particle background ──
particles_html = '<div class="particles">'
for i in range(25):
    left = (i * 4.1) % 100
    size = 2 + (i % 3)
    duration = 8 + (i % 7)
    delay = (i * 0.5) % 6
    color = ["rgba(139,92,246,0.3)", "rgba(59,130,246,0.3)", "rgba(6,182,212,0.3)"][i % 3]
    particles_html += f'<div class="particle" style="left:{left}%;width:{size}px;height:{size}px;background:{color};animation-duration:{duration}s;animation-delay:{delay}s;"></div>'
particles_html += '</div>'
st.markdown(particles_html, unsafe_allow_html=True)

# ===============================
# LOAD MODEL
# ===============================

@st.cache_resource
def load_all():
    import tensorflow as tf
    from keras.src.layers.rnn.lstm import LSTM as KerasLSTM

    # Patch LSTM.from_config to strip 'time_major' (saved by Keras 2.x but rejected by Keras 3.x)
    _original_from_config = KerasLSTM.from_config.__func__

    @classmethod
    def _patched_from_config(cls, config):
        config.pop('time_major', None)
        return _original_from_config(cls, config)

    KerasLSTM.from_config = _patched_from_config

    model = tf.keras.models.load_model("climate_model.h5", compile=False)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Restore original from_config
    KerasLSTM.from_config = _original_from_config

    scaler = joblib.load("scaler.pkl")
    return model, scaler

model, scaler = load_all()

# ===============================
# INITIALIZE SESSION STATE
# ===============================

if "final_risk" not in st.session_state:
    st.session_state.final_risk = None
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []
if "prediction_probs" not in st.session_state:
    st.session_state.prediction_probs = None
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = None


# ===============================
# 3D ROTATING GLOBE COMPONENT
# ===============================

def render_globe(height=500):
    """Render a 3D rotating globe using Three.js"""
    globe_html = """
    <div id="globe-container" style="width:100%; height:""" + str(height) + """px; position:relative; border-radius:20px; overflow:hidden; background: radial-gradient(ellipse at center, #0a0f2e 0%, #050816 100%);">
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function() {
        const container = document.getElementById('globe-container');
        if (!container) return;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 3.2;
        camera.position.y = 0.3;
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setClearColor(0x000000, 0);
        container.appendChild(renderer.domElement);

        // Master group for globe elements – tilted like Earth's axis
        const globeGroup = new THREE.Group();
        globeGroup.rotation.z = 0.41; // 23.5 degree Earth tilt
        scene.add(globeGroup);

        // ── Stars (dense + colorful) ──
        const starsGeometry = new THREE.BufferGeometry();
        const starPositions = [];
        const starColors = [];
        for (let i = 0; i < 5000; i++) {
            starPositions.push(
                (Math.random() - 0.5) * 120,
                (Math.random() - 0.5) * 120,
                (Math.random() - 0.5) * 120
            );
            const c = new THREE.Color();
            c.setHSL(0.5 + Math.random() * 0.3, 0.3 + Math.random() * 0.4, 0.7 + Math.random() * 0.3);
            starColors.push(c.r, c.g, c.b);
        }
        starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starPositions, 3));
        starsGeometry.setAttribute('color', new THREE.Float32BufferAttribute(starColors, 3));
        const starsMaterial = new THREE.PointsMaterial({ size: 0.09, transparent: true, opacity: 0.9, vertexColors: true });
        const stars = new THREE.Points(starsGeometry, starsMaterial);
        scene.add(stars);

        // ── Outer wireframe (cyan/blue with higher detail) ──
        const outerWireGeom = new THREE.SphereGeometry(1.005, 64, 64);
        const outerWireMat = new THREE.MeshBasicMaterial({
            color: 0x06b6d4, wireframe: true, transparent: true, opacity: 0.07
        });
        const outerWire = new THREE.Mesh(outerWireGeom, outerWireMat);
        globeGroup.add(outerWire);

        // ── Inner wireframe (purple, coarser) ──
        const innerWireGeom = new THREE.SphereGeometry(0.995, 24, 24);
        const innerWireMat = new THREE.MeshBasicMaterial({
            color: 0x8b5cf6, wireframe: true, transparent: true, opacity: 0.06
        });
        const innerWire = new THREE.Mesh(innerWireGeom, innerWireMat);
        globeGroup.add(innerWire);

        // ── Icosahedron hex grid overlay ──
        const hexGeom = new THREE.IcosahedronGeometry(1.003, 3);
        const hexMat = new THREE.MeshBasicMaterial({
            color: 0x3b82f6, wireframe: true, transparent: true, opacity: 0.1
        });
        const hexGrid = new THREE.Mesh(hexGeom, hexMat);
        globeGroup.add(hexGrid);

        // ── Solid inner core ──
        const coreGeom = new THREE.SphereGeometry(0.96, 48, 48);
        const coreMat = new THREE.MeshBasicMaterial({
            color: 0x0f172a, transparent: true, opacity: 0.6
        });
        const core = new THREE.Mesh(coreGeom, coreMat);
        globeGroup.add(core);

        // ── Inner energy core (small glowing sphere) ──
        const energyCoreGeom = new THREE.SphereGeometry(0.15, 32, 32);
        const energyCoreMat = new THREE.MeshBasicMaterial({
            color: 0x8b5cf6, transparent: true, opacity: 0.2
        });
        const energyCore = new THREE.Mesh(energyCoreGeom, energyCoreMat);
        globeGroup.add(energyCore);

        // ── Outer atmosphere glow (3 layers) ──
        const atmoLayers = [];
        const atmoConfigs = [
            { r: 1.06, color: 0x3b82f6, op: 0.05 },
            { r: 1.12, color: 0x8b5cf6, op: 0.03 },
            { r: 1.2,  color: 0x06b6d4, op: 0.02 }
        ];
        atmoConfigs.forEach(cfg => {
            const g = new THREE.SphereGeometry(cfg.r, 48, 48);
            const m = new THREE.MeshBasicMaterial({
                color: cfg.color, transparent: true, opacity: cfg.op, side: THREE.BackSide
            });
            const mesh = new THREE.Mesh(g, m);
            atmoLayers.push(mesh);
            scene.add(mesh);
        });

        // ── Latitude lines (colored by zone) ──
        const latGroup = new THREE.Group();
        for (let lat = -75; lat <= 75; lat += 15) {
            const phi = (90 - lat) * Math.PI / 180;
            const radius = Math.sin(phi);
            const y = Math.cos(phi);
            const curve = new THREE.EllipseCurve(0, 0, radius, radius, 0, 2 * Math.PI, false, 0);
            const points = curve.getPoints(120);
            const pts3d = points.map(p => new THREE.Vector3(p.x, y, p.y));
            const lineGeom = new THREE.BufferGeometry().setFromPoints(pts3d);
            // Color by climate zone
            let lineColor = 0x10b981; // tropical green
            if (Math.abs(lat) > 60) lineColor = 0x06b6d4; // polar cyan
            else if (Math.abs(lat) > 30) lineColor = 0x3b82f6; // temperate blue
            const op = (lat % 30 === 0) ? 0.3 : 0.1;
            const lineMat = new THREE.LineBasicMaterial({ color: lineColor, transparent: true, opacity: op });
            latGroup.add(new THREE.Line(lineGeom, lineMat));
        }
        globeGroup.add(latGroup);

        // ── Longitude lines (gradient colored) ──
        const lonGroup = new THREE.Group();
        for (let lon = 0; lon < 360; lon += 12) {
            const points = [];
            for (let i = 0; i <= 140; i++) {
                const phi = (i / 140) * Math.PI;
                const theta = lon * Math.PI / 180;
                points.push(new THREE.Vector3(
                    Math.sin(phi) * Math.cos(theta),
                    Math.cos(phi),
                    Math.sin(phi) * Math.sin(theta)
                ));
            }
            const lineGeom = new THREE.BufferGeometry().setFromPoints(points);
            const hue = (lon / 360);
            const c = new THREE.Color().setHSL(0.55 + hue * 0.15, 0.6, 0.5);
            const op = (lon % 30 === 0) ? 0.18 : 0.05;
            const lineMat = new THREE.LineBasicMaterial({ color: c, transparent: true, opacity: op });
            lonGroup.add(new THREE.Line(lineGeom, lineMat));
        }
        globeGroup.add(lonGroup);

        // ── Glowing hotspot dots ──
        const dotGroup = new THREE.Group();
        const dotColors = [0x3b82f6, 0x8b5cf6, 0x06b6d4, 0xef4444, 0xf59e0b, 0x10b981];
        for (let i = 0; i < 100; i++) {
            const phi = Math.random() * Math.PI;
            const theta = Math.random() * 2 * Math.PI;
            const r = 1.008;
            const x = r * Math.sin(phi) * Math.cos(theta);
            const y = r * Math.cos(phi);
            const z = r * Math.sin(phi) * Math.sin(theta);
            const dotGeom = new THREE.SphereGeometry(0.01 + Math.random() * 0.008, 8, 8);
            const dotMat = new THREE.MeshBasicMaterial({
                color: dotColors[i % dotColors.length], transparent: true, opacity: 0.9
            });
            const dot = new THREE.Mesh(dotGeom, dotMat);
            dot.position.set(x, y, z);
            dotGroup.add(dot);
        }
        globeGroup.add(dotGroup);

        // ── Connection arcs ──
        const arcGroup = new THREE.Group();
        const arcColors = [0x3b82f6, 0x8b5cf6, 0x06b6d4, 0x10b981, 0xf59e0b, 0xef4444];
        for (let a = 0; a < 15; a++) {
            const phi1 = Math.random() * Math.PI;
            const theta1 = Math.random() * 2 * Math.PI;
            const phi2 = Math.random() * Math.PI;
            const theta2 = Math.random() * 2 * Math.PI;
            const p1 = new THREE.Vector3(
                Math.sin(phi1) * Math.cos(theta1),
                Math.cos(phi1),
                Math.sin(phi1) * Math.sin(theta1)
            );
            const p2 = new THREE.Vector3(
                Math.sin(phi2) * Math.cos(theta2),
                Math.cos(phi2),
                Math.sin(phi2) * Math.sin(theta2)
            );
            const mid = p1.clone().add(p2).multiplyScalar(0.5).normalize().multiplyScalar(1.35 + Math.random() * 0.35);
            const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
            const pts = curve.getPoints(50);
            const lineGeom = new THREE.BufferGeometry().setFromPoints(pts);
            const lineMat = new THREE.LineBasicMaterial({
                color: arcColors[a % arcColors.length], transparent: true, opacity: 0.3
            });
            const line = new THREE.Line(lineGeom, lineMat);
            line.userData = { phase: Math.random() * Math.PI * 2 };
            arcGroup.add(line);
        }
        globeGroup.add(arcGroup);

        // ── Orbiting satellites ──
        const satGroup = new THREE.Group();
        for (let s = 0; s < 4; s++) {
            const satGeom = new THREE.OctahedronGeometry(0.018, 0);
            const satColor = [0x06b6d4, 0xf59e0b, 0x10b981, 0xef4444][s];
            const satMat = new THREE.MeshBasicMaterial({
                color: satColor, transparent: true, opacity: 0.9
            });
            const sat = new THREE.Mesh(satGeom, satMat);
            sat.userData = {
                orbitRadius: 1.25 + s * 0.12,
                speed: 0.006 + s * 0.003,
                tilt: (s * 35 + 15) * Math.PI / 180,
                phase: s * Math.PI / 2
            };
            satGroup.add(sat);

            // Orbit path
            const orbitPts = [];
            for (let i = 0; i <= 150; i++) {
                const angle = (i / 150) * Math.PI * 2;
                const r = sat.userData.orbitRadius;
                orbitPts.push(new THREE.Vector3(
                    r * Math.cos(angle),
                    r * Math.sin(angle) * Math.sin(sat.userData.tilt),
                    r * Math.sin(angle) * Math.cos(sat.userData.tilt)
                ));
            }
            const orbitGeom = new THREE.BufferGeometry().setFromPoints(orbitPts);
            const orbitMat = new THREE.LineBasicMaterial({
                color: satColor, transparent: true, opacity: 0.05
            });
            satGroup.add(new THREE.Line(orbitGeom, orbitMat));
        }
        scene.add(satGroup);

        // ── Cloud wisps ──
        const cloudGroup = new THREE.Group();
        for (let c = 0; c < 30; c++) {
            const phi = Math.random() * Math.PI;
            const theta = Math.random() * 2 * Math.PI;
            const r = 1.03 + Math.random() * 0.025;
            const cloudGeom = new THREE.PlaneGeometry(0.06 + Math.random() * 0.08, 0.02 + Math.random() * 0.025);
            const cloudMat = new THREE.MeshBasicMaterial({
                color: 0xffffff, transparent: true, opacity: 0.06 + Math.random() * 0.06,
                side: THREE.DoubleSide
            });
            const cloud = new THREE.Mesh(cloudGeom, cloudMat);
            cloud.position.set(
                r * Math.sin(phi) * Math.cos(theta),
                r * Math.cos(phi),
                r * Math.sin(phi) * Math.sin(theta)
            );
            cloud.lookAt(0, 0, 0);
            cloudGroup.add(cloud);
        }
        globeGroup.add(cloudGroup);

        // ── Energy pulse rings (expand outward) ──
        const pulseRings = [];
        for (let p = 0; p < 3; p++) {
            const pGeom = new THREE.RingGeometry(0.98, 1.0, 80);
            const pMat = new THREE.MeshBasicMaterial({
                color: [0x3b82f6, 0x8b5cf6, 0x06b6d4][p],
                transparent: true, opacity: 0, side: THREE.DoubleSide
            });
            const pMesh = new THREE.Mesh(pGeom, pMat);
            pMesh.rotation.x = Math.PI / 2;
            pMesh.userData = { phase: p * 2.1, speed: 0.015 + p * 0.005 };
            pulseRings.push(pMesh);
            globeGroup.add(pMesh);
        }

        // ── Multiple orbit rings ──
        const ringColors = [0x8b5cf6, 0x3b82f6, 0x06b6d4];
        const rings = [];
        for (let r = 0; r < 3; r++) {
            const ringGeom = new THREE.RingGeometry(1.06 + r * 0.09, 1.08 + r * 0.09, 100);
            const ringMat = new THREE.MeshBasicMaterial({
                color: ringColors[r], transparent: true, opacity: 0.05 - r * 0.012, side: THREE.DoubleSide
            });
            const ring = new THREE.Mesh(ringGeom, ringMat);
            rings.push(ring);
            scene.add(ring);
        }

        // ── Data stream particles rising from surface ──
        const dataParticles = new THREE.Group();
        for (let d = 0; d < 40; d++) {
            const dGeom = new THREE.SphereGeometry(0.005, 4, 4);
            const dMat = new THREE.MeshBasicMaterial({
                color: [0x3b82f6, 0x8b5cf6, 0x06b6d4, 0x10b981][d % 4],
                transparent: true, opacity: 0.7
            });
            const dMesh = new THREE.Mesh(dGeom, dMat);
            dMesh.userData = {
                basePhi: Math.random() * Math.PI,
                baseTheta: Math.random() * 2 * Math.PI,
                height: Math.random(),
                speed: 0.003 + Math.random() * 0.005
            };
            dataParticles.add(dMesh);
        }
        globeGroup.add(dataParticles);

        // ── Holographic scan disc ──
        const scanGeom = new THREE.RingGeometry(0, 1.015, 80);
        const scanMat = new THREE.MeshBasicMaterial({
            color: 0x06b6d4, transparent: true, opacity: 0.04, side: THREE.DoubleSide
        });
        const scanLine = new THREE.Mesh(scanGeom, scanMat);
        globeGroup.add(scanLine);

        // ── Lighting ──
        scene.add(new THREE.AmbientLight(0xffffff, 0.5));
        const pointLight = new THREE.PointLight(0x3b82f6, 0.3, 10);
        pointLight.position.set(2, 2, 3);
        scene.add(pointLight);

        // ── Mouse interaction ──
        let mouseX = 0, mouseY = 0;

        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();
            mouseX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
            mouseY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
        });

        // ── Animation loop ──
        let time = 0;
        let baseRotY = 0;
        function animate() {
            requestAnimationFrame(animate);
            time += 0.016;
            const now = Date.now();

            // HORIZONTAL rotation only (around Y axis)
            baseRotY += 0.004;
            globeGroup.rotation.y = baseRotY + mouseX * 0.3;

            // Atmosphere glow breathe
            atmoLayers.forEach((atmo, i) => {
                const breathe = 1 + 0.02 * Math.sin(now * 0.0008 + i * 0.8);
                atmo.scale.set(breathe, breathe, breathe);
            });

            // Inner energy core pulse
            const corePulse = 1 + 0.3 * Math.sin(now * 0.003);
            energyCore.scale.set(corePulse, corePulse, corePulse);
            energyCoreMat.opacity = 0.1 + 0.15 * Math.sin(now * 0.002);

            // Hex grid subtle pulse
            hexMat.opacity = 0.06 + 0.04 * Math.sin(now * 0.0015);

            // Orbit rings wobble
            rings.forEach((ring, i) => {
                ring.rotation.x = Math.PI / 2.2 + Math.sin(now * 0.0008 + i * 1.2) * 0.15;
                ring.rotation.z += 0.001 + i * 0.0005;
                ring.material.opacity = 0.03 + 0.02 * Math.sin(now * 0.002 + i);
            });

            // Energy pulse rings expand and fade
            pulseRings.forEach(pr => {
                pr.userData.phase += pr.userData.speed;
                if (pr.userData.phase > Math.PI * 2) pr.userData.phase -= Math.PI * 2;
                const progress = pr.userData.phase / (Math.PI * 2);
                const sc = 1 + progress * 0.4;
                pr.scale.set(sc, sc, sc);
                pr.material.opacity = 0.12 * Math.sin(progress * Math.PI);
            });

            // Scan line sweep
            scanLine.rotation.x += 0.012;
            scanMat.opacity = 0.02 + 0.03 * Math.sin(now * 0.003);

            // Stars twinkle
            stars.rotation.y += 0.0002;
            stars.rotation.x += 0.0001;
            starsMaterial.opacity = 0.75 + 0.25 * Math.sin(now * 0.001);

            // Point light orbit
            pointLight.position.x = 3 * Math.cos(now * 0.0005);
            pointLight.position.z = 3 * Math.sin(now * 0.0005);

            // Pulse hotspot dots
            dotGroup.children.forEach((dot, i) => {
                dot.material.opacity = 0.4 + 0.6 * Math.sin(now * 0.003 + i);
                const sc = 1 + 0.5 * Math.sin(now * 0.004 + i * 0.5);
                dot.scale.set(sc, sc, sc);
            });

            // Connection arcs glow
            arcGroup.children.forEach(arc => {
                if (arc.userData.phase !== undefined) {
                    arc.material.opacity = 0.1 + 0.25 * Math.sin(now * 0.002 + arc.userData.phase);
                }
            });

            // Satellites orbit
            satGroup.children.forEach(child => {
                if (child.userData.orbitRadius) {
                    child.userData.phase += child.userData.speed;
                    const a = child.userData.phase;
                    const r = child.userData.orbitRadius;
                    const tilt = child.userData.tilt;
                    child.position.set(
                        r * Math.cos(a),
                        r * Math.sin(a) * Math.sin(tilt),
                        r * Math.sin(a) * Math.cos(tilt)
                    );
                    child.rotation.y += 0.05;
                    child.rotation.z += 0.03;
                }
            });

            // Data stream particles rise from surface
            dataParticles.children.forEach(dp => {
                dp.userData.height += dp.userData.speed;
                if (dp.userData.height > 1) dp.userData.height = 0;
                const h = dp.userData.height;
                const r = 1.01 + h * 0.3;
                const phi = dp.userData.basePhi;
                const theta = dp.userData.baseTheta;
                dp.position.set(
                    r * Math.sin(phi) * Math.cos(theta),
                    r * Math.cos(phi),
                    r * Math.sin(phi) * Math.sin(theta)
                );
                dp.material.opacity = 0.7 * (1 - h);
                const dsc = 0.5 + h * 1.5;
                dp.scale.set(dsc, dsc, dsc);
            });

            renderer.render(scene, camera);
        }
        animate();

        // ── Handle resize ──
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    })();
    </script>
    """
    components.html(globe_html, height=height + 10, scrolling=False)





# ===============================
# POPUP ALARM FUNCTION
# ===============================

def show_popup_alarm(risk_level, temp, rain, humid, wind):
    """Display a JavaScript popup alert with sound alarm for dangerous climate events."""
    color_map = {"Severe": "#ef4444", "High Risk": "#f59e0b", "Alert": "#3b82f6"}
    icon_map = {"Severe": "🚨", "High Risk": "⚠️", "Alert": "🌦️"}
    color = color_map.get(risk_level, "#3b82f6")
    icon = icon_map.get(risk_level, "🌦️")

    alarm_html = f"""
    <div id="climate-alarm-overlay" style="
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.7); z-index: 99999;
        display: flex; align-items: center; justify-content: center;
        animation: fadeIn 0.3s ease-out;">

        <div style="
            background: linear-gradient(135deg, #0f172a, #1e1b4b);
            border: 2px solid {color};
            border-radius: 24px; padding: 2.5rem;
            max-width: 480px; width: 90%;
            text-align: center;
            box-shadow: 0 0 60px {color}40;
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);">

            <div style="font-size: 4rem; margin-bottom: 0.8rem;">{icon}</div>
            <h2 style="color: {color}; font-size: 1.5rem; font-weight: 800; margin: 0 0 0.5rem 0;
                        font-family: 'Inter', sans-serif;">
                CLIMATE {risk_level.upper()} DETECTED
            </h2>
            <div style="background: rgba(255,255,255,0.05); border-radius: 12px;
                         padding: 1rem; margin: 1rem 0; text-align: left;">
                <div style="color: #94a3b8; font-size: 0.85rem; line-height: 2;">
                    Temperature: <strong style="color: #f1f5f9;">{temp} C</strong><br>
                    Rainfall: <strong style="color: #f1f5f9;">{rain} mm</strong><br>
                    Humidity: <strong style="color: #f1f5f9;">{humid}%</strong><br>
                    Wind Speed: <strong style="color: #f1f5f9;">{wind} km/h</strong>
                </div>
            </div>
            <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 1.5rem;">
                Take necessary precautions immediately!
            </p>
            <button onclick="document.getElementById('climate-alarm-overlay').remove();"
                style="background: linear-gradient(135deg, {color}, {color}cc);
                       color: white; border: none; border-radius: 12px;
                       padding: 0.7rem 2.5rem; font-size: 1rem; font-weight: 700;
                       cursor: pointer; letter-spacing: 0.5px;">
                DISMISS
            </button>
        </div>
    </div>

    <style>
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        @keyframes popIn {{
            from {{ opacity: 0; transform: scale(0.8); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
    </style>

    <script>
        // Auto-dismiss after 15 seconds
        setTimeout(function() {{
            var overlay = document.getElementById('climate-alarm-overlay');
            if (overlay) overlay.remove();
        }}, 15000);
    </script>
    """
    components.html(alarm_html, height=0, scrolling=False)


# ===============================
# SIDEBAR – NAVIGATION + INFO
# ===============================

with st.sidebar:
    st.markdown("""
    <style>
        @keyframes spinBounce {
            0% { transform: translateY(0) rotateY(0deg); }
            25% { transform: translateY(-12px) rotateY(90deg); }
            50% { transform: translateY(0) rotateY(180deg); }
            75% { transform: translateY(-8px) rotateY(270deg); }
            100% { transform: translateY(0) rotateY(360deg); }
        }
    </style>
    <div style="text-align:center; padding: 1.5rem 0;">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem; animation: spinBounce 3s ease-in-out infinite; display:inline-block;">🌍</div>
        <h2 style="background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    font-size: 1.3rem; font-weight: 800; margin: 0;">
            Climate Predictor
        </h2>
        <p style="color: #475569; font-size: 0.75rem; margin-top: 0.3rem; letter-spacing: 1.5px; text-transform: uppercase;">AI Weather Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # ── Page Navigation ──
    page = st.radio(
        "🧭 Navigation",
        ["🏠 Home", "📊 Predict", "📩 Alerts", "ℹ️ About"],
        index=0,
        label_visibility="visible"
    )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # System status
    st.markdown("""
    <div class="sidebar-info">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.8rem;">
            <span class="status-badge badge-active">● Live</span>
            <span style="color:#475569; font-size:0.72rem;">System Operational</span>
        </div>
        <div style="color:#64748b; font-size:0.78rem; line-height: 1.8;">
            🤖 LSTM Neural Network<br>
            📊 4 Climate Parameters<br>
            🎯 4 Risk Categories<br>
            📱 SMS Alert System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Quick Stats
    total_predictions = len(st.session_state.prediction_history)
    severe_count = sum(1 for h in st.session_state.prediction_history if h['risk'] == 'Severe')
    st.markdown(f"""
    <div style="display:flex; gap:0.5rem; margin-bottom:1rem;">
        <div style="flex:1; background:rgba(59,130,246,0.08); border:1px solid rgba(59,130,246,0.15); border-radius:12px; padding:0.8rem; text-align:center;">
            <div style="font-size:1.4rem; font-weight:800; font-family:'Orbitron',monospace; color:#3b82f6;">{total_predictions}</div>
            <div style="font-size:0.6rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Predictions</div>
        </div>
        <div style="flex:1; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.15); border-radius:12px; padding:0.8rem; text-align:center;">
            <div style="font-size:1.4rem; font-weight:800; font-family:'Orbitron',monospace; color:#ef4444;">{severe_count}</div>
            <div style="font-size:0.6rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Severe</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Prediction history (compact)
    if st.session_state.prediction_history:
        st.markdown("#### 📜 Recent")
        for entry in reversed(st.session_state.prediction_history[-3:]):
            risk = entry['risk']
            color_map = {"Severe": "#ef4444", "High Risk": "#f59e0b", "Alert": "#3b82f6", "Normal": "#10b981"}
            icon_map = {"Severe": "🚨", "High Risk": "⚠️", "Alert": "🌦️", "Normal": "✅"}
            dot_color = color_map.get(risk, "#94a3b8")
            icon = icon_map.get(risk, "●")
            st.markdown(f"""
            <div class="history-item">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:{dot_color}; font-weight:600; font-size:0.82rem;">{icon} {risk}</span>
                    <span style="color:#334155; font-size:0.65rem; font-family:'Orbitron',monospace;">{entry['time']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    current_time = datetime.datetime.now().strftime("%d %b %Y • %I:%M %p")
    st.markdown(f"""
    <div style="text-align:center; color:#334155; font-size:0.72rem; font-family:'Orbitron',monospace;">
        🕐 {current_time}
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════
# PAGE 1: HOME
# ═══════════════════════════════════════════

if page == "🏠 Home":

    # ── Hero Section ──
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Climate Prediction & Alert</h1>
        <p class="hero-subtitle">Powered by LSTM Deep Learning</p>
        <div class="hero-badges">
            <span class="hero-badge badge-ai">🤖 AI Powered</span>
            <span class="hero-badge badge-rt">⚡ Real-time</span>
            <span class="hero-badge badge-sms">📱 SMS Alerts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Rotating 3D Globe ──
    render_globe(450)

    st.markdown('<div class="fancy-divider-thick"></div>', unsafe_allow_html=True)

    # ── How It Works ──
    st.markdown("""
    <div class="section-title">
        <div class="icon-box" style="background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(59,130,246,0.2)); border: 1px solid rgba(139,92,246,0.3);">🔄</div>
        <div>
            <h3>How It Works</h3>
            <p>Four simple steps to predict and alert</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="steps-container">
        <div class="step-item">
            <div class="step-circle active">📊</div>
            <div class="step-text">Input Data</div>
        </div>
        <div class="step-item">
            <div class="step-circle active">🧠</div>
            <div class="step-text">AI Analysis</div>
        </div>
        <div class="step-item">
            <div class="step-circle active">📈</div>
            <div class="step-text">View Results</div>
        </div>
        <div class="step-item">
            <div class="step-circle active">📩</div>
            <div class="step-text">Send Alert</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # ── Features ──
    st.markdown("""
    <div class="section-title">
        <div class="icon-box" style="background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(59,130,246,0.2)); border: 1px solid rgba(6,182,212,0.3);">✨</div>
        <div>
            <h3>Key Features</h3>
            <p>Cutting-edge climate intelligence capabilities</p>
        </div>
    </div>

    <div class="feature-grid">
        <div class="feature-card" style="border-top: 3px solid #8b5cf6;">
            <div class="f-icon">🧠</div>
            <div class="f-title">LSTM Neural Network</div>
            <div class="f-desc">Deep learning model trained on temporal climate sequences for accurate pattern recognition</div>
        </div>
        <div class="feature-card" style="border-top: 3px solid #3b82f6;">
            <div class="f-icon">📊</div>
            <div class="f-title">4-Parameter Analysis</div>
            <div class="f-desc">Comprehensive analysis of temperature, rainfall, humidity, and wind speed data</div>
        </div>
        <div class="feature-card" style="border-top: 3px solid #ef4444;">
            <div class="f-icon">🚨</div>
            <div class="f-title">Real-time Alerts</div>
            <div class="f-desc">Instant popup alerts with sound alarms for dangerous weather conditions</div>
        </div>
        <div class="feature-card" style="border-top: 3px solid #10b981;">
            <div class="f-icon">📱</div>
            <div class="f-title">SMS Notifications</div>
            <div class="f-desc">Automated SMS dispatch to emergency contacts via Twilio integration</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats Bar ──
    st.markdown('<div class="fancy-divider-thick"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-row">
        <div class="stat-item">
            <div class="stat-number">4</div>
            <div class="stat-label">Parameters</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">LSTM</div>
            <div class="stat-label">Model Type</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">4</div>
            <div class="stat-label">Risk Levels</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">SMS</div>
            <div class="stat-label">Alert System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════
# PAGE 2: PREDICT
# ═══════════════════════════════════════════

elif page == "📊 Predict":

    st.markdown("""
    <div class="hero-section" style="padding: 1.5rem 1rem 0.5rem 1rem;">
        <h1 class="hero-title" style="font-size:2rem;">📊 Climate Risk Prediction</h1>
        <p class="hero-subtitle">Enter weather parameters for AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider-thick"></div>', unsafe_allow_html=True)

    # ── Input Section ──
    st.markdown("""
    <div class="section-title">
        <div class="icon-box" style="background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(139,92,246,0.2)); border: 1px solid rgba(59,130,246,0.3);">📊</div>
        <div>
            <h3>Climate Parameters</h3>
            <p>Enter current weather readings for AI-powered risk analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        temperature = st.number_input("🌡️ Temperature (°C)", 0.0, 60.0, 0.0, step=0.5, help="Current air temperature")
    with col2:
        rainfall = st.number_input("🌧️ Rainfall (mm)", 0.0, 200.0, 0.0, step=1.0, help="Rainfall in millimeters")
    with col3:
        humidity = st.number_input("💧 Humidity (%)", 0.0, 100.0, 0.0, step=1.0, help="Relative humidity percentage")
    with col4:
        wind = st.number_input("💨 Wind Speed (km/h)", 0.0, 100.0, 0.0, step=0.5, help="Wind speed in km/h")

    # ── Metric Cards ──
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)

    temp_pct = min(temperature / 60 * 100, 100)
    rain_pct = min(rainfall / 200 * 100, 100)
    humid_pct = min(humidity / 100 * 100, 100)
    wind_pct = min(wind / 100 * 100, 100)

    with mcol1:
        st.markdown(f"""
        <div class="metric-card temp">
            <div class="metric-icon">🌡️</div>
            <div class="metric-label">Temperature</div>
            <div class="metric-value">{temperature}°</div>
            <div class="metric-bar"><div class="metric-bar-fill" style="width:{temp_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with mcol2:
        st.markdown(f"""
        <div class="metric-card rain">
            <div class="metric-icon">🌧️</div>
            <div class="metric-label">Rainfall</div>
            <div class="metric-value">{rainfall}mm</div>
            <div class="metric-bar"><div class="metric-bar-fill" style="width:{rain_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with mcol3:
        st.markdown(f"""
        <div class="metric-card humid">
            <div class="metric-icon">💧</div>
            <div class="metric-label">Humidity</div>
            <div class="metric-value">{humidity}%</div>
            <div class="metric-bar"><div class="metric-bar-fill" style="width:{humid_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with mcol4:
        st.markdown(f"""
        <div class="metric-card wind">
            <div class="metric-icon">💨</div>
            <div class="metric-label">Wind Speed</div>
            <div class="metric-value">{wind}km/h</div>
            <div class="metric-bar"><div class="metric-bar-fill" style="width:{wind_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ── Predict Button ──
    bcol1, bcol2, bcol3 = st.columns([1, 2, 1])
    with bcol2:
        predict_clicked = st.button("🔍  Analyze Climate Risk", use_container_width=True)

    # ── Prediction Logic ──
    if predict_clicked:
        if temperature == 0 and rainfall == 0 and humidity == 0 and wind == 0:
            st.warning("⚠️ Please enter valid climate parameters before predicting.")
        else:
            with st.spinner("🧠 AI Neural Network analyzing climate patterns..."):
                user_df = pd.DataFrame(
                    [[temperature, rainfall, humidity, wind]],
                    columns=['Temperature', 'Rainfall', 'Humidity', 'Wind Speed']
                )

                scaled = scaler.transform(user_df)
                sequence = np.repeat(scaled, 5, axis=0).reshape(1, 5, 4)

                prediction = model.predict(sequence, verbose=0)
                predicted_class = np.argmax(prediction)

                risk_names = {
                    0: "Normal",
                    1: "Alert",
                    2: "High Risk",
                    3: "Severe"
                }

                st.session_state.final_risk = risk_names[predicted_class]
                st.session_state.prediction_probs = prediction[0]
                st.session_state.last_inputs = {
                    'temp': temperature, 'rain': rainfall,
                    'humid': humidity, 'wind': wind
                }

                st.session_state.prediction_history.append({
                    'risk': risk_names[predicted_class],
                    'temp': temperature,
                    'rain': rainfall,
                    'humid': humidity,
                    'wind': wind,
                    'time': datetime.datetime.now().strftime("%H:%M:%S")
                })

                st.rerun()

    # ── Results Section ──
    if st.session_state.final_risk:
        final_risk = st.session_state.final_risk

        st.markdown('<div class="fancy-divider-thick"></div>', unsafe_allow_html=True)

        # Section Title
        st.markdown("""
        <div class="section-title">
            <div class="icon-box" style="background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(245,158,11,0.2)); border: 1px solid rgba(239,68,68,0.3);">🎯</div>
            <div>
                <h3>Prediction Results</h3>
                <p>AI-powered climate risk assessment complete</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk Level Stepper
        risk_levels = ["Normal", "Alert", "High Risk", "Severe"]
        risk_icons_stepper = ["✅", "🌦️", "⚠️", "🚨"]
        risk_colors_stepper = ["#10b981", "#3b82f6", "#f59e0b", "#ef4444"]
        risk_bg_stepper = ["rgba(16,185,129,0.2)", "rgba(59,130,246,0.2)", "rgba(245,158,11,0.2)", "rgba(239,68,68,0.2)"]

        stepper_html = '<div class="risk-stepper">'
        for i, (level, icon, color, bg) in enumerate(zip(risk_levels, risk_icons_stepper, risk_colors_stepper, risk_bg_stepper)):
            is_active = level == final_risk
            active_class = "active" if is_active else "inactive"
            dot_style = f"background:{bg}; color:{color}; border: 2px solid {color};" if is_active else ""
            label_color = color if is_active else "#475569"
            stepper_html += (
                f'<div class="risk-step">'
                f'<div class="risk-dot {active_class}" style="{dot_style}">{icon}</div>'
                f'<div class="risk-step-label" style="color:{label_color};">{level}</div>'
                f'</div>'
            )
        stepper_html += '</div>'
        st.markdown(stepper_html, unsafe_allow_html=True)

        # Result Card
        result_map = {
            "Severe": ("result-severe", "🚨", "EXTREME CLIMATE DANGER", "Immediate action required! Severe weather conditions detected. Evacuate if necessary."),
            "High Risk": ("result-high", "⚠️", "HIGH CLIMATE RISK", "Dangerous weather conditions approaching. Take precautionary measures immediately."),
            "Alert": ("result-alert", "🌦️", "WEATHER ALERT", "Unusual weather patterns detected. Stay informed and prepared for changes."),
            "Normal": ("result-normal", "✅", "CLIMATE NORMAL", "All weather parameters are within safe ranges. No immediate threats detected.")
        }

        css_class, icon, title, desc = result_map[final_risk]
        st.markdown(
            f'<div class="result-card {css_class}">'
            f'<div class="result-icon">{icon}</div>'
            f'<h2>{title}</h2>'
            f'<p>{desc}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Popup + alarm for dangerous levels
        if final_risk != "Normal":
            last = st.session_state.last_inputs or {'temp': 0, 'rain': 0, 'humid': 0, 'wind': 0}
            show_popup_alarm(final_risk, last['temp'], last['rain'], last['humid'], last['wind'])

        # Charts Section
        if st.session_state.prediction_probs is not None:
            probs = st.session_state.prediction_probs
            risk_labels = ["Normal", "Alert", "High Risk", "Severe"]
            risk_colors_css = ["green", "blue", "amber", "red"]
            risk_index = risk_labels.index(final_risk)
            confidence = float(probs[risk_index]) * 100

            chart_col1, chart_col2 = st.columns(2)

            # CSS Gauge
            with chart_col1:
                gauge_color_map = {
                    "Normal": "#10b981", "Alert": "#3b82f6",
                    "High Risk": "#f59e0b", "Severe": "#ef4444"
                }
                gauge_color = gauge_color_map[final_risk]
                angle = confidence * 3.6

                st.markdown(
                    f'<div class="glass-card" style="text-align:center;">'
                    f'<h4 style="color:#64748b; margin-bottom:1rem; font-size:0.8rem; text-transform:uppercase; letter-spacing:2px;">Confidence Level</h4>'
                    f'<div class="gauge-container">'
                    f'<div class="gauge-ring" style="background: conic-gradient({gauge_color} {angle}deg, rgba(255,255,255,0.05) {angle}deg);">'
                    f'<div class="gauge-inner">'
                    f'<div class="gauge-value" style="color:{gauge_color};">{confidence:.1f}%</div>'
                    f'<div class="gauge-label">{final_risk}</div>'
                    f'</div></div></div></div>',
                    unsafe_allow_html=True
                )

            # CSS Bar Chart
            with chart_col2:
                bars_html = ""
                max_prob = max(float(p) for p in probs)
                for i, (label, css_color) in enumerate(zip(risk_labels, risk_colors_css)):
                    pct = float(probs[i]) * 100
                    bar_width = (float(probs[i]) / max_prob * 100) if max_prob > 0 else 0
                    bars_html += (
                        f'<div class="prob-bar-row">'
                        f'<div class="prob-bar-label">{label}</div>'
                        f'<div class="prob-bar-track">'
                        f'<div class="prob-bar-fill {css_color}" style="width:{bar_width}%;"></div>'
                        f'</div>'
                        f'<div class="prob-bar-value">{pct:.1f}%</div>'
                        f'</div>'
                    )

                full_html = (
                    '<div class="glass-card">'
                    '<h4 style="color:#64748b; margin-bottom:1rem; font-size:0.8rem; text-transform:uppercase; letter-spacing:2px;">'
                    'Risk Probability Distribution</h4>'
                    f'<div class="prob-chart">{bars_html}</div>'
                    '</div>'
                )
                st.markdown(full_html, unsafe_allow_html=True)

        # Safety Tips
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        tips_map = {
            "Severe": [
                ("🏠", "Seek Shelter", "Move to a sturdy building immediately. Avoid windows and open areas."),
                ("📱", "Stay Connected", "Keep your phone charged. Monitor emergency broadcasts continuously."),
                ("🚗", "Avoid Travel", "Do not drive unless absolutely necessary. Roads may be dangerous."),
                ("🧰", "Emergency Kit", "Prepare water, food, first-aid supplies, and flashlights.")
            ],
            "High Risk": [
                ("🏠", "Stay Indoors", "Limit outdoor activities. Secure loose items around your property."),
                ("📻", "Monitor Updates", "Follow local weather forecasts and official advisories."),
                ("💧", "Store Water", "Keep drinking water reserves. Power outages are possible."),
                ("🤝", "Alert Neighbors", "Inform elderly and vulnerable people in your community.")
            ],
            "Alert": [
                ("👀", "Stay Aware", "Keep an eye on weather changes throughout the day."),
                ("🌂", "Be Prepared", "Carry rain gear and dress appropriately for conditions."),
                ("📋", "Plan Ahead", "Have backup plans for outdoor activities."),
                ("📱", "Check Forecasts", "Review updated weather forecasts regularly.")
            ],
            "Normal": [
                ("☀️", "Enjoy Outdoors", "Great conditions for outdoor activities and recreation."),
                ("💧", "Stay Hydrated", "Drink plenty of water throughout the day."),
                ("🌿", "Go Green", "Perfect weather for gardening or nature walks."),
                ("😊", "Relax", "No weather concerns. Enjoy your day!")
            ]
        }

        tips = tips_map[final_risk]
        tip_colors = {"Severe": "#ef4444", "High Risk": "#f59e0b", "Alert": "#3b82f6", "Normal": "#10b981"}
        tip_color = tip_colors[final_risk]

        st.markdown(
            f'<div class="section-title">'
            f'<div class="icon-box" style="background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(59,130,246,0.2)); border: 1px solid rgba(139,92,246,0.3);">💡</div>'
            f'<div><h3>Safety Recommendations</h3>'
            f'<p>Suggested actions based on the {final_risk.lower()} risk level</p></div></div>',
            unsafe_allow_html=True
        )

        tips_html = '<div class="tips-grid">'
        for tip_icon, tip_title, tip_desc in tips:
            tips_html += (
                f'<div class="tip-card">'
                f'<div class="tip-icon">{tip_icon}</div>'
                f'<div class="tip-title" style="color:{tip_color};">{tip_title}</div>'
                f'<div class="tip-desc">{tip_desc}</div>'
                f'</div>'
            )
        tips_html += '</div>'
        st.markdown(tips_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════
# PAGE 3: ALERTS
# ═══════════════════════════════════════════

elif page == "📩 Alerts":

    st.markdown("""
    <div class="hero-section" style="padding: 1.5rem 1rem 0.5rem 1rem;">
        <h1 class="hero-title" style="font-size:2rem;">📩 Emergency Alert System</h1>
        <p class="hero-subtitle">Dispatch SMS warnings to emergency contacts</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider-thick"></div>', unsafe_allow_html=True)

    final_risk = st.session_state.final_risk

    if final_risk and final_risk != "Normal":

        # Current risk display
        risk_color_map = {"Severe": "#ef4444", "High Risk": "#f59e0b", "Alert": "#3b82f6"}
        risk_icon_map = {"Severe": "🚨", "High Risk": "⚠️", "Alert": "🌦️"}
        rcolor = risk_color_map.get(final_risk, "#3b82f6")
        ricon = risk_icon_map.get(final_risk, "🌦️")

        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:3rem; margin-bottom:0.5rem;">{ricon}</div>
            <h3 style="color:{rcolor}; font-size:1.5rem; margin-bottom:0.5rem;">Current Risk: {final_risk}</h3>
            <p style="color:#64748b; font-size:0.88rem;">SMS alerts are ready to be dispatched</p>
        </div>
        """, unsafe_allow_html=True)

        # Contact cards
        st.markdown("""
        <div class="section-title">
            <div class="icon-box" style="background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(245,158,11,0.2)); border: 1px solid rgba(239,68,68,0.3);">👥</div>
            <div>
                <h3>Emergency Contacts</h3>
                <p>Registered numbers for alert dispatch</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        phone_list = [
            "+919025364252",
            "+918248194449"
        ]

        contact_html = '<div style="display:flex; gap:0.8rem; margin-bottom:1.5rem; flex-wrap:wrap;">'
        for phone in phone_list:
            contact_html += (
                f'<div style="flex:1; min-width:200px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:1rem; display:flex; align-items:center; gap:0.8rem;">'
                f'<div style="width:40px;height:40px;border-radius:50%;background:rgba(59,130,246,0.15);display:flex;align-items:center;justify-content:center;font-size:1.2rem;">👤</div>'
                f'<div><div style="font-size:0.75rem;color:#64748b;">Emergency Contact</div>'
                f'<div style="font-size:0.9rem;color:#e2e8f0;font-family:Orbitron,monospace;">{phone}</div></div>'
                f'</div>'
            )
        contact_html += '</div>'
        st.markdown(contact_html, unsafe_allow_html=True)

        # Send button
        alert_col1, alert_col2, alert_col3 = st.columns([1, 2, 1])
        with alert_col2:
            if st.button("🚨  Send Emergency Alert", use_container_width=True):

                last = st.session_state.last_inputs or {'temp': 0, 'rain': 0, 'humid': 0, 'wind': 0}
                time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

                # Safety recommendations per risk level (plain text for SMS)
                safety_tips = {
                    "Severe": [
                        "Seek shelter in a sturdy building immediately",
                        "Keep phone charged and monitor emergency broadcasts",
                        "Do NOT travel unless absolutely necessary",
                        "Prepare water, food, first-aid and flashlights"
                    ],
                    "High Risk": [
                        "Stay indoors and secure loose items around property",
                        "Follow local weather forecasts and official advisories",
                        "Keep drinking water reserves ready",
                        "Inform elderly and vulnerable people nearby"
                    ],
                    "Alert": [
                        "Stay aware of weather changes throughout the day",
                        "Carry rain gear and dress for conditions",
                        "Have backup plans for outdoor activities",
                        "Check updated weather forecasts regularly"
                    ]
                }

                tips_list = safety_tips.get(final_risk, [])
                tips_text = "\n".join(f"- {tip}" for tip in tips_list)

                message = f"""CLIMATE ALERT - Risk Level: {final_risk}
Temperature: {last['temp']}C
Rainfall: {last['rain']}mm
Humidity: {last['humid']}%
Wind: {last['wind']} km/h
Time: {time_now}

Safety Recommendations:
{tips_text}

Take necessary precautions and stay safe!"""
                progress = st.progress(0, text="📤 Preparing to send alerts...")

                for idx, number in enumerate(phone_list):
                    try:
                        send_sms(message, number)
                        progress.progress(
                            (idx + 1) / len(phone_list),
                            text=f"✅ Alert sent to {number}"
                        )
                        st.success(f"✅ Alert successfully sent to {number}")
                    except Exception as e:
                        st.error(f"❌ Failed to send to {number}: {e}")

                # Celebration
                st.markdown("""
                <div class="climate-celebration" style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3);">
                    <div class="celebration-text">
                        <div style="font-size:3rem; margin-bottom:0.5rem;">✅</div>
                        <h3 style="color:#10b981;">Alerts Dispatched!</h3>
                        <p style="color:#94a3b8;">Emergency notifications sent to all contacts</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Popup alert with sound alarm after SMS sent
                show_popup_alarm(final_risk, last['temp'], last['rain'], last['humid'], last['wind'])

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:4rem; margin-bottom:1rem; animation: float 3s ease-in-out infinite; display:inline-block;">🌤️</div>
            <h3 style="color:#10b981; font-size:1.4rem; margin-bottom:0.5rem;">No Active Alerts</h3>
            <p style="color:#64748b; font-size:0.95rem; margin-bottom:1rem;">Climate conditions are normal or no prediction has been made yet.</p>
            <p style="color:#475569; font-size:0.85rem;">Go to the <strong style="color:#8b5cf6;">📊 Predict</strong> page to analyze climate data first.</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Alert History ──
    st.markdown('<div class="fancy-divider-thick"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
        <div class="icon-box" style="background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(59,130,246,0.2)); border: 1px solid rgba(139,92,246,0.3);">📜</div>
        <div>
            <h3>Prediction History</h3>
            <p>Complete log of all climate risk assessments</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.prediction_history:
        for entry in reversed(st.session_state.prediction_history):
            risk = entry['risk']
            color_map = {"Severe": "#ef4444", "High Risk": "#f59e0b", "Alert": "#3b82f6", "Normal": "#10b981"}
            icon_map = {"Severe": "🚨", "High Risk": "⚠️", "Alert": "🌦️", "Normal": "✅"}
            dot_color = color_map.get(risk, "#94a3b8")
            icon = icon_map.get(risk, "●")
            st.markdown(f"""
            <div class="history-item" style="margin-bottom:0.6rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:{dot_color}; font-weight:700; font-size:0.9rem;">{icon} {risk}</span>
                    <span style="color:#475569; font-size:0.72rem; font-family:'Orbitron',monospace;">{entry['time']}</span>
                </div>
                <div style="color:#64748b; font-size:0.78rem; margin-top:0.4rem;">
                    🌡 {entry['temp']}°C &nbsp; 🌧 {entry['rain']}mm &nbsp; 💧 {entry['humid']}% &nbsp; 💨 {entry['wind']}km/h
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#475569; text-align:center; padding:2rem 0;">No predictions recorded yet</p>', unsafe_allow_html=True)


# ═══════════════════════════════════════════
# PAGE 4: ABOUT
# ═══════════════════════════════════════════

elif page == "ℹ️ About":

    st.markdown("""
    <div class="hero-section" style="padding: 1.5rem 1rem 0.5rem 1rem;">
        <h1 class="hero-title" style="font-size:2rem;">ℹ️ About the System</h1>
        <p class="hero-subtitle">Climate Intelligence powered by Deep Learning</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider-thick"></div>', unsafe_allow_html=True)

    # ── System Architecture ──
    st.markdown("""
    <div class="section-title">
        <div class="icon-box" style="background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(59,130,246,0.2)); border: 1px solid rgba(139,92,246,0.3);">🏗️</div>
        <div>
            <h3>System Architecture</h3>
            <p>How the climate prediction engine works</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    arch_col1, arch_col2 = st.columns(2)

    with arch_col1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#8b5cf6; font-size:1rem; margin-bottom:1rem;">🧠 Machine Learning Pipeline</h4>
            <div style="color:#94a3b8; font-size:0.85rem; line-height:2;">
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                    <span style="background:rgba(139,92,246,0.2); color:#a78bfa; padding:0.2rem 0.6rem; border-radius:6px; font-size:0.7rem; font-weight:600;">1</span>
                    <span>Data Collection — 4 climate parameters</span>
                </div>
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                    <span style="background:rgba(59,130,246,0.2); color:#93c5fd; padding:0.2rem 0.6rem; border-radius:6px; font-size:0.7rem; font-weight:600;">2</span>
                    <span>Feature Scaling — StandardScaler normalization</span>
                </div>
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                    <span style="background:rgba(6,182,212,0.2); color:#67e8f9; padding:0.2rem 0.6rem; border-radius:6px; font-size:0.7rem; font-weight:600;">3</span>
                    <span>Sequence Generation — 5-step time series</span>
                </div>
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                    <span style="background:rgba(16,185,129,0.2); color:#6ee7b7; padding:0.2rem 0.6rem; border-radius:6px; font-size:0.7rem; font-weight:600;">4</span>
                    <span>LSTM Inference — Neural network prediction</span>
                </div>
                <div style="display:flex; align-items:center; gap:0.5rem;">
                    <span style="background:rgba(245,158,11,0.2); color:#fcd34d; padding:0.2rem 0.6rem; border-radius:6px; font-size:0.7rem; font-weight:600;">5</span>
                    <span>Risk Classification — 4-level output</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with arch_col2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#3b82f6; font-size:1rem; margin-bottom:1rem;">📐 Model Specifications</h4>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                <div style="background:rgba(255,255,255,0.03); border-radius:12px; padding:1rem; text-align:center;">
                    <div style="font-size:0.65rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Architecture</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#8b5cf6; font-family:'Orbitron',monospace;">LSTM</div>
                </div>
                <div style="background:rgba(255,255,255,0.03); border-radius:12px; padding:1rem; text-align:center;">
                    <div style="font-size:0.65rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Input Features</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#3b82f6; font-family:'Orbitron',monospace;">4</div>
                </div>
                <div style="background:rgba(255,255,255,0.03); border-radius:12px; padding:1rem; text-align:center;">
                    <div style="font-size:0.65rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Time Steps</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#06b6d4; font-family:'Orbitron',monospace;">5</div>
                </div>
                <div style="background:rgba(255,255,255,0.03); border-radius:12px; padding:1rem; text-align:center;">
                    <div style="font-size:0.65rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Output Classes</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#10b981; font-family:'Orbitron',monospace;">4</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # ── Risk Levels ──
    st.markdown("""
    <div class="section-title">
        <div class="icon-box" style="background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(239,68,68,0.2)); border: 1px solid rgba(245,158,11,0.3);">🎯</div>
        <div>
            <h3>Risk Level Definitions</h3>
            <p>Understanding the 4-tier climate risk classification</p>
        </div>
    </div>

    <div class="feature-grid">
        <div class="feature-card" style="border-top:3px solid #10b981;">
            <div class="f-icon">✅</div>
            <div class="f-title" style="color:#10b981;">Normal</div>
            <div class="f-desc">All weather parameters within safe ranges. No action needed.</div>
        </div>
        <div class="feature-card" style="border-top:3px solid #3b82f6;">
            <div class="f-icon">🌦️</div>
            <div class="f-title" style="color:#3b82f6;">Alert</div>
            <div class="f-desc">Unusual patterns detected. Stay aware and monitor conditions.</div>
        </div>
        <div class="feature-card" style="border-top:3px solid #f59e0b;">
            <div class="f-icon">⚠️</div>
            <div class="f-title" style="color:#f59e0b;">High Risk</div>
            <div class="f-desc">Dangerous conditions approaching. Take precautionary measures.</div>
        </div>
        <div class="feature-card" style="border-top:3px solid #ef4444;">
            <div class="f-icon">🚨</div>
            <div class="f-title" style="color:#ef4444;">Severe</div>
            <div class="f-desc">Extreme danger! Immediate action required for safety.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Footer ──
    st.markdown('<div class="fancy-divider-thick"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-brand">🌍 Climate Prediction & Alert System</div>
            <p style="color:#475569; font-size:0.8rem; margin:0.3rem 0;">Intelligent weather monitoring powered by deep learning neural networks</p>
            <div class="footer-links">
                <span>🤖 LSTM Model</span>
                <span>📊 Real-time Analysis</span>
                <span>📱 SMS Integration</span>
                <span>🔒 Secure</span>
            </div>
            <div class="footer-tech">
                <span class="tech-badge">Python</span>
                <span class="tech-badge">TensorFlow</span>
                <span class="tech-badge">Keras</span>
                <span class="tech-badge">Streamlit</span>
                <span class="tech-badge">Twilio</span>
                <span class="tech-badge">Three.js</span>
            </div>
            <p style="color:#1e293b; font-size:0.65rem; margin-top:0.8rem;">© 2026 Climate Intelligence System • All Rights Reserved</p>
        </div>
    </div>
    """, unsafe_allow_html=True)