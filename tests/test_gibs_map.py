import json

import pytest

from fieldshift import mapview
from fieldshift.fetch import gibs

CAPS = """<Contents><Layer><ows:Title>NDVI</ows:Title><ows:Metadata xlink:href='https://x/colormaps/v1.3/MODIS_NDVI.xml' xlink:role='http://e/colormap/1.3' xlink:type='simple'/>
<ows:Identifier>MODIS_Terra_NDVI_8Day</ows:Identifier><Format>image/png</Format>
<Dimension><ows:Identifier>Time</ows:Identifier><Default>2026-11-13</Default><Value>2026-01-01/2026-11-13/P1D</Value></Dimension>
<TileMatrixSetLink><TileMatrixSet>GoogleMapsCompatible_Level9</TileMatrixSet></TileMatrixSetLink></Layer>
<Layer><ows:Identifier>IMERG_Precipitation_Rate</ows:Identifier><Format>image/png</Format>
<ows:Metadata xlink:role="http://e/colormap/1.3" xlink:href="https://x/colormaps/v1.3/P.xml"/>
<Dimension><Default>2026-11-12</Default></Dimension><TileMatrixSetLink><TileMatrixSet>GoogleMapsCompatible_Level6</TileMatrixSet></TileMatrixSetLink></Layer></Contents>"""
CMAP = """<ColorMap><Legend type="classification"><LegendEntry rgb="128,128,128" tooltip="No Data" id="0"/>
<LegendEntry rgb="241,236,236" tooltip="0.000 &#8211; 0.005" id="1"/><LegendEntry rgb="10,100,10" tooltip="0.500 &#8211; 0.510" id="2"/>
<LegendEntry rgb="0,24,1" tooltip="&#8805; 1.000" id="3"/></Legend></ColorMap>"""


def test_capabilities_parse_both_attribute_orders():
    a = gibs.parse_capabilities(CAPS, "MODIS_Terra_NDVI_8Day")
    b = gibs.parse_capabilities(CAPS, "IMERG_Precipitation_Rate")
    assert a == {"date": "2026-11-13", "tms": "GoogleMapsCompatible_Level9", "ext": "png", "colormap": "https://x/colormaps/v1.3/MODIS_NDVI.xml"}
    assert b["colormap"].endswith("P.xml") and b["date"] == "2026-11-12"
    assert gibs.parse_capabilities(CAPS, "NoSuchLayer") is None


def test_colormap_skips_nodata_and_gives_range_and_gradient():
    lg = gibs.parse_colormap(CMAP)
    assert lg.stops == [(241, 236, 236), (10, 100, 10), (0, 24, 1)] and (lg.vmin, lg.vmax) == (0.0, 1.0)
    assert lg.css_gradient().startswith("linear-gradient(to right,rgb(241, 236, 236) 0%")
    k = gibs.parse_colormap(CMAP.replace("0.000 &#8211; 0.005", "&lt; 200.0").replace("&#8805; 1.000", "&#8805; 350.0")
                            .replace("0.500 &#8211; 0.510", "300.0 &#8211; 301.0"), kelvin=True)
    assert round(k.vmin, 2) == round(200 - 273.15, 2) and round(k.vmax, 2) == round(350 - 273.15, 2)


class FakeResp:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


class FakeSession:
    def __init__(self, fail=False):
        self.fail, self.calls = fail, []

    def get(self, url, timeout=None):
        self.calls.append(url)
        if self.fail:
            raise ConnectionError("offline")
        return FakeResp(CAPS if url == gibs.CAPS_URL else CMAP)


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(gibs, "CACHE_DIR", tmp_path)
    return tmp_path


def test_load_caches_metadata_and_unlisted_layers_are_unavailable(cache_dir):
    s = FakeSession()
    out = gibs.load_layers(s, now=1000.0)
    assert out["ndvi"].ok and out["ndvi"].date == "2026-11-13" and out["ndvi"].legend.vmax == 1.0
    assert not out["soil"].ok and "not listed" in out["soil"].reason          # the fake capabilities do not contain it
    assert json.loads((cache_dir / "gibs_layers.json").read_text())["layers"]["ndvi"]["date"] == "2026-11-13"


def test_offline_without_cache_is_unavailable_never_invented(cache_dir):
    out = gibs.load_layers(FakeSession(fail=True), now=5.0)
    assert all(not l.ok and l.date == "" and "could not be reached" in l.reason for l in out.values())
    m = mapview.build_map(40.4, 71.7, out)
    html = m.get_root().render()
    assert "gibs.earthdata.nasa.gov" not in html                              # no data layer is offered
    assert all(not ok for *_, ok in mapview.layer_status(out))
    assert "World_Imagery" in html and "tile.openstreetmap.org" in html and "opentopomap" in html


def test_offline_with_old_cache_marks_layers_stale(cache_dir):
    gibs.load_layers(FakeSession(), now=1.0)
    out = gibs.load_layers(FakeSession(fail=True), now=1.0 + gibs.CACHE_TTL_S + 5)
    assert out["ndvi"].ok and out["ndvi"].stale
    assert mapview.layer_status(out)[0][1].endswith("*")


def test_map_contains_real_tile_urls_attribution_and_marker(cache_dir):
    out = gibs.load_layers(FakeSession(), now=1.0)
    for lang in ("en", "uz"):
        html = mapview.build_map(40.43, 71.70, out, lang, tooltip="x").get_root().render()
        assert "MODIS_Terra_NDVI_8Day/default/2026-11-13/GoogleMapsCompatible_Level9/{z}/{y}/{x}.png" in html
        assert "Esri" in html and "OpenStreetMap contributors" in html and "NASA GIBS / EOSDIS" in html
        assert "circleMarker" in html and "fs-maplegend" in html
    from fieldshift.i18n import tr
    assert json.dumps(tr("map.base_sat", "uz"))[1:-1] in html and "Sun'iy yo'ldosh" in tr("map.base_sat", "uz")
