import streamlit as st

st.set_page_config(page_title="GETO Sports Model", page_icon="⚡", layout="centered")

st.markdown("""
<style>
:root {--bg:#0b1220;--ink:#f8fafc;--muted:#9ca3af;--grad:linear-gradient(90deg,#38bdf8,#22d3ee);}
[data-testid="stAppViewContainer"]{background:var(--bg);}
*{font-family:Inter,system-ui;color:var(--ink);}
h1{font-weight:800;text-align:center;margin-bottom:6px;}
.card{background:#111827;border-radius:16px;padding:18px;margin:12px 0;box-shadow:0 4px 12px rgba(0,0,0,.35);}
a{text-decoration:none;color:var(--ink);}
.btn{display:block;text-align:center;padding:14px;border-radius:14px;font-weight:800;
background:var(--grad);color:#0b1220;font-size:18px;margin:8px 0;}
</style>

<h1>⚡ GETO Sports Models</h1>
<p style='text-align:center;color:var(--muted);'>Select a model to begin:</p>

<div class='card'>
  <a class='btn' href='./1_Soccer_Goals'>⚽ Soccer Goals Model</a>
  <a class='btn' href='./2_Soccer_Corners'>🏁 Soccer Corners Model</a>
  <a class='btn' href='./3_NBA_Coming_Soon'>🏀 NBA (Coming Soon)</a>
</div>
""", unsafe_allow_html=True)
