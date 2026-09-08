class Channel:
    def __init__(self, channel_name, *args):
        self.channel_name = channel_name
        # Simulate Java constructor overloads
        if len(args) == 0:
            self.obj = None
        elif len(args) == 1:
            if isinstance(args[0], int):
                self.obj = None  # emulate ("Sports", 3)
            else:
                self.obj = args[0]
        elif len(args) == 2:
            # ("Fun", 2, "extra")
            self.obj = args[1]
        else:
            self.obj = None

    def get_channel_name(self):
        return self.channel_name

    def set_channel_name(self, chname):
        self.channel_name = chname

    def get_obj(self):
        return self.obj

    def set_obj(self, obj):
        self.obj = obj

    def __str__(self):
        return f"Channel(channelName='{self.channel_name}', obj={self.obj})"

def test_channel_constructors_and_getters():
    c1 = Channel("News")
    assert c1.get_channel_name() == "News"

    c2 = Channel("Fun", 2, "extra")
    assert c2.get_channel_name() == "Fun"
    assert c2.get_obj() == "extra"

    c3 = Channel("Sports", 3)
    assert c3.get_channel_name() == "Sports"

    c4 = Channel("Games", "objval")
    assert c4.get_channel_name() == "Games"
    assert c4.get_obj() == "objval"

def test_channel_setters():
    c = Channel("Initial")
    c.set_channel_name("Changed")
    c.set_obj(1001)
    assert c.get_channel_name() == "Changed"
    assert c.get_obj() == 1001

def test_channel_tostring():
    c = Channel("Stringy", "val")
    s = str(c)
    assert "channelName='Stringy'" in s
    assert "obj=val" in s