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


class _Resp:
    def __init__(self, status=200, body=None, content=b"col\n1\n"):
        self.status_code, self._body, self.content, self.text = status, body if body is not None else {}, content, "x"

    def json(self):
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            import requests
            raise requests.HTTPError(f"HTTP {self.status_code}")


class _ScriptedHTTP:
    """Fake requests.Session: replays a script of responses/exceptions for .request(), counts login posts."""

    def __init__(self, script, logins_ok=True):
        self.script, self.calls, self.headers, self.logins, self.logins_ok = list(script), [], {}, 0, logins_ok

    def post(self, url, **kw):
        assert url.endswith("/login")
        self.logins += 1
        return _Resp(200, {"token": f"tok{self.logins}"}) if self.logins_ok else _Resp(401)

    def request(self, method, url, **kw):
        self.calls.append((method, url.rsplit("/", 2)[-2:], dict(self.headers)))
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _client(script, **kw):
    c = A.Client(A.Credentials("u", "p"), sleep=lambda s: None)
    c.http = _ScriptedHTTP(script, **kw)
    return c


def test_status_relogs_in_once_on_403_and_retries():
    c = _client([_Resp(403), _Resp(200, {"status": "processing"})])
    assert c.status("t") == "processing"
    assert c.http.logins == 1 and c.relogins == 1 and len(c.http.calls) == 2
    assert c.http.calls[1][2]["Authorization"] == "Bearer tok1"          # the retry carries the fresh token


def test_persistent_403_raises_after_a_single_relogin():
    c = _client([_Resp(403), _Resp(403), _Resp(200, {"status": "done"})])
    with pytest.raises(Exception):
        c.status("t")
    assert c.http.logins == 1                                          # no login storm


def test_transient_errors_back_off_and_recover():
    import requests
    waits = []
    c = A.Client(A.Credentials("u", "p"), sleep=waits.append)
    c.http = _ScriptedHTTP([requests.ConnectionError("x"), _Resp(503), _Resp(429), _Resp(200, {"status": "done"})])
    assert c.status("t") == "done"
    assert waits == [2.0, 4.0, 8.0] and c.http.logins == 0               # exponential backoff, no re-login needed


def test_submit_never_retries_a_lost_response_but_may_relogin_on_403():
    import requests
    c = _client([requests.Timeout("lost")])
    with pytest.raises(requests.Timeout):
        c.submit({"task_type": "point"})
    assert len(c.http.calls) == 1                                       # a retry could create a duplicate task
    c = _client([_Resp(403), _Resp(202, {"task_id": "abc"})])
    assert c.submit({"task_type": "point"}) == "abc" and c.http.logins == 1


def test_wait_survives_failed_polls_and_logs_each_status():
    import requests
    lines = []
    c = _client([requests.ConnectionError("x")] * 6 + [_Resp(200, {"status": "pending"}), _Resp(500), _Resp(500), _Resp(500), _Resp(500), _Resp(500), _Resp(500),
                 _Resp(200, {"status": "processing"}), _Resp(200, {"status": "done"})])
    assert c.wait("t", every=0, log=lines.append) == "done"
    assert sum("poll failed" in m for m in lines) >= 1 and sum("status=" in m for m in lines) == 3


def test_wait_gives_up_after_too_many_consecutive_failures():
    import requests
    c = _client([requests.ConnectionError("x")] * 200)
    with pytest.raises(requests.ConnectionError):
        c.wait("t", every=0, max_failures=3, log=lambda m: None)


def test_download_keeps_only_result_csvs_and_sanitises_names(tmp_path):
    files = [{"file_id": "1", "file_name": "../../evil/x-MOD13Q1-061-results.csv", "file_size": 10},
             {"file_id": "2", "file_name": "x-SPL3SMP-E-006-results.csv", "file_size": 10},
             {"file_id": "3", "file_name": "x-request.json", "file_size": 10},
             {"file_id": "4", "file_name": "x-MOD13Q1-061-VI-Quality-lookup.csv", "file_size": 10},
             {"file_id": "5", "file_name": "x-OTHER-results.csv", "file_size": 10}]
    c = _client([_Resp(200, {"files": files}), _Resp(200), _Resp(200)])
    saved = c.download("task", tmp_path / "raw")
    assert sorted(p.name for p in saved) == ["x-MOD13Q1-061-results.csv", "x-SPL3SMP-E-006-results.csv"]
    assert all(p.parent == tmp_path / "raw" for p in saved) and not (tmp_path / "evil").exists()


def test_oversized_download_refused(tmp_path):
    c = _client([_Resp(200, {"files": [{"file_id": "1", "file_name": "x-MOD13Q1-061-results.csv", "file_size": 10**9}]})])
    with pytest.raises(RuntimeError, match="unexpectedly large"):
        c.download("task", tmp_path)
