import streamlit as st
from utils import avg, to_num, clamp01, tier_label, parlay_preview

st.set_page_config(page_title="GETO Goals (Mobile)", page_icon="⚽", layout="centered")

# ===== Mobile-first CSS + keypad enforcement (no JS fetches) =====
st.markdown("""
<style>
:root { --bg:#0b1220; --card:#0f172a; --ink:#e5e7eb; --muted:#93a3b8; --border:#1f2937; --grad:linear-gradient(90deg,#3b82f6,#60a5fa); }
[data-testid="stAppViewContainer"]{background:var(--bg);}
*{font-family:Inter, system-ui; color:var(--ink);}
h1,h2,h3{font-weight:800;}
.card{background:var(--card); border:1px solid var(--border); border-radius:16px; padding:14px; box-shadow:0 4px 12px rgba(0,0,0,.25);}
.stTextInput input{background:var(--card) !important; border:1px solid var(--border) !important;
  border-radius:12px; height:48px; font-size:16px; text-align:center; color:var(--ink) !important;}
input[type="text"]::placeholder{color:#64748b;}
.btn-primary button{width:100%; height:52px; border-radius:14px; border:none; background:var(--grad); color:white; font-weight:800; font-size:18px;}
.badge{font-size:12px; color:var(--muted); border:1px solid var(--border); padding:3px 8px; border-radius:10px;}
.output{display:flex; gap:10px; flex-direction:column;}
</style>
<script>
window.addEventListener('load', () => {
  document.querySelectorAll('input[type="text"]').forEach(e => {
    e.setAttribute('inputmode','decimal'); e.setAttribute('pattern','[0-9]*');
  });
});
</script>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown("<h1 style='text-align:center'>⚽ GETO Goals — Mobile</h1>", unsafe_allow_html=True)
st.caption("Enter team % (FootyStats). Leave blank if unknown. Mobile keypad enforced.")

# ===== Inputs (single-column, tap-friendly) =====
st.markdown("### Scored (Over %)")
h_scored_15 = st.text_input("Home Over 1.5 %", value="", placeholder="%")
h_scored_25 = st.text_input("Home Over 2.5 %", value="", placeholder="%")
h_scored_35 = st.text_input("Home Over 3.5 %", value="", placeholder="%")
a_scored_15 = st.text_input("Away Over 1.5 %", value="", placeholder="%")
a_scored_25 = st.text_input("Away Over 2.5 %", value="", placeholder="%")
a_scored_35 = st.text_input("Away Over 3.5 %", value="", placeholder="%")

st.markdown("### Conceded (Over %)")
h_conc_15 = st.text_input("Home Conceded 1.5 %", value="", placeholder="%")
h_conc_25 = st.text_input("Home Conceded 2.5 %", value="", placeholder="%")
h_conc_35 = st.text_input("Home Conceded 3.5 %", value="", placeholder="%")
a_conc_15 = st.text_input("Away Conceded 1.5 %", value="", placeholder="%")
a_conc_25 = st.text_input("Away Conceded 2.5 %", value="", placeholder="%")
a_conc_35 = st.text_input("Away Conceded 3.5 %", value="", placeholder="%")

st.markdown("### Totals (Over %)")
h_total_15 = st.text_input("Home Total 1.5 %", value="", placeholder="%")
h_total_25 = st.text_input("Home Total 2.5 %", value="", placeholder="%")
h_total_35 = st.text_input("Home Total 3.5 %", value="", placeholder="%")
a_total_15 = st.text_input("Away Total 1.5 %", value="", placeholder="%")
a_total_25 = st.text_input("Away Total 2.5 %", value="", placeholder="%")
a_total_35 = st.text_input("Away Total 3.5 %", value="", placeholder="%")

st.markdown("### BTTS (%)")
h_btts = st.text_input("Home BTTS %", value="", placeholder="%")
a_btts = st.text_input("Away BTTS %", value="", placeholder="%")

st.markdown("### Context")
league_avg_goals = st.text_input("League Avg Goals (e.g. 2.85)", value="", placeholder="e.g. 2.85")
tempo = st.radio("League Tempo vs World", ["Low","Normal","High"], horizontal=True, index=1)
fav = st.radio("Favorite Team", ["H","A","N/A"], horizontal=True, index=2)

# ===== Model logic (upgraded per plan) =====
def _context_adj():
    t = {"Low":-3,"Normal":0,"High":4}[tempo]
    f = {"H":2,"A":-1,"N/A":0}[fav]
    la = 0
    try:
        L = float(league_avg_goals)
        la = 4 if L > 3.0 else (-3 if L < 2.3 else 0)
    except:
        pass
    return t + f + la

def _egi():
    total_mid = avg([h_total_15, a_total_15, h_total_25, a_total_25, h_total_35, a_total_35]) or 50.0
    btts_mid  = avg([h_btts, a_btts]) or 50.0
    return 0.65*total_mid + 0.35*btts_mid

k_map = {"1.5":0.8, "2.5":1.2, "3.5":1.6, "4.5":2.0}

def _g_pressure():
    s = avg([h_scored_15, a_scored_15, h_conc_15, a_conc_15, h_scored_25, a_scored_25, h_conc_25, a_conc_25]) or 50.0
    return max(-5.0, min(5.0, (s - 50.0)/5.0))

def _line_base(L):
    # collect whatever exists for that line
    parts = []
    if L=="1.5":
        parts = [h_scored_15,a_scored_15,h_conc_15,a_conc_15,h_total_15,a_total_15]
    elif L=="2.5":
        parts = [h_scored_25,a_scored_25,h_conc_25,a_conc_25,h_total_25,a_total_25]
    elif L=="3.5":
        parts = [h_scored_35,a_scored_35,h_conc_35,a_conc_35,h_total_35,a_total_35]
    elif L=="4.5":
        # 4.5 often lacks per-team; we lean on totals + EGI
        parts = [h_total_35,a_total_35]  # close proxy + blended later
    return avg(parts) or 50.0

def prob_over(L):
    base = _line_base(L)
    egi  = _egi()
    blended = 0.6*base + 0.4*egi
    press = _g_pressure()
    ctx   = _context_adj()
    return clamp01(blended + k_map[L]*press + ctx)

def prob_btts():
    base = avg([h_btts, a_btts]) or 50.0
    ctx  = _context_adj()
    return clamp01(base + 0.35*_g_pressure() + ctx)

# ===== Run =====
st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
run = st.button("🔮 Run Model")
st.markdown("</div>", unsafe_allow_html=True)

if run:
    st.markdown("### Results")
    results = {
        "Over 1.5 Goals": prob_over("1.5"),
        "Over 2.5 Goals": prob_over("2.5"),
        "Over 3.5 Goals": prob_over("3.5"),
        "Over 4.5 Goals": prob_over("4.5"),
        "BTTS": prob_btts()
    }
    st.markdown("<div class='output'>", unsafe_allow_html=True)
    for name, p in results.items():
        badge = tier_label(p)
        emoji = "❔" if p is None else badge.split()[0]
        val = "N/A" if p is None else f"{p:.1f}%"
        st.markdown(f"<div class='card'>{emoji} <b>{name}</b> → <b>{val}</b> <span class='badge'>{badge}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Parlay preview (same-game same-market is conservative)
    st.markdown("### Parlay Preview")
    top = [(k,v) for k,v in results.items() if "Over" in k and v is not None]
    top.sort(key=lambda x: x[1], reverse=True)
    if len(top) >= 2:
        (k1,p1), (k2,p2) = top[0], top[1]
        proj, syn = parlay_preview(p1, p2, kind="same_game_same_market")
        st.markdown(f"<div class='card'>🧮 <b>{k1} + {k2}</b><br>Projected Hit: <b>{proj:.1f}%</b> • Synergy: <b>{syn}/100</b><br><span class='badge'>Same-game, same-market: heavy correlation penalty</span></div>", unsafe_allow_html=True)
