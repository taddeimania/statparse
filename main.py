from positions import QuarterBack, RunningBack, WideReceiver, TightEnd

def get_home_and_away(byte):
    away = ""
    home = ""
    for x in range(3087, 3090):
        home += byte[x]

    for x in range(3119, 3122):
        away += byte[x]

    return [home, away]


def print_stats(byte):
    game = get_home_and_away(byte)

    home_side = True
    for side in game:
        for i in range(1, 3):
            qb1 = QuarterBack(byte, i, home=home_side)
            print "{},".format(side),
            qb1.print_stats()
        for i in range(1, 5):
            rb = RunningBack(byte, i, home=home_side)
            print "{},".format(side),
            rb.print_stats()
        for i in range(1, 5):
            wr = WideReceiver(byte, i, home=home_side)
            print "{},".format(side),
            wr.print_stats()
        for i in range(1, 3):
            te = TightEnd(byte, i, home=home_side)
            print "{},".format(side),
            te.print_stats()
#        for i in range(1, 3):
#            k = Kicker(byte, i, home=home_side)
#            print "{},".format(side),
#            k.print_stats()


        home_side = False

def main():
    f = open("/home/jtaddei/3.nst", "rb")
    byte = f.read()
    print_stats(byte)

if __name__ == "__main__":
    main()