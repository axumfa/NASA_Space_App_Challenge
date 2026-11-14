"""Headless smoke test of app.py via streamlit.testing (no browser needed)."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from streamlit.testing.v1 import AppTest

def report(tag, at, t0):
    print(f"{tag}: {time.time()-t0:.0f}s exceptions={[e.value for e in at.exception]} errors={[e.value[:60] for e in at.error]} warnings={[w.value[:50] for w in at.warning]}")

at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=400)
t = time.time(); at.run(); report("fergana default", at, t)
t = time.time(); at.radio(key="field_choice").set_value("Central Kansas, USA").run(); report("kansas", at, t)
t = time.time(); at.selectbox(key="profile").set_value("water-first").run(); report("water-first", at, t)
t = time.time(); at.slider(key="rain").set_value(-20).run(); report("rain -20%", at, t)
t = time.time(); at.slider(key="temp").set_value(2.0).run(); report("temp +2", at, t)
t = time.time(); at.slider(key="supply").set_value(60).run(); report("supply 60%", at, t)
at.radio(key="field_choice").set_value("My own location").run(); report("own location", at, time.time())
at.selectbox(key="crop1").set_value("winter_wheat").run(); report("duplicate crop", at, time.time())
