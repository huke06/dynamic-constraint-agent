"""DeepSeek chat client with per-call accounting. Credentials stay in memory."""
import json, sys, time, urllib.request
from pathlib import Path
import httpx
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from probe_deepseek import credential  # reads env var or the prior session file


class Ledger:
    """Token/latency accounting grouped by call kind."""

    def __init__(self):
        self.calls = []

    def add(self, record):
        self.calls.append(record)

    def totals(self):
        out = {}
        for c in self.calls:
            kind = c['kind']
            m = out.setdefault(kind, {'calls': 0, 'seconds': 0.0, 'prompt_tokens': 0,
                                      'completion_tokens': 0, 'total_tokens': 0,
                                      'reasoning_tokens': 0, 'cache_hit_tokens': 0,
                                      'errors': 0})
            m['calls'] += 1
            m['seconds'] += c.get('seconds', 0.0)
            u = (c.get('response') or {}).get('usage') or {}
            m['prompt_tokens'] += u.get('prompt_tokens', 0) or 0
            m['completion_tokens'] += u.get('completion_tokens', 0) or 0
            m['total_tokens'] += u.get('total_tokens', 0) or 0
            m['reasoning_tokens'] += ((u.get('completion_tokens_details') or {}).get('reasoning_tokens') or 0)
            m['cache_hit_tokens'] += u.get('prompt_cache_hit_tokens', 0) or 0
            if 'error' in c:
                m['errors'] += 1
        return out


class DeepSeek:
    def __init__(self, model='deepseek-flash', ledger=None, timeout=240):
        self.model = model
        self.ledger = ledger or Ledger()
        self.secret = credential()
        proxy = urllib.request.getproxies().get('https')
        self.client = OpenAI(api_key=self.secret, base_url='https://api.deepseek.com',
                             max_retries=0, timeout=timeout,
                             http_client=httpx.Client(proxy=proxy, timeout=timeout))

    def chat(self, kind, messages, tools=None, tool_choice=None, thinking=False,
             max_tokens=1024, temperature=0.0, retries=1):
        request = {'model': self.model, 'messages': messages, 'max_tokens': max_tokens,
                   'temperature': temperature,
                   'extra_body': {'thinking': {'type': 'enabled' if thinking else 'disabled'}}}
        if tools:
            request['tools'] = tools
            request['tool_choice'] = tool_choice or 'auto'
        error = None
        for attempt in range(retries + 1):
            record = {'kind': kind, 'request': request, 'started': time.time(), 'attempt': attempt}
            started = time.perf_counter()
            try:
                response = self.client.chat.completions.create(**request)
                raw = response.model_dump(exclude_none=True)
                record['response'] = raw
                record['seconds'] = time.perf_counter() - started
                self.ledger.add(record)
                choice = record['response']['choices'][0]
                if choice.get('finish_reason') == 'length':
                    record['truncated'] = True
                return record
            except Exception as exc:  # transient transport/first-byte problems only
                error = type(exc).__name__ + ': ' + str(exc)
                record['error'] = error
                record['seconds'] = time.perf_counter() - started
                self.ledger.add(record)
                if attempt >= retries:
                    break
        raise RuntimeError(error)

    def close(self):
        self.client.close()