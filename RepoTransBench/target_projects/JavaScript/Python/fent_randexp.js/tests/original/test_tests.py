# Contains the data structure from tests.js, adapted for pytest collection.
# This will be imported by test_main.py for parameterized testing.

TESTS_DICT = {
  "Pattern Flags": {
    "i": {
      "regexp": r"(?i)hey there",
      "desc": "Ignore the case of alphabetic characters"
    },
    "m": {
      "regexp": r"(?m)hip$\nhop",
      "desc": "Multiline mode. Causes ^ to match beginning of line or beginning of string. Causes $ to match end of line or end of string."
    }
  },
  "Position Matching": {
    "^": {
      "regexp": r"^The",
      "desc": "Only matdches the beginning of a string."
    },
    "$": {
      "regexp": r"and$",
      "desc": "Only matches the end of a string."
    },
    "\\b": {
      "regexp": r"ly\b",
      "desc": "Matches any word boundary (test characters must exist at the beginning or end of a word within the string)"
    },
    "\\B": {
      "regexp": r"m\Bore",
      "desc": "Matches any non-word boundary."
    },
    "Bad Regexp": {
      "regexp": [r"(?m)a^", r"b^", r"(?m)$c", r"$d", r"e\bf", r"\Bg"],
      "desc": "A string that matches these regular expressions does not exist.",
      "bad": True
    }
  },
  "Characters": {
    "Any character except []{}^$.|?*+()": {
      "regexp": r"a",
      "desc": "All charaacters except the listed special characters match a single instane of themselves."
    },
    "\\ (backslash) followed by any of []{}^$.|?*+()": {
      "regexp": r"\+",
      "desc": "A backslash escapes special characters to suppress their special meaning."
    },
    "\\0": {
      "regexp": r"nully: \0",
      "desc": "Matches NUL character."
    },
    "\\n": {
      "regexp": r"a new\nline",
      "desc": "Matches a new line character."
    },
    "\\f": {
      "regexp": r"\f",
      "desc": "Matches a form feed character."
    },
    "\\t": {
      "regexp": r"col1\tcol2\tcol3",
      "desc": "Matches a tab character."
    },
    "\\v": {
      "regexp": r"row1\vrow2",
      "desc": "Matches a vertical tab character."
    },
    "[\\b]": {
      "regexp": r"something[\b]",
      "desc": "Matches a backspace."
    },
    "\\XXX": {
      "regexp": r"\50",
      "desc": "Matches the ASCII character expressed by the octal number XXX."
    },
    "\\xXX": {
      "regexp": r"\xA9",
      "desc": "Matches the ASCII character expressed by the hex number XX."
    },
    "\\uFFFF": {
      "regexp": r"\u00A3",
      "desc": "Matches the ASCII character expressed by the UNICODE XXXX."
    }
  },
  "Character Sets": {
    "[xyz]": {
      "regexp": [r"(?i)[abcD!]", r"[a-z]", r"[0-4]", r"[a-zA-Z0-9]", r"[\w]", r"[\d]", r"[\s]", r"[\W]", r"[\D]", r"[\S]"],
      "desc": "Matches any one character enclosed in the character set. You may use a hyphen to denote range."
    },
    "[^xyz]": {
      "regexp": [r"[^AN]BC", r"[^\w]", r"[^\d]", r"[^\s]", r"[^\W]", r"[^\D]", r"[^\S]"],
      "desc": "Matches any one characer not enclosed in the character set."
    },
    "Bad Custom Sets": {
      "regexp": [r"[^\W\w]", r"[^\D\d]", r"[^\S\s]", r"[^\W\w]"],
      "desc": "A string that matches these regular expressions does not exist",
      "bad": True
    },
    ". (Dot)": {
      "regexp": r"b.t",
      "desc": "Matches any character except newline or another Unicode line terminator."
    },
    "\\w": {
      "regexp": r"\w",
      "desc": "Matches any alphanumeric character including the underscore. Equivalent to [a-zA-Z0-9]."
    },
    "\\W": {
      "regexp": r"\W",
      "desc": "Matches any single non-word character. Equivalent to [^a-zA-Z0-9]."
    },
    "\\d": {
      "regexp": r"\d\d\d\d",
      "desc": "Matches any single digit. Equivalent to [0-9]."
    },
    "\\D": {
      "regexp": r"\D",
      "desc": "Matches any non-digit, Equivalent to [^0-9]."
    },
    "\\s": {
      "regexp": r"in\sbetween",
      "desc": "Matches any single space character. Equivalent to [ \\f\\n\\r\\t\\v\\u00A0\\u1680\\u180e\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200a\\u2028\\u2029\\u2028\\u2029\\u202f\\u205f\\u3000]."
    },
    "\\S": {
      "regexp": r"\S",
      "desc": "Matches any single non-sace character. Equivalent to [^ \\f\\n\\r\\t\\v\\u00A0\\u1680\\u180e\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200a\\u2028\\u2029\\u2028\\u2029\\u202f\\u205f\\u3000]."
    }
  },
  "Repetition": {
    "{x}": {
      "regexp": r"\d{5}",
      "desc": "Matches exactly x occurrences of a regular expression."
    },
    "{x,}": {
      "regexp": r"\s{2,}",
      "desc": "Matches x or more occurrences of a regular expression."
    },
    "{x,y}": {
      "regexp": r"\d{2,4}",
      "desc": "Matches x to y number of occurrences of a regular expression."
    },
    "?": {
      "regexp": r"a\s?b",
      "desc": "Matches zero or one occurrences. Equivalent to {0,1}."
    },
    "*": {
      "regexp": r"we*",
      "desc": "Matches zero or more occurrences. Equivalent to {0,}."
    },
    "+": {
      "regexp": r"fe+d",
      "desc": "Matches one ore more occurrences. Equivalent to {1,}."
    }
  },
  "Alternation & Grouping": {
    "()": {
      "regexp": r"(abc)+(def)",
      "desc": "Grouping characters together to create a clause. May be nested. Also captures the desired subpattern."
    },
    "(?:x)": {
      "regexp": r"(?:.d){2}",
      "desc": "Matches x but does not capture it."
    },
    "| (Pipe)": {
      "regexp": r"forever|young",
      "desc": "Matches only one clause on either side of the pipe."
    }
  },
  "Back References": {
    "()\\x": {
      "regexp": [r"(\w+)\s+\1", r"(a)(\2\1)", r"(a|b){5}\1", r"(a)(b)\1\2"],
      "desc": '"\\x" (where x is a number from 1 to 9) when added to the end of a regular expression pattern allows you to back reference a subpattern within the pattern, so the value of the subpatterns is remembered and used as part of the matching.'
    }
  }
}