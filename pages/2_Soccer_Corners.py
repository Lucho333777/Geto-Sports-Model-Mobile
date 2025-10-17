import streamlit as st

st.set_page_config(page_title="GETO Corners (Mobile)", page_icon="🏁", layout="centered")

st.markdown("""
<style>
:root {--bg:#0b1220;--card:#111827;--ink:#f8fafc;--muted:#9ca3af;--border:#1e293b;--grad:linear-gradient(90deg,#38bdf8,#22d3ee);}
[data-testid="stAppViewContainer"]{background:var(--bg);}
*{font-family:Inter,system-ui;color:var(--ink);}
h1{text-align:center;font-weight:800;margin:8px 0;}
h3{margin:8px 0;}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;margin-top:12px;}
label{display:block;margin-top:6px;}
input,select{width:100%;background:var(--card);border:1px solid var(--border);
  color:var(--ink);border-radius:12px;padding:10px;font-size:18px;text-align:center;margin-bottom:6px;}
button{width:100%;background:var(--grad);color:#0b1220;border:none;border-radius:14px;
  padding:14px;font-size:18px;font-weight:900;margin-top:10px;}
.output{margin-top:14px;font-size:16px;}
.badge{font-size:13px;color:var(--muted);border:1px solid var(--border);padding:3px 8px;border-radius:10px;margin-left:6px;}
.row{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.sep{height:8px}
.info{color:var(--muted);font-size:13px;margin-top:6px}
</style>

<h1>🏁 GETO Corners (Mobile)</h1>
<p style='text-align:center;color:var(--muted);'>Totals 6.5–10.5; Earned/Conceded 2.5–5.5. Native number keypad.</p>

<form id='cornersForm' onsubmit='return false;'>

<div class='card'>
  <h3>📊 Total Corners % (Home & Away)</h3>
  <div class="row">
    <div><label>Home Over 6.5 %</label><input type='number' step='any' inputmode='decimal' name='ht65'></div>
    <div><label>Away Over 6.5 %</label><input type='number' step='any' inputmode='decimal' name='at65'></div>
    <div><label>Home Over 7.5 %</label><input type='number' step='any' inputmode='decimal' name='ht75'></div>
    <div><label>Away Over 7.5 %</label><input type='number' step='any' inputmode='decimal' name='at75'></div>
    <div><label>Home Over 8.5 %</label><input type='number' step='any' inputmode='decimal' name='ht85'></div>
    <div><label>Away Over 8.5 %</label><input type='number' step='any' inputmode='decimal' name='at85'></div>
    <div><label>Home Over 9.5 %</label><input type='number' step='any' inputmode='decimal' name='ht95'></div>
    <div><label>Away Over 9.5 %</label><input type='number' step='any' inputmode='decimal' name='at95'></div>
    <div><label>Home Over 10.5 %</label><input type='number' step='any' inputmode='decimal' name='ht105'></div>
    <div><label>Away Over 10.5 %</label><input type='number' step='any' inputmode='decimal' name='at105'></div>
  </div>
</div>

<div class='card'>
  <h3>🚀 Team Corners Earned %</h3>
  <div class="row">
    <div><label>Home Over 2.5 %</label><input type='number' step='any' inputmode='decimal' name='he25'></div>
    <div><label>Away Over 2.5 %</label><input type='number' step='any' inputmode='decimal' name='ae25'></div>
    <div><label>Home Over 3.5 %</label><input type='number' step='any' inputmode='decimal' name='he35'></div>
    <div><label>Away Over 3.5 %</label><input type='number' step='any' inputmode='decimal' name='ae35'></div>
    <div><label>Home Over 4.5 %</label><input type='number' step='any' inputmode='decimal' name='he45'></div>
    <div><label>Away Over 4.5 %</label><input type='number' step='any' inputmode='decimal' name='ae45'></div>
    <div><label>Home Over 5.5 %</label><input type='number' step='any' inputmode='decimal' name='he55'></div>
    <div><label>Away Over 5.5 %</label><input type='number' step='any' inputmode='decimal' name='ae55'></div>
  </div>
</div>

<div class='card'>
  <h3>🧱 Team Corners Conceded %</h3>
  <div class="row">
    <div><label>Home Conceded 2.5 %</label><input type='number' step='any' inputmode='decimal' name='hc25'></div>
    <div><label>Away Conceded 2.5 %</label><input type='number' step='any' inputmode='decimal' name='ac25'></div>
    <div><label>Home Conceded 3.5 %</label><input type='number' step='any' inputmode='decimal' name='hc35'></div>
    <div><label>Away Conceded 3.5 %</label><input type='number' step='any' inputmode='decimal' name='ac35'></div>
    <div><label>Home Conceded 4.5 %</label><input type='number' step='any' inputmode='decimal' name='hc45'></div>
    <div><label>Away Conceded 4.5 %</label><input type='number' step='any' inputmode='decimal' name='ac45'></div>
    <div><label>Home Conceded 5.5 %</label><input type='number' step='any' inputmode='decimal' name='hc55'></div>
    <div><label>Away Conceded 5.5 %</label><input type='number' step='any' inputmode='decimal' name='ac55'></div>
  </div>
</div>

<div class='card'>
  <h3>⚙️ Context</h3>
  <label>League Avg Corners/Match (e.g. 9.8)</label>
  <input type='number' step='any' inputmode='decimal' name='league' placeholder='e.g. 9.8'>
  <label>League Tempo vs World</label>
  <select name='tempo'>
    <option value='Normal' selected>Normal</option>
    <option value='Low'>Low</option>
    <option value='High'>High</option>
  </select>
  <label>Favorite Team</label>
  <select name='fav'>
    <option value='N/A' selected>N/A</option>
    <option value='H'>Home</option>
    <option value='A'>Away</option>
  </select>
</div>

<button id='runCorners' type='button'>🔮 Run Model</button>
</form>

<div id='cornersOutput' class='output'></div>

<script>
function num(v){ const x=parseFloat(v); return isNaN(x)? null : x; }
function mean(arr){ const xs=arr.map(num).filter(v=>v!==null); return xs.length? xs.reduce((a,b)=>a+b,0)/xs.length : null; }
function clamp(x){ if(x===null) return null; return Math.max(0, Math.min(100, x)); }
function tier(p){
  if(p===null) return "N/A";
  if(p>=75) return "💎 Strong Over";
  if(p>=60) return "🔥 Lean Over";
  if(p>=45) return "⚖️ Neutral";
  if(p>=30) return "⚠️ Lean Under";
  return "❌ Strong Under";
}

function ctxAdj(league, tempo, fav){
  let t = tempo==="High"?4 : tempo==="Low"?-3 : 0;
  let f = fav==="H"?2 : fav==="A"?-1 : 0;
  let la = 0;
  if(league!==null){ la = league>10?3 : (league<8?-3:0); }
  return t+f+la;
}

function pressureIndex(vals){
  // pressure from Earned/Conceded bands 3.5 & 4.5
  const mid = mean([vals.he35, vals.ae35, vals.hc35, vals.ac35, vals.he45, vals.ae45, vals.hc45, vals.ac45]) ?? 50;
  let p = (mid - 50)/4.5; if(p>5)p=5; if(p<-5)p=-5; return p;
}

const kMap = {"6.5":1.0, "7.5":1.2, "8.5":1.4, "9.5":1.6, "10.5":1.8};

function probLine(line, vals){
  // base from totals
  const pair = {"6.5":["ht65","at65"], "7.5":["ht75","at75"], "8.5":["ht85","at85"], "9.5":["ht95","at95"], "10.5":["ht105","at105"]}[line];
  let base = mean([vals[pair[0]], vals[pair[1]]]) ?? 50;
  const press = pressureIndex(vals);
  const ctx   = ctxAdj(vals.league, vals.tempo, vals.fav);
  return clamp(base + kMap[line]*press + ctx);
}

document.getElementById('runCorners').addEventListener('click', ()=>{
  const f = document.getElementById('cornersForm');
  const fd = new FormData(f);
  const vals = {};
  ["ht65","at65","ht75","at75","ht85","at85","ht95","at95","ht105","at105",
   "he25","ae25","he35","ae35","he45","ae45","he55","ae55",
   "hc25","ac25","hc35","ac35","hc45","ac45","hc55","ac55","league"].forEach(k=> vals[k]=num(fd.get(k)));
  vals['tempo'] = fd.get('tempo');
  vals['fav']   = fd.get('fav');

  const r = {
    "Over 6.5 Corners":  probLine("6.5", vals),
    "Over 7.5 Corners":  probLine("7.5", vals),
    "Over 8.5 Corners":  probLine("8.5", vals),
    "Over 9.5 Corners":  probLine("9.5", vals),
    "Over 10.5 Corners": probLine("10.5", vals)
  };

  let lines = "";
  Object.entries(r).forEach(([k,v])=>{
    const badge = tier(v);
    const emoji = badge==="N/A" ? "❔" : badge.split(" ")[0];
    const val = v===null ? "N/A" : v.toFixed(1)+"%";
    lines += `<div class='card'>${emoji} <b>${k}</b> → <b>${val}</b> <span class='badge'>${badge}</span></div>`;
  });

  document.getElementById('cornersOutput').innerHTML = `
    <div class='card'><b>GETO CORNERS MODEL OUTPUT</b><div class='sep'></div>${lines}
    <div class='sep'></div><div class='info'>Model blends totals base + earned/conceded pressure + tempo/favorite/league context.</div></div>
  `;
});
</script>
""", unsafe_allow_html=True)
