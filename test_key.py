"""Quick check that your Anthropic API key works. Never prints the key."""
import os
import sys
from pathlib import Path


def load_env(path=".env"):
    p = Path(__file__).parent / path
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()
key = os.environ.get("ANTHROPIC_API_KEY")
if not key:
    sys.exit("No ANTHROPIC_API_KEY found in the environment or .env")

try:
    import anthropic
except ImportError:
    sys.exit("anthropic is not installed. Run: python3 setup.py --fix")

client = anthropic.Anthropic(api_key=key)
try:
    r = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=20,
        messages=[{"role": "user", "content": "Reply with the single word: ok"}],
    )
    print("KEY OK. Claude said:", r.content[0].text.strip())
except anthropic.AuthenticationError:
    sys.exit("KEY REJECTED (401): the key is invalid or revoked.")
except anthropic.PermissionDeniedError as e:
    sys.exit(f"KEY NOT ALLOWED (403): {e}")
except anthropic.APIConnectionError as e:
    sys.exit(f"NETWORK/PROXY problem, not the key: {e}")
except anthropic.APIStatusError as e:
    sys.exit(f"API error {e.status_code}: {e}")
