# Shared math + labels used by both models

def to_num(x):
    try:
        return float(x)
    except:
        return None

def avg(vals):
    xs = [to_num(v) for v in vals if to_num(v) is not None]
    return round(sum(xs)/len(xs), 2) if xs else None

def clamp01(x):
    if x is None:
        return None
    return max(0.0, min(100.0, x))

def tier_label(p):
    if p is None: return "N/A"
    if p >= 75:  return "💎 Strong Over"
    if p >= 60:  return "🔥 Lean Over"
    if p >= 45:  return "⚖️ Neutral"
    if p >= 30:  return "⚠️ Lean Under"
    return "❌ Strong Under"

def synergy_penalty(kind: str) -> float:
    # correlations for parlay preview
    return {
        "same_game_same_market": 0.40,
        "same_game_cross_market": 0.20,
        "diff_game": 0.05
    }.get(kind, 0.10)

def parlay_preview(p1, p2, kind="same_game_cross_market"):
    if p1 is None or p2 is None:
        return None, None
    q1, q2 = p1/100.0, p2/100.0
    pen = synergy_penalty(kind)
    proj = 100.0 * (q1 * q2) * (1.0 - pen)
    synergy = round(((p1 + p2)/2.0) * (1.0 - pen))
    return round(proj, 1), max(0, min(100, synergy))
