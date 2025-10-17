import streamlit as st

st.set_page_config(page_title="GETO NBA (Mobile)", page_icon="🏀", layout="centered")

st.markdown("""
<style>
:root { --bg:#0b1220; --card:#0f172a; --ink:#e5e7eb; --muted:#93a3b8; --border:#1f2937; --grad:linear-gradient(90deg,#22c55e,#06b6d4); }
[data-testid="stAppViewContainer"]{background:var(--bg);}
*{font-family:Inter, system-ui; color:var(--ink);}
.card{background:var(--card); border:1px solid var(--border); border-radius:16px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,.25); text-align:center;}
.btn button{width:100%; height:52px; border:none; border-radius:14px; background:var(--grad); color:white; font-weight:800; font-size:18px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>🏀 GETO NBA — Mobile</h1>", unsafe_allow_html=True)
st.markdown("<div class='card'><b>Coming Soon</b><br>We’re calibrating pace, eFG%, and 3P variance models.</div>", unsafe_allow_html=True)
st.markdown("<div class='btn'>", unsafe_allow_html=True)
st.button("Notify Me When Live")
st.markdown("</div>", unsafe_allow_html=True)
