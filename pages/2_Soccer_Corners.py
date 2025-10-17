import streamlit as st
from statistics import mean

st.set_page_config(page_title="GETO Corners", page_icon="🏁", layout="centered")

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

<h1>🏁 GETO Corners (Mobile)</h1>
<p style='text-align:center;color:var(--muted);'>Quick numeric entry + instant model output.</p>

<form id='cornersForm'>
<div class='card'>
  <h3>Total Corners</h3>
  <label>Home Over 8.5 %</label><input type='number' step='any' inputmode='decimal' name='h85'>
  <label>Away Over 8.5 %</label><input type='number' step='any' inputmode='decimal' name='a85'>
  <label>Home Over 9.5 %</label><input type='number' step='any' inputmode='decimal' name='h95'>
  <label>Away Over 9.5 %</label><input type='number' step='any' inputmode='decimal' name='a95'>
  <label>League Avg Corners</label><input type='number' step='any' inputmode='decimal' name='league'>
</div>
<button type='button' onclick='runCornerModel()'>🔮 Run Model</button>
</form>

<div id='output' class='output'></div>

<script>
function runCornerModel(){
  const h85=parseFloat(document.querySelector("[name='h85']").value||0);
  const a85=parseFloat(document.querySelector("[name='a85']").value||0);
  const h95=parseFloat(document.querySelector("[name='h95']").value||0);
  const a95=parseFloat(document.querySelector("[name='a95']").value||0);
  const league=parseFloat(document.querySelector("[name='league']").value||0);

  let over85=(h85+a85)/2;
  let over95=(h95+a95)/2;
  let adj = league>10 ? 4 : league<8 ? -3 : 0;
  over85=Math.min(Math.max(over85+adj,0),100);
  over95=Math.min(Math.max(over95+adj,0),100);

  let verdict = over95>60 ? "💎 High Corner Tempo" :
                over95>45 ? "🔥 Lean Over" :
                over95>30 ? "⚠️ Lean Under" : "❌ Low Pace";

  document.getElementById("output").innerHTML =
    `<div class='card'><b>GETO CORNERS MODEL OUTPUT</b><br>
    Over 8.5: ${over85.toFixed(1)}%<br>
    Over 9.5: ${over95.toFixed(1)}%<br>
    <b>Verdict:</b> ${verdict}</div>`;
}
</script>
""", unsafe_allow_html=True)
