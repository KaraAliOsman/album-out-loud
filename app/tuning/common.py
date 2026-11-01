"""Shared helpers for the tuning bench: API client, image encoding, paths.

The API key is read from a file at call time and is never printed, logged or stored.
"""
import base64
import os
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
PROMPTS = ROOT / "prompts"
RESULTS = ROOT / "results"
TRUTH = ROOT / "truth.json"

API_URL = "https://api.primalabs.ai/v1/chat/completions"
KEY_FILE = Path(os.environ["PRIMALABS_KEY_FILE"])

MODELS = {
    "mimo": "primalabs-ai/MiMo-V2.6-Pro",
    "nemotron": "primalabs-ai/Nemotron-3.5-Super-VL-NVFP4",
}
# Both models can reason; hidden reasoning counts against max_tokens, so a model that runs
# with thinking on gets this many extra tokens on top of the mode budget (recorded per call).
# 2000 was too few for MiMo on the long prompts (finish_reason length, empty content).
REASONING_EXTRA = {"mimo": 6000, "nemotron": 3000}
# Thinking switch accepted by both endpoints (tested): chat_template_kwargs.enable_thinking.
THINKING_OFF = {"chat_template_kwargs": {"enable_thinking": False}}


def _key():
    return KEY_FILE.read_text(encoding="utf-8").strip()


def image_data_url(path):
    data = Path(path).read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode("ascii")


def chat(model_id, messages, temperature, max_tokens, timeout=180, extra=None):
    """One POST. Returns (response_json, seconds). Raises RuntimeError on failure."""
    body = json.dumps({
        "model": model_id, "messages": messages,
        "temperature": temperature, "max_tokens": max_tokens, **(extra or {}),
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + _key(),
    })
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r), round(time.time() - t0, 2)
    except urllib.error.HTTPError as e:
        detail = e.read()[:300].decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from None
    except Exception as e:  # timeouts, connection errors
        raise RuntimeError(f"{type(e).__name__}: {e}") from None


def chat_retry(model_id, messages, temperature, max_tokens, extra=None):
    """Call once, retry once on error. Returns dict with response or error."""
    errors = []
    for attempt in (1, 2):
        try:
            resp, secs = chat(model_id, messages, temperature, max_tokens, extra=extra)
            return {"ok": True, "attempts": attempt, "seconds": secs, "response": resp, "errors": errors}
        except RuntimeError as e:
            errors.append(str(e))
            if attempt == 1:
                time.sleep(3)
    return {"ok": False, "attempts": 2, "seconds": None, "response": None, "errors": errors}


def extract(resp):
    """Pull visible content, reasoning text length, finish reason and usage from a response."""
    if not resp:
        return {"content": None, "reasoning_chars": 0, "finish_reason": None, "usage": None}
    ch = (resp.get("choices") or [{}])[0]
    msg = ch.get("message") or {}
    content = msg.get("content")
    if isinstance(content, list):  # some servers return content parts
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
    reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
    return {
        "content": content,
        "reasoning_chars": len(reasoning) if isinstance(reasoning, str) else 0,
        "finish_reason": ch.get("finish_reason"),
        "usage": resp.get("usage"),
    }


def load_truth():
    return json.loads(TRUTH.read_text(encoding="utf-8"))


def calls_logged():
    """All API attempts logged so far by bench.py, judge.py and judge_batch.py (budget ledger)."""
    total = 0
    for name, field in (("raw.jsonl", "attempts"), ("judge.jsonl", "judge_attempts"),
                        ("judge_batch.jsonl", "judge_attempts")):
        f = RESULTS / name
        if f.exists():
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    total += json.loads(line).get(field, 1)
    return total
