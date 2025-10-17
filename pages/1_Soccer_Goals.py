import streamlit as st
from statistics import mean

st.set_page_config(page_title="GETO Goals", page_icon="⚽", layout="centered")

# ---------- STYLING ----------
st.markdown("""
<style>
:root {--bg:#0b1220;--card:#111827;--ink:#f8fafc;--muted:#9ca3af;
--border:#1e293b;--grad:linear-gradient(90deg,#38bdf8,#22d3ee);}
[data-testid="stAppViewContainer"]{background:var(--bg);}
*{font-family:Inter,system-ui;color:var(--ink);}
h1{text-align:center;font-weight:800;margin-bottom:8px;}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:18px;margin-top:12px;}
label{display:block;margin-top:6px;}
input{width:100%;background:var(--card);border:1px solid var(--border);
color:var(--ink);border-radius:12px;padding:10px;font-size:18px;text-align:center;margin-bottom:6px;}
button{width:100%;background:var(--grad);color:#0b1220;border:none;border-radius:14px;
padding:14px;font-size:18px;font-weight:800;margin-top:10px;}
.output{margin-top:14px;font-size:16px;}
</style>

<h1>⚽ GETO Goals (Mobile)</h1>
<p style='text-align:center;color:var(--muted);'>Numeric keypad version — instant entry on phones.</p>

<form id='goalsForm'>
<div class='card'>
  <h3>Scored & Conceded %</h3>
  <label>Home Over 1.5 %</label><input type='number' step='any' inputmode='decimal' name='h15'>
  <label>Away Over 1.5 %</label><input type='number' step='any' inputmode='decimal' name='a15'>
  <label>Home Over 2.5 %</label><input type='number' step='any' inputmode='decimal' name='h25'>
  <label>Away Over 2.5 %</label><input type='number' step='any' inputmode='decimal' name='a25'>
  <label>League Avg Goals</label><input type='number' step='any' inputmode='decimal' name='league'>
</div>
<button type='button' onclick='getoRunModel()'>🔮 Run Model</button>
</form>

<div id='output' class='output'></div>

<script>
function getoRunModel(){
  const h15=parseFloat(document.querySelector("[name='h15']").value||0);
  const a15=parseFloat(document.querySelector("[name='a15']").value||0);
  const h25=parseFloat(document.querySelector("[name='h25']").value||0);
  const a25=parseFloat(document.querySelector("[name='a25']").value||0);
  const league=parseFloat(document.querySelector("[name='league']").value||0);

  let over15=(h15+a15)/2;
  let over25=(h25+a25)/2;
  let adj = league>3 ? 4 : league<2.3 ? -3 : 0;
  over15=Math.min(Math.max(over15+adj,0),100);
  over25=Math.min(Math.max(over25+adj,0),100);

  let verdict = over25>60 ? "💎 Strong Over 2.5" :
                over25>45 ? "🔥 Lean Over" :
                over25>30 ? "⚠️ Lean Under" : "❌ Strong Under";

  document.getElementById("output").innerHTML =
    `<div class='card'><b>GETO GOALS MODEL OUTPUT</b><br>
    Over 1.5: ${over15.toFixed(1)}%<br>
    Over 2.5: ${over25.toFixed(1)}%<br>
    <b>Verdict:</b> ${verdict}</div>`;
}
</script>
""", unsafe_allow_html=True)
