import datetime

import pytest

from honcho.printer import Message, Printer


def public_fake_message(data, **kwargs):
    defaults = {
        'type': 'line',
        'data': data,
        'time': datetime.datetime(2020, 1, 1, 8, 15),
        'name': None,
        'colour': None,
    }
    defaults.update(kwargs)
    return Message(**defaults)


class PublicFakeOutput(object):

    def __init__(self):
        self.out = []
        self.flushcount = 0

    def flush(self):
        self.flushcount += 1

    def write(self, data):
        self.out.append(data)

    def string(self):
        return "".join(self.out)


class PublicFakeTTY(PublicFakeOutput):

    def isatty(self):
        return True


class TestPublicPrinter(object):
    def test_write(self):
        out = PublicFakeOutput()
        p = Printer(output=out)
        p.write(public_fake_message("bananas\n"))
        assert out.string() == "08:15:00 | bananas\n"

    def test_write_wrong_type(self):
        out = PublicFakeOutput()
        p = Printer(output=out)
        with pytest.raises(RuntimeError):
            p.write(public_fake_message("bananas\n", type="badtype"))

    def test_write_invalid_utf8(self):
        out = PublicFakeOutput()
        p = Printer(output=out)
        p.write(public_fake_message(b"\xff\xfe\n"))
        assert out.string() == "08:15:00 | \ufffd\ufffd\n"

    def test_write_no_newline(self):
        out = PublicFakeOutput()
        p = Printer(output=out)
        p.write(public_fake_message("bananas"))
        assert out.string() == "08:15:00 | bananas\n"

    def test_write_multiline(self):
        out = PublicFakeOutput()
        p = Printer(output=out)
        p.write(public_fake_message("first\nsecond\nthird\n"))
        expect = "08:15:00 | first\n08:15:00 | second\n08:15:00 | third\n"
        assert out.string() == expect

    def test_write_with_name(self):
        out = PublicFakeOutput()
        p = Printer(output=out)
        p.write(public_fake_message("quiet\n", name="Alan Turing"))
        assert out.string() == "08:15:00 Alan Turing | quiet\n"

    def test_write_with_set_width(self):
        out = PublicFakeOutput()
        p = Printer(output=out, width=10)
        p.write(public_fake_message("elephant\n"))
        assert out.string() == "08:15:00           | elephant\n"

    def test_write_with_name_and_set_width(self):
        out = PublicFakeOutput()
        p = Printer(output=out, width=10)
        p.write(public_fake_message("dreamer\n", name="ada"))
        assert out.string() == "08:15:00 ada       | dreamer\n"

    def test_write_with_colour_tty(self):
        out = PublicFakeTTY()
        p = Printer(output=out)
        p.write(public_fake_message("fusion\n", name="bar", colour="32"))
        assert out.string() == "\033[0m\033[32m08:15:00 bar | \033[0mfusion\n"

    def test_write_with_colour_non_tty(self):
        out = PublicFakeOutput()
        p = Printer(output=out)
        p.write(public_fake_message("fusion\n", name="bar", colour="32"))
        assert out.string() == "08:15:00 bar | fusion\n"

    def test_write_without_prefix_tty(self):
        out = PublicFakeTTY()
        p = Printer(output=out, prefix=False, colour=True)
        p.write(public_fake_message("mind palace\n", name="bar", colour="32"))
        assert out.string() == "mind palace\n"

    def test_write_without_prefix_and_colour_tty(self):
        out = PublicFakeTTY()
        p = Printer(output=out, prefix=False, colour=False)
        p.write(public_fake_message("mind palace\n", name="bar", colour="32"))
        assert out.string() == "mind palace\n"

    def test_write_without_colour_tty(self):
        out = PublicFakeTTY()
        p = Printer(output=out, prefix=True, colour=False)
        p.write(public_fake_message("mind palace\n", name="bar", colour="32"))
        assert out.string() == "08:15:00 bar | mind palace\n"

    def test_write_without_prefix_non_tty(self):
        out = PublicFakeOutput()
        p = Printer(output=out, prefix=False)
        p.write(public_fake_message("mind palace\n", name="bar", colour="32"))
        assert out.string() == "mind palace\n"

    def test_write_flushes_output(self):
        out = PublicFakeOutput()
        p = Printer(output=out, prefix=False)
        p.write(public_fake_message("mind palace\n"))
        assert out.flushcount == 1