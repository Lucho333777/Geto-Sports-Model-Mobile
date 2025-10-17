import streamlit as st

st.set_page_config(page_title="GETO Sports Model (Mobile)", page_icon="📱", layout="centered")

# Global mobile-first styles
st.markdown("""
<style>
:root {
  --bg:#0b1220; --card:#111827; --ink:#e5e7eb; --muted:#93a3b8;
  --border:#1f2937; --grad:linear-gradient(90deg,#3b82f6,#60a5fa);
  --accent:#22c55e; --danger:#ef4444;
}
[data-testid="stAppViewContainer"]{background:var(--bg);}
*{font-family: Inter, system-ui; color:var(--ink);}
h1,h2,h3{font-weight:800;}
.card{background:var(--card); border:1px solid var(--border); border-radius:16px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,.25);}
.btn-primary button{width:100%; height:52px; border-radius:14px; border:none;
  background:var(--grad); color:white; font-weight:800; font-size:18px;}
.badge{font-size:12px; color:var(--muted); border:1px solid var(--border); padding:3px 8px; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>GETO — Mobile</h1>", unsafe_allow_html=True)
st.caption("Tap the sidebar ▸ Pages ▸ pick **Soccer Goals** or **Soccer Corners**. NBA coming soon.")

st.markdown("""
<div class='card'>
  <b>What’s inside:</b><br>
  • Mobile-native numeric keypad inputs (iOS/Android)<br>
  • Clean results with confidence tiers<br>
  • Parlay preview with correlation penalty<br>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
st.button("Open Pages in Sidebar ➜")
st.markdown("</div>", unsafe_allow_html=True)
