import struct

from status_parser import StatusParser
from stat_map import STAT_MAP


stat_format = [
    "TEAM", "POS", "WK", "PASATT", "PASSCOMP", "PASSTD", "PASSINT", "PASSYDS", "REC", "RECYDS", "RECTD", "RUSAT",
    "RUSYDS", "RUSTD", "KR", "KRYDS", "KRTD", "PR", "PRYDS", "PRTD", "XPA", "XPM", "FGA", "FGM", "COND", "INJ"
]

positions = ["QB1", "QB2", "RB1", "RB2", "RB3", "RB4", "WR1", "WR2", "WR3", "WR4", "TE1", "TE2"]
conditions_dict = {"11": "Excellent", "10": "Good", "01": "Average", "00": "Bad"}
position_offset = {'QB': 0, 'RB': 26, 'WR': 90, 'TE': 154, 'K': 0}


def get_stats(player, conditions, injuries, statfile):
    base_offset, rec_offset = get_offsets(player)
    values = [player['team'], player['pos'], 1] + \
              extract_stats(player, statfile, base_offset, rec_offset) + \
             [get_player_condition(player, conditions), get_player_condition(player, injuries)]
    return dict(zip(stat_format, values))


def get_offsets(player):
    pos = player['pos']
    base_offset = position_offset[pos]
    if pos not in ["QB", 'K']:
        if player['order'] == 1:
            rec_offset = base_offset + 9
        else:
            base_offset += (16 * player['order'])
            rec_offset = base_offset - 7
    else:
        if player['order'] <= 1:
            base_offset = 0
            rec_offset = 0
        else:
            base_offset += 10
            rec_offset = 0

    if not player['home']:
        base_offset += 261
        rec_offset += 261
    return base_offset, rec_offset


def clean_stats(exclude_list, stat_list):
    for field in exclude_list:
        stat_list[field.upper()] = 0
    return stat_list


def parse_extra_data(infile, team_list, team_one_start, team_two_start):
    list_of_statuses = []
    for x in range(team_one_start, team_one_start + 3):
        list_of_statuses.append(bin(ord(infile[x]))[2:])
    for x in range(team_two_start, team_two_start + 3):
        list_of_statuses.append(bin(ord(infile[x]))[2:])

    return StatusParser(list_of_statuses, team_list, positions, infile).condition_list


def get_injuries(infile, team_list):
    return parse_extra_data(infile, team_list, 6031, 6292)


def get_conditions(infile, team_list):
    return parse_extra_data(infile, team_list, 6403, 6664)


def get_player_condition(player, conditions):
    if player['pos'] == "K":
        return "Good"
    return conditions_dict[conditions["{}{}{}".format(player['team'], player['pos'], player['order'])]]


def extract_stats(player, statfile, base_offset, rec_offset):
    rush_yards = struct.unpack('H', statfile[int(STAT_MAP['rusyds_start'] + base_offset):int(STAT_MAP['rusyds_stop'] + base_offset)])[0],
    if rush_yards > 1000:
        rush_yards = struct.unpack('B', statfile[STAT_MAP['rusyds_start'] + base_offset])[0]

    return [
        struct.unpack('B', statfile[STAT_MAP['passatt'] + base_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['comp'] + base_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['passtd'] + base_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['passint'] + base_offset])[0],
        struct.unpack('H', statfile[int(STAT_MAP['passyards_start'] + base_offset):int(STAT_MAP['passyards_stop'] + base_offset)])[0],
        struct.unpack('B', statfile[STAT_MAP['rusat'] + base_offset])[0],
        rush_yards,
        struct.unpack('B', statfile[STAT_MAP['rustd'] + base_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['rec'] + rec_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['rectd'] + rec_offset])[0],
        struct.unpack('H', statfile[int(STAT_MAP['recyds_start'] + rec_offset):int(STAT_MAP['recyds_stop'] + rec_offset)])[0],
        struct.unpack('B', statfile[STAT_MAP['kr'] + rec_offset])[0],
        struct.unpack('H', statfile[int(STAT_MAP['kryds_start'] + rec_offset):int(STAT_MAP['kryds_stop'] + rec_offset)])[0],
        struct.unpack('B', statfile[STAT_MAP['krtd'] + rec_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['pr'] + rec_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['prtd'] + rec_offset])[0],
        struct.unpack('H', statfile[int(STAT_MAP['pryds_start'] + rec_offset):int(STAT_MAP['pryds_stop'] + rec_offset)])[0],
        struct.unpack('B', statfile[STAT_MAP['xpa'] + base_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['xpm'] + base_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['fga'] + base_offset])[0],
        struct.unpack('B', statfile[STAT_MAP['fgm'] + base_offset])[0]
    ]
