"""Generate src/fieldshift/crops.json from a compact table (easier to review than raw JSON).

VALUES ARE TRANSCRIBED FROM GENERAL KNOWLEDGE of FAO-56 (Allen et al. 1998, Tables 11-12) and
FAO ECOCROP; they have NOT been re-checked against the source tables line by line. Anything
listed in a crop's "approx" key is an authors' estimate. Review before the submission.
"""
import json
from pathlib import Path

FIELDS = ["name", "season", "sow", "days", "stages", "kc", "gdd_base", "gdd_req", "t_min", "t_opt",
          "t_max", "frost_kill_c", "heat_thr_c", "water_need_mm", "drought_tol", "salinity_tol",
          "n_credit", "root_m", "cover", "om", "forage", "income", "family", "market"]
# kc = (ini, mid, end); stages = days (ini, dev, mid, late)
T = {
 "cotton": ("Cotton", "summer", (100,125), 180, (30,50,55,45), (.35,1.18,.60), 15.5, 1300, 15, (22,32), 40, 0, 38, 700, .5, .6, 0, 1.4, .35, .30, .05, .85, "malvaceae", "Often sold via contracts/clusters; check current procurement terms and prices."),
 "winter_wheat": ("Winter wheat", "winter", (265,315), 250, (30,140,40,40), (.40,1.15,.25), 0, 1800, -10, (8,22), 32, -18, 32, 450, .5, .5, 0, 1.5, .60, .50, .30, .60, "small_grain", "Food-security crop; procurement/quota rules may apply locally."),
 "barley": ("Winter barley", "winter", (265,305), 230, (30,120,40,40), (.30,1.15,.25), 0, 1600, -10, (8,20), 30, -14, 32, 400, .65, .8, 0, 1.2, .60, .45, .35, .50, "small_grain", "Feed/malting market; lower price than wheat in most regions."),
 "maize": ("Maize (grain)", "summer", (100,135), 125, (20,35,40,30), (.30,1.20,.60), 10, 1500, 10, (18,30), 38, -2, 35, 600, .35, .4, 0, 1.2, .50, .55, .50, .75, "warm_grass", "Strong feed demand; drying/storage costs matter."),
 "sorghum": ("Sorghum", "summer", (120,150), 130, (20,35,45,30), (.30,1.05,.55), 10, 1400, 10, (20,32), 40, -1, 38, 450, .85, .6, 0, 1.5, .50, .50, .60, .50, "warm_grass", "Thin local market in some regions; feed use; check buyers."),
 "millet": ("Millet", "summer", (130,160), 110, (15,25,40,30), (.30,1.00,.30), 10, 1000, 10, (22,34), 42, -1, 40, 350, .90, .5, 0, 1.2, .40, .35, .50, .35, "warm_grass", "Small niche market; mostly feed/food local use."),
 "alfalfa": ("Alfalfa (1 yr stand modelled)", "perennial", (235,270), 330, (10,30,200,90), (.40,.95,.90), 5, 1500, 5, (15,28), 38, -12, 38, 900, .70, .4, 100, 2.5, .85, .80, 1.00, .65, "legume_forage", "Local hay/feed demand; livestock needed or hay sold; seed cost."),
 "mung_bean": ("Mung bean", "summer", (160,200), 70, (10,15,25,20), (.40,1.15,.35), 10, 1000, 12, (25,32), 40, 0, 38, 300, .60, .3, 30, .8, .50, .40, .30, .55, "legume_grain", "Often grown as post-wheat short-season crop; check buyers/export prices."),
 "chickpea": ("Chickpea (spring sown)", "summer", (60,90), 110, (20,30,35,25), (.40,1.00,.35), 5, 1300, 5, (15,26), 35, -4, 35, 350, .85, .3, 30, 1.2, .35, .35, .20, .60, "legume_grain_cool", "Good export demand historically; price volatile."),
 "lentil": ("Lentil (spring sown)", "summer", (60,90), 100, (20,30,30,20), (.40,1.10,.30), 5, 1100, 5, (15,25), 32, -5, 32, 300, .70, .3, 30, .8, .30, .30, .20, .60, "legume_grain_cool", "Export/food market; check local buyers."),
 "soybean": ("Soybean", "summer", (125,155), 135, (20,30,60,25), (.40,1.15,.50), 10, 1300, 10, (20,30), 38, -1.5, 35, 550, .40, .5, 30, 1.1, .45, .45, .30, .75, "legume_grain", "Large commodity market in the US; limited processing in Central Asia."),
 "sunflower": ("Sunflower", "summer", (100,135), 130, (25,35,45,25), (.35,1.05,.35), 6, 1500, 8, (18,28), 38, -2, 36, 550, .75, .5, 0, 2.0, .45, .45, .30, .70, "asteraceae", "Oil crush demand; check local processors."),
 "safflower": ("Safflower", "summer", (60,100), 140, (25,35,55,25), (.35,1.15,.25), 5, 1500, 5, (18,28), 38, -4, 36, 450, .85, .7, 0, 2.0, .35, .40, .25, .45, "asteraceae", "Niche oil/dye market; few buyers in many regions."),
 "rapeseed": ("Winter rapeseed", "winter", (235,265), 300, (40,90,100,70), (.35,1.15,.35), 0, 1800, -8, (10,22), 32, -15, 30, 450, .50, .5, 0, 1.2, .50, .45, .15, .65, "brassica", "Oil crush demand; needs a nearby processor; winter-kill risk."),
 "rye_cover": ("Winter rye cover crop", "cover", (262,305), 190, (30,60,60,40), (.40,.85,.50), 0, 0, -15, (5,20), 30, -30, 35, 250, .75, .7, 0, 1.5, .95, .70, .20, -.12, "cover_rye", "No direct sale; ~USD 60-100/ha seed+termination (rough); may be grazed."),
 "hairy_vetch": ("Hairy vetch cover crop", "cover", (250,290), 200, (30,60,70,40), (.40,.95,.50), 0, 0, -5, (8,22), 32, -20, 32, 280, .60, .3, 80, 1.0, .85, .75, .40, -.18, "legume_cover", "No direct sale; seed costly/hard to find (~USD 100/ha incl. termination, rough); N credit for next crop."),
 "clover": ("Berseem/crimson clover cover", "cover", (255,290), 190, (30,60,60,40), (.40,.90,.85), 0, 0, 0, (12,24), 34, -8, 34, 350, .45, .5, 70, .9, .85, .70, .45, -.08, "legume_forage", "Forage value (hay/grazing); seed availability varies."),
 "potato": ("Potato", "summer", (90,115), 130, (25,30,45,30), (.50,1.15,.75), 5, 1200, 7, (14,22), 30, -1, 30, 550, .30, .3, 0, .6, .30, .30, .10, .90, "solanaceae", "High value but high cost, storage and price risk."),
 "melon": ("Melon", "summer", (105,135), 120, (25,35,40,20), (.50,1.05,.75), 12, 1100, 12, (24,32), 40, 0, 38, 450, .50, .5, 0, 1.2, .30, .25, .10, .80, "cucurbit", "High value local/regional demand; labour intensive; perishable."),
 "sugar_beet": ("Sugar beet", "summer", (75,105), 180, (30,45,90,15), (.35,1.20,.70), 3, 1800, 5, (15,25), 35, -4, 33, 700, .45, .8, 0, 1.2, .40, .40, .50, .70, "chenopod", "Needs a sugar factory within reach; contract-based."),
}
APPROX = ["gdd_req", "heat_thr_c", "frost_kill_c", "drought_tol", "salinity_tol", "n_credit", "cover",
          "om", "forage", "income", "stages", "water_need_mm", "t_opt"]
