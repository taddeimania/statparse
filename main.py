import os
from positions import QuarterBack, RunningBack, WideReceiver, TightEnd, Kicker, BasePosition

HOME_DIR = os.path.abspath(os.path.dirname(__file__))
stat_list = []

def get_home_and_away(byte):
    away = ""
    home = ""
    for x in range(3087, 3090):
        home += byte[x]

    for x in range(3119, 3122):
        away += byte[x]

    return [home, away]


def set_stats(byte):
    game = get_home_and_away(byte)

    home_side = True
    for side in game:
        for i in range(1, 3):
            qb1 = QuarterBack(byte, i, team=side, home=home_side)
            stat_list.append(qb1.get_stats())
        for i in range(1, 5):
            rb = RunningBack(byte, i, team=side, home=home_side)
            stat_list.append(rb.get_stats())
        for i in range(1, 5):
            wr = WideReceiver(byte, i, team=side, home=home_side)
            stat_list.append(wr.get_stats())
        for i in range(1, 3):
            te = TightEnd(byte, i, team=side, home=home_side)
            stat_list.append(te.get_stats())

        k = Kicker(byte, team=side, home=home_side)
        stat_list.append(k.get_stats())


        home_side = False

def main():
    f = open("{}/1.nst".format(HOME_DIR), "rb")
    byte = f.read()
    BasePosition.team_list = get_home_and_away(byte)
    BasePosition.get_injuries(byte)
    BasePosition.get_conditions(byte)
    set_stats(byte)
    for stats in stat_list:
        print stats

if __name__ == "__main__":
    main()