from base_position import BasePosition

class QuarterBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.exclude = ["rec", "rectd", "recyds", "kr", "kryds", "krtd", "pr",
                        "pryds", "prtd", "xpa", "xpm", "fgm", "fga"]
        self.pos = "QB{}".format(order)
        super(QuarterBack, self).__init__(statfile, order, **kwargs)

class RunningBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.pos = "RB{}".format(order)
        super(RunningBack, self).__init__(statfile, order, **kwargs)

class WideReceiver(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.pos = "WR{}".format(order)
        super(WideReceiver, self).__init__(statfile, order, **kwargs)

class TightEnd(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.pos = "TE{}".format(order)
        super(TightEnd, self).__init__(statfile, order, **kwargs)

class Kicker(BasePosition):

    def __init__(self, statfile, **kwargs):
        self.pos = "K"
        self.exclude = ["passatt", "comp", "passtd", "passint", "passyds", "rusat", "rusyds", "rustd", "rec", "rectd",
                        "recyds", "kr", "kryds", "pr", "pryds", "krtd", "prtd"]
        super(Kicker, self).__init__(statfile, 1, **kwargs)