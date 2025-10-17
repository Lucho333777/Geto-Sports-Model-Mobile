import streamlit as st

st.set_page_config(page_title="GETO Goals (Mobile)", page_icon="⚽", layout="centered")

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

<h1>⚽ GETO Goals (Mobile)</h1>
<p style='text-align:center;color:var(--muted);'>Enter % (leave blank if unknown). Native number keypad. Tap Run.</p>

<form id='goalsForm' onsubmit='return false;'>

<div class='card'>
  <h3>📊 Total Goals % (Home & Away)</h3>
  <div class="row">
    <div><label>Home Over 1.5 %</label><input type='number' step='any' inputmode='decimal' name='ht15'></div>
    <div><label>Away Over 1.5 %</label><input type='number' step='any' inputmode='decimal' name='at15'></div>
    <div><label>Home Over 2.5 %</label><input type='number' step='any' inputmode='decimal' name='ht25'></div>
    <div><label>Away Over 2.5 %</label><input type='number' step='any' inputmode='decimal' name='at25'></div>
    <div><label>Home Over 3.5 %</label><input type='number' step='any' inputmode='decimal' name='ht35'></div>
    <div><label>Away Over 3.5 %</label><input type='number' step='any' inputmode='decimal' name='at35'></div>
    <div><label>Home Over 4.5 %</label><input type='number' step='any' inputmode='decimal' name='ht45'></div>
    <div><label>Away Over 4.5 %</label><input type='number' step='any' inputmode='decimal' name='at45'></div>
  </div>
  <div class="info">Tip: totals drive the baseline intensity per line.</div>
</div>

<div class='card'>
  <h3>⚽ Team Goals Scored %</h3>
  <div class="row">
    <div><label>Home Over 0.5 %</label><input type='number' step='any' inputmode='decimal' name='hs05'></div>
    <div><label>Away Over 0.5 %</label><input type='number' step='any' inputmode='decimal' name='as05'></div>
    <div><label>Home Over 1.5 %</label><input type='number' step='any' inputmode='decimal' name='hs15'></div>
    <div><label>Away Over 1.5 %</label><input type='number' step='any' inputmode='decimal' name='as15'></div>
    <div><label>Home Over 2.5 %</label><input type='number' step='any' inputmode='decimal' name='hs25'></div>
    <div><label>Away Over 2.5 %</label><input type='number' step='any' inputmode='decimal' name='as25'></div>
  </div>
</div>

<div class='card'>
  <h3>🧱 Team Goals Conceded %</h3>
  <div class="row">
    <div><label>Home Conceded 0.5 %</label><input type='number' step='any' inputmode='decimal' name='hc05'></div>
    <div><label>Away Conceded 0.5 %</label><input type='number' step='any' inputmode='decimal' name='ac05'></div>
    <div><label>Home Conceded 1.5 %</label><input type='number' step='any' inputmode='decimal' name='hc15'></div>
    <div><label>Away Conceded 1.5 %</label><input type='number' step='any' inputmode='decimal' name='ac15'></div>
    <div><label>Home Conceded 2.5 %</label><input type='number' step='any' inputmode='decimal' name='hc25'></div>
    <div><label>Away Conceded 2.5 %</label><input type='number' step='any' inputmode='decimal' name='ac25'></div>
  </div>
</div>

<div class='card'>
  <h3>⚙️ Context</h3>
  <label>League Avg Goals (e.g. 2.85)</label>
  <input type='number' step='any' inputmode='decimal' name='league' placeholder='e.g. 2.85'>
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

<button id='runGoals' type='button'>🔮 Run Model</button>
</form>

<div id='goalsOutput' class='output'></div>

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
  if(league!==null){ la = league>3.0?4 : (league<2.3?-3:0); }
  return t+f+la;
}

function baseForLine(line, vals){
  // totals drive the base; fall back to scored/conceded blend
  const map = {
    "1.5": ["ht15","at15"], "2.5": ["ht25","at25"],
    "3.5": ["ht35","at35"], "4.5": ["ht45","at45"]
  };
  let base = mean(map[line].map(k=>vals[k]));
  if(base===null){
    // blend scored/conceded for near lines
    if(line==="1.5"){
      base = mean([vals.hs15, vals.as15, vals.hc15, vals.ac15, vals.ht15, vals.at15]);
    }else if(line==="2.5"){
      base = mean([vals.hs25, vals.as25, vals.hc25, vals.ac25, vals.ht25, vals.at25]);
    }else if(line==="3.5"){
      base = mean([vals.ht35, vals.at35]) ?? mean([vals.hs25, vals.as25]);
    }else{
      base = mean([vals.ht45, vals.at45]) ?? mean([vals.ht35, vals.at35]);
    }
  }
  return base===null? 50 : base;
}

function pressure(vals){
  // use 1.5 & 2.5 scored/conceded to detect attack/defense pressure
  const s = mean([vals.hs15, vals.as15, vals.hc15, vals.ac15, vals.hs25, vals.as25, vals.hc25, vals.ac25]) ?? 50;
  let gp = (s - 50)/5.0; // scale
  if(gp>5) gp=5; if(gp<-5) gp=-5;
  return gp;
}

const kMap = {"1.5":0.8, "2.5":1.2, "3.5":1.6, "4.5":2.0};

function probOver(line, vals){
  const base = baseForLine(line, vals);
  const press = pressure(vals);
  const ctx = ctxAdj(vals.league, vals.tempo, vals.fav);
  // blend toward total-intensity proxy (avg of totals around the line)
  const egi = mean([vals.ht15, vals.at15, vals.ht25, vals.at25, vals.ht35, vals.at35]) ?? 50;
  const blended = 0.6*base + 0.4*(egi ?? 50);
  return clamp(blended + kMap[line]*press + ctx);
}

document.getElementById('runGoals').addEventListener('click', ()=>{
  const f = document.getElementById('goalsForm');
  const vals = {};
  ['ht15','at15','ht25','at25','ht35','at35','ht45','at45',
   'hs05','as05','hs15','as15','hs25','as25',
   'hc05','ac05','hc15','ac15','hc25','ac25','league']
   .forEach(k=> vals[k] = num((new FormData(f)).get(k)));
  vals['tempo'] = (new FormData(f)).get('tempo');
  vals['fav']   = (new FormData(f)).get('fav');

  const r = {
    "Over 1.5 Goals": probOver("1.5", vals),
    "Over 2.5 Goals": probOver("2.5", vals),
    "Over 3.5 Goals": probOver("3.5", vals),
    "Over 4.5 Goals": probOver("4.5", vals)
  };

  let lines = "";
  Object.entries(r).forEach(([k,v])=>{
    const badge = tier(v);
    const emoji = badge==="N/A" ? "❔" : badge.split(" ")[0];
    const val = v===null ? "N/A" : v.toFixed(1)+"%";
    lines += `<div class='card'>${emoji} <b>${k}</b> → <b>${val}</b> <span class='badge'>${badge}</span></div>`;
  });

  document.getElementById('goalsOutput').innerHTML = `
    <div class='card'><b>GETO GOALS MODEL OUTPUT</b><div class='sep'></div>${lines}
    <div class='sep'></div><div class='info'>Model uses totals as base, scored/conceded pressure, plus tempo/favorite/league context.</div></div>
  `;
});
</script>
""", unsafe_allow_html=True)