# Seasonal Ky: FAO Irrigation & Drainage Paper 33, Table 1 (read from the reproduction in FAO paper 66, Table 1).
# value, note. "analog" = a different species in the same FAO group, used as a stand-in.
KY = {"cotton": (0.85, ""), "winter_wheat": (1.05, ""), "maize": (1.25, ""), "soybean": (0.85, ""),
      "sorghum": (0.90, ""), "alfalfa": (1.10, ""), "sunflower": (0.95, ""), "safflower": (0.80, ""),
      "sugar_beet": (1.00, ""), "potato": (1.10, ""),
      "mung_bean": (1.15, "analog: FAO 'beans'"), "chickpea": (1.15, "analog: FAO 'peas'"),
      "lentil": (1.15, "analog: FAO 'peas'"), "melon": (1.10, "analog: FAO 'watermelon'")}
SRC = {
 "kc_and_stages": "Kc ini/mid/end checked against FAO-56 Table 12 (fetched from fao.org); stage lengths are from memory of FAO-56 Table 11 and were NOT re-checked; hairy vetch and cereal-rye cover Kc are analogues (approx)",
 "ky": "FAO-33 seasonal Ky (Table 1 of FAO paper 66 reproduces it) where listed; otherwise fallback 0.6+0.9*(1-drought_tol), flagged approx",
 "gdd_base_cotton": "15.5 C = cotton DD60 convention, from memory; FAO paper 66 does not state a cotton base temperature",
 "temperature": "FAO ECOCROP-style ranges (t_min, t_opt, t_max); cover crops from extension-service guidance",
 "gdd": "GDD base and requirement approximate, from cultivar-group literature (modified method, cap 30 C)",
 "trait_scores": "cover/om/forage/income/drought/salinity: 0-1 authors' relative estimates (income index 1 ~ USD 600-700/ha gross margin, rough; cover crops are negative = seed+termination cost; cover-crop forage halved because it is not a harvested crop)",
 "n_credit": "approx. net N credit to the following crop, kg N/ha (extension-service ranges)",
 "sow_doy": "typical sowing window, day of year, mid-latitude northern hemisphere (Central Asia / US Plains)",
}
out = {"_meta": {"warning": "Transcribed from general knowledge, approximate. Review before relying on it.",
                 "units": "see field names; scores 0-1; kc dimensionless; t in C; water mm",
                 "gdd_cap_c": 30.0}, "crops": {}}
for cid, row in T.items():
    d = dict(zip(FIELDS, row))
    d["sow_doy"] = list(d.pop("sow")); d["stages"] = list(d["stages"])
    d["kc"] = dict(zip(["ini", "mid", "end"], d["kc"])); d["t_opt"] = list(d["t_opt"])
    d["n_fixing"] = d["n_credit"] > 0
    d["market_note"] = d.pop("market")
    d["sources"] = SRC
    if cid in KY:
        d["ky"], note = KY[cid]
        d["ky_source"] = "FAO-33 Table 1" + (f" ({note})" if note else "")
        d["approx"] = list(APPROX)
        if note:
            d["approx"].append("ky")
    else:
        d["ky"] = round(0.6 + 0.9 * (1 - d["drought_tol"]), 2)
        d["ky_source"] = "fallback formula 0.6+0.9*(1-drought_tol)"
        d["approx"] = APPROX + ["ky"]
    if cid == "alfalfa":
        d["notes"] = ("Simplification: modelled as a 1-year stand (establishment + one production year). A real "
                      "3-year stand does not fit the 1-3 year rotation cycle used here; longer stands would add benefit not modelled.")
    out["crops"][cid] = d
Path("src/fieldshift/crops.json").write_text(json.dumps(out, indent=1))
print(len(out["crops"]), "crops written")
