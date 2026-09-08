import re

# Django 3.0+ removal of ugettext_lazy compatibility
try:
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import ugettext_lazy as _

linebreak_re = re.compile(r"\r\n|\r|\n")

FIELD_CHOICES = (
    (1, _("Single line text")),
    (2, _("Multi line text")),
    (3, _("Email")),
    (4, _("Number")),
    (5, _("URL")),
    (6, _("Checkbox")),
    (7, _("Select")),
    (8, _("Multiple select")),
    (9, _("Radio buttons")),
    (10, _("File upload")),
    (11, _("Date")),
    (12, _("Date/time")),
    (13, _("Time")),
    (14, _("Hidden")),
)


def split_choices(choices):
    """
    Split a choices list, dict, or string into a list of tuples.
    Accepts:
      - a string: One value per line. "Red\nBlue" -> [("Red", "Red"), ("Blue", "Blue")]
      - a list/tuple: If it's already a list of tuples, passes unchanged.
    """
    if not choices or isinstance(choices, (int, float)):
        return []
    if isinstance(choices, (list, tuple)):
        # If already properly formatted, keep as is.
        return choices
    lines = linebreak_re.split(str(choices))
    return [(v.strip(), v.strip()) for v in lines if v.strip()]


# Alias
choices_from_lines = split_choices

FIELD_TYPES = tuple((k, v) for k, v in FIELD_CHOICES)