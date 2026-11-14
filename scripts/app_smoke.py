"""Headless smoke test of app.py via streamlit.testing (no browser needed)."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from streamlit.testing.v1 import AppTest

def report(tag, at, t0):
    print(f"{tag}: {time.time()-t0:.0f}s exceptions={[e.value for e in at.exception]} errors={[e.value[:60] for e in at.error]} warnings={[w.value[:50] for w in at.warning]}")

at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=400)
t = time.time(); at.run(); report("fergana default", at, t)
at.session_state["lang_label"] = "O'zbekcha"; at.run(); report("language: uz", at, time.time())
print("  uz sample:", [m.value[:90] for m in at.markdown if "disclaimer" in m.value][:1])
at.session_state["lang_label"] = "English"; at.run()
t = time.time(); at.selectbox(key="field_choice__en").set_value("Central Kansas, USA").run(); report("kansas", at, t)
t = time.time(); at.selectbox(key="field_choice__en").set_value("Karakalpakstan farmland (near Nukus), Uzbekistan").run(); report("preset: Karakalpakstan", at, t)
t = time.time(); at.selectbox(key="profile__en").set_value("Water first").run(); report("water-first", at, t)
def apply_whatif(**vals):
    for k, v in vals.items():
        at.slider(key=k).set_value(v)
    [b for b in at.button if b.label == "Apply what-if"][0].click()
    at.run()
t = time.time(); at.slider(key="rain").set_value(-20); at.run(); print(f"  (slider move without Apply: {time.time()-t:.1f}s, no recompute expected)")
t = time.time(); apply_whatif(rain=-20, temp=2.0, supply=60); report("what-if applied: rain -20, +2C, supply 60%", at, t)
t = time.time(); apply_whatif(rain=-20, temp=2.0, supply=60); report("same what-if again (cache hit)", at, t)
t = time.time(); at.selectbox(key="profile__en").set_value("Income first").run(); report("profile change under what-if", at, t)
at.selectbox(key="field_choice__en").set_value("My own location").run(); report("own location", at, time.time())
at.selectbox(key="crop1__en").set_value("Winter wheat").run(); report("duplicate crop", at, time.time())
at.selectbox(key="crop1__en").set_value("Cotton").run()      # undo the duplicate-crop state
for lang in ("English", "O'zbekcha"):
    at.session_state["lang_label"] = lang; at.session_state["view"] = "options"; at.run(); report(f"options view ({lang})", at, time.time())
    at.session_state["view"] = "glossary"; at.run(); report(f"glossary view ({lang})", at, time.time())
    at.session_state["view"] = "field"; at.run(); report(f"field view ({lang})", at, time.time())
