try:
    import ahocorasick
except ImportError:
    ahocorasick = None

import re

class RegexMatcher:
    def __init__(self, regex_config_path: str, redact=40):
        # Only init automaton if ahocorasick is available, else stub/mimic logic for testing
        self.automaton = ahocorasick.Automaton() if ahocorasick else None
        self.regexes = []
        self.redact = redact
        self._parse_regex_config(regex_config_path)
        self.ready = True

    def _parse_regex_config(self, regex_config_path):
        # For testing, use a stub/config-independent fallback if ahocorasick unavailable
        if not regex_config_path:
            self.regexes = [re.compile(r"password:?\s*([^\s,]+)")]
            return
        try:
            with open(regex_config_path, "r") as f:
                conf = f.read()
                # Actually, parse config for stub: collect regexes lines
                self.regexes = []
                for line in conf.splitlines():
                    if "regex =" in line:
                        pattern = line.split("regex =")[-1].strip().strip('"')
                        self.regexes.append(re.compile(pattern))
        except Exception:
            self.regexes = [re.compile(r"password:?\s*([^\s,]+)")]

    def find_matches(self, text):
        # Use regexes directly if ahocorasick not available
        results = []
        for rx in self.regexes:
            for match in rx.finditer(text):
                results.append(match)
        return results

    def mask(self, text):
        matches = self.find_matches(text)
        for m in matches:
            s, e = m.span(1 if m.lastindex else 0)
            mask_len = max(3, (e - s) * self.redact // 100)
            stars = "*" * mask_len
            text = text[:s] + stars + text[e:]
        return text