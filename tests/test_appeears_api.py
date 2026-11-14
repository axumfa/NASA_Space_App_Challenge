import datetime as dt
import json
from pathlib import Path

import pytest

from fieldshift.config import DEMO_FIELDS
from fieldshift.fetch import appeears_api as A


def test_task_payload_covers_both_fields_products_and_dates():
    t = A.build_task(end=dt.date(2026, 11, 14))
    p = t["params"]
    assert t["task_type"] == "point" and p["dates"] == [{"startDate": "04-01-2015", "endDate": "11-14-2026"}]
    assert {c["id"] for c in p["coordinates"]} == set(DEMO_FIELDS)
    assert all(c["latitude"] == DEMO_FIELDS[c["id"]].lat for c in p["coordinates"])
    got = {(x["product"], x["layer"]) for x in p["layers"]}
    assert ("MOD13Q1.061", "_250m_16_days_pixel_reliability") in got and ("MOD13Q1.061", "_250m_16_days_VI_Quality") in got
    assert ("SPL3SMP_E.006", "Soil_Moisture_Retrieval_Data_AM_retrieval_qual_flag") in got
    assert not any(pv == "SPL3SMP_E.005" for pv, _ in got)        # that version does not exist in AppEEARS


def test_credentials_from_env_file_are_masked_everywhere(tmp_path, monkeypatch):
    monkeypatch.delenv("EARTHDATA_USERNAME", raising=False); monkeypatch.delenv("EARTHDATA_PASSWORD", raising=False)
    env = tmp_path / ".env"
    env.write_text("# comment\nEARTHDATA_USERNAME=alice\nexport EARTHDATA_PASSWORD='s3cret-pw'\n")
    c = A.load_credentials(env)
    assert (c.username, c.password) == ("alice", "s3cret-pw")
    for text in (repr(c), str(c), f"{c}", repr(A.Client(c))[:200]):
        assert "s3cret-pw" not in text and "alice" not in text


def test_missing_credentials_error_names_keys_not_values(tmp_path, monkeypatch):
    monkeypatch.delenv("EARTHDATA_USERNAME", raising=False); monkeypatch.delenv("EARTHDATA_PASSWORD", raising=False)
    env = tmp_path / ".env"; env.write_text("EARTHDATA_USERNAME=bob\n")
    with pytest.raises(A.CredentialsMissing) as e:
        A.load_credentials(env)
    assert "EARTHDATA_PASSWORD" in str(e.value) and "bob" not in str(e.value)


class _FakeHTTP:
    def __init__(self, files):
        self.files, self.headers = files, {}

    def get(self, url, timeout=0):
        class R:
            status_code = 200
            def __init__(s, url): s.url = url
            def raise_for_status(s): pass
            def json(s): return {"files": self_files}
            @property
            def content(s): return b"col\n1\n"
        self_files = self.files
        return R(url)


def test_download_keeps_only_result_csvs_and_sanitises_names(tmp_path):
    files = [{"file_id": "1", "file_name": "../../evil/x-MOD13Q1-061-results.csv", "file_size": 10},
             {"file_id": "2", "file_name": "x-SPL3SMP-E-006-results.csv", "file_size": 10},
             {"file_id": "3", "file_name": "x-request.json", "file_size": 10},
             {"file_id": "4", "file_name": "x-MOD13Q1-061-VI-Quality-lookup.csv", "file_size": 10},
             {"file_id": "5", "file_name": "x-OTHER-results.csv", "file_size": 10}]
    c = A.Client(A.Credentials("u", "p")); c.http = _FakeHTTP(files)
    saved = c.download("task", tmp_path / "raw")
    assert sorted(p.name for p in saved) == ["x-MOD13Q1-061-results.csv", "x-SPL3SMP-E-006-results.csv"]
    assert all(p.parent == tmp_path / "raw" for p in saved) and not (tmp_path / "evil").exists()


def test_oversized_download_refused(tmp_path):
    c = A.Client(A.Credentials("u", "p")); c.http = _FakeHTTP([{"file_id": "1", "file_name": "x-MOD13Q1-061-results.csv", "file_size": 10**9}])
    with pytest.raises(RuntimeError, match="unexpectedly large"):
        c.download("task", tmp_path)
