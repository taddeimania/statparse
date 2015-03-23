import os
from positions.positions import get_stats, get_injuries, get_conditions, clean_stats, Player

HOME_DIR = os.path.abspath(os.path.dirname(__file__))

qb_exclude = ["rec", "rectd", "recyds", "kr", "kryds", "krtd", "pr", "pryds", "prtd", "xpa", "xpm", "fgm", "fga"]
k_exclude = ["passatt", "comp", "passtd", "passint", "passyds", "rusat", "rusyds", "rustd", "rec", "rectd", "recyds",
             "kr", "kryds", "pr", "pryds", "krtd", "prtd"]
exclude = ["passatt", "comp", "passtd", "passint", "passyds", "xpa", "xpm", "fgm", "fga"]


def get_home_and_away(byte):
    away = ""
    home = ""
    for x in range(2629, 2632):
        home += byte[x]

    for x in range(2661, 2664):
        away += byte[x]

    return [home, away]


def set_stats(byte, team_list, conditions, injuries):
    stat_list = []

    home_side = True
    for side in team_list:
        for i in range(1, 3):
            qb1 = {"order": i, "pos": "QB", "team": side, "home": home_side}
            qb_stats = clean_stats(qb_exclude, get_stats(qb1, conditions, injuries, byte))
            stat_list.append(qb_stats)
        for i in range(1, 5):
            rb = {"order": i, "pos": "RB", "team": side, "home": home_side}
            rb_stats = clean_stats(exclude, get_stats(rb, conditions, injuries, byte))
            stat_list.append(rb_stats)
        for i in range(1, 5):
            wr = Player(i, "WR", team=side, home=home_side)
            wr = {"order": i, "pos": "WR", "team": side, "home": home_side}
            wr_stats = clean_stats(exclude, get_stats(wr, conditions, injuries, byte))
            stat_list.append(wr_stats)
        for i in range(1, 3):
            te = {"order": i, "pos": "TE", "team": side, "home": home_side}
            te_stats = clean_stats(exclude, get_stats(te, conditions, injuries, byte))
            stat_list.append(te_stats)

        k = {"order": i, "pos": "K", "team": side, "home": home_side}
        k_stats = clean_stats(k_exclude, get_stats(k, conditions, injuries, byte))
        stat_list.append(k_stats)

        home_side = False
    return stat_list


def main():
    with open("{}/1.jat".format(HOME_DIR), "rb") as f:
        byte = f.read()
    team_list = get_home_and_away(byte)
    injuries = get_injuries(byte, team_list)
    conditions = get_conditions(byte, team_list)
    stat_list = set_stats(byte, team_list, conditions, injuries)
    for stats in stat_list:
        print stats

if __name__ == "__main__":
    main()
