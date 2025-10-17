import streamlit as st
from utils import avg, to_num, clamp01, tier_label, parlay_preview

st.set_page_config(page_title="GETO Corners (Mobile)", page_icon="🏁", layout="centered")

# ===== Mobile-first CSS + keypad =====
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

st.markdown("<h1 style='text-align:center'>🏁 GETO Corners — Mobile</h1>", unsafe_allow_html=True)
st.caption("Fill %s. Leave blank if unknown. Mobile keypad enforced. Lines: totals 6.5–10.5; team 2.5–5.5.")

# ==== Inputs ====
st.markdown("### Total Corners (Over %)")
h_65 = st.text_input("Home Over 6.5 %", "", placeholder="%")
h_75 = st.text_input("Home Over 7.5 %", "", placeholder="%")
h_85 = st.text_input("Home Over 8.5 %", "", placeholder="%")
h_95 = st.text_input("Home Over 9.5 %", "", placeholder="%")
h_105= st.text_input("Home Over 10.5 %", "", placeholder="%")

a_65 = st.text_input("Away Over 6.5 %", "", placeholder="%")
a_75 = st.text_input("Away Over 7.5 %", "", placeholder="%")
a_85 = st.text_input("Away Over 8.5 %", "", placeholder="%")
a_95 = st.text_input("Away Over 9.5 %", "", placeholder="%")
a_105= st.text_input("Away Over 10.5 %", "", placeholder="%")

st.markdown("### Team Corners Earned (Over %)")
he_25 = st.text_input("Home Over 2.5 %", "", placeholder="%")
he_35 = st.text_input("Home Over 3.5 %", "", placeholder="%")
he_45 = st.text_input("Home Over 4.5 %", "", placeholder="%")
he_55 = st.text_input("Home Over 5.5 %", "", placeholder="%")

ae_25 = st.text_input("Away Over 2.5 %", "", placeholder="%")
ae_35 = st.text_input("Away Over 3.5 %", "", placeholder="%")
ae_45 = st.text_input("Away Over 4.5 %", "", placeholder="%")
ae_55 = st.text_input("Away Over 5.5 %", "", placeholder="%")

st.markdown("### Team Corners Conceded (Over %)")
hc_25 = st.text_input("Home Conceded 2.5 %", "", placeholder="%")
hc_35 = st.text_input("Home Conceded 3.5 %", "", placeholder="%")
hc_45 = st.text_input("Home Conceded 4.5 %", "", placeholder="%")
hc_55 = st.text_input("Home Conceded 5.5 %", "", placeholder="%")

ac_25 = st.text_input("Away Conceded 2.5 %", "", placeholder="%")
ac_35 = st.text_input("Away Conceded 3.5 %", "", placeholder="%")
ac_45 = st.text_input("Away Conceded 4.5 %", "", placeholder="%")
ac_55 = st.text_input("Away Conceded 5.5 %", "", placeholder="%")

st.markdown("### Context")
league_avg = st.text_input("League Avg Corners/Match (e.g. 9.8)", value="", placeholder="e.g. 9.8")
tempo = st.radio("League Tempo vs World", ["Low","Normal","High"], horizontal=True, index=1)
fav   = st.radio("Favorite Team", ["H","A","N/A"], horizontal=True, index=2)

# ==== Model (upgraded) ====
k_map = {"6.5":1.0, "7.5":1.2, "8.5":1.4, "9.5":1.6, "10.5":1.8}

def _pressure_index():
    mids = [he_35, ae_35, hc_35, ac_35, he_45, ae_45, hc_45, ac_45]
    mid = avg(mids) or 50.0
    return max(-5.0, min(5.0, (mid - 50.0)/4.5))

def _context_adj():
    t = {"Low":-3,"Normal":0,"High":4}[tempo]
    f = {"H":2,"A":-1,"N/A":0}[fav]
    la = 0
    try:
        L = float(league_avg)
        la = 3 if L>10 else (-3 if L<8 else 0)
    except:
        pass
    return t + f + la

def _pair_mean(hv, av): return avg([hv, av]) or 50.0

def prob_line(L, hv, av):
    base = _pair_mean(hv, av)
    press = _pressure_index()
    ctx = _context_adj()
    return clamp01(base + k_map[L]*press + ctx)

# ===== Run =====
st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
run = st.button("🔮 Run Model")
st.markdown("</div>", unsafe_allow_html=True)

if run:
    results = {
        "6.5": prob_line("6.5", h_65, a_65),
        "7.5": prob_line("7.5", h_75, a_75),
        "8.5": prob_line("8.5", h_85, a_85),
        "9.5": prob_line("9.5", h_95, a_95),
        "10.5": prob_line("10.5", h_105, a_105)
    }

    st.markdown("### Results")
    st.markdown("<div class='output'>", unsafe_allow_html=True)
    for L, p in results.items():
        badge = tier_label(p)
        emoji = "❔" if p is None else badge.split()[0]
        val = "N/A" if p is None else f"{p:.1f}%"
        st.markdown(f"<div class='card'>{emoji} <b>Over {L} Corners</b> → <b>{val}</b> <span class='badge'>{badge}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Parlay preview examples
    st.markdown("### Parlay Preview")
    ranked = [(L,p) for L,p in results.items() if p is not None]
    ranked.sort(key=lambda x: x[1], reverse=True)
    if len(ranked) >= 2:
        (L1,p1), (L2,p2) = ranked[0], ranked[1]
        proj, syn = parlay_preview(p1, p2, kind="same_game_same_market")
        st.markdown(
            f"<div class='card'>🧮 <b>Over {L1} + Over {L2}</b><br>"
            f"Projected Hit: <b>{proj:.1f}%</b> • Synergy: <b>{syn}/100</b><br>"
            f"<span class='badge'>Same-game, same-market penalty applied</span></div>",
            unsafe_allow_html=True
        )
