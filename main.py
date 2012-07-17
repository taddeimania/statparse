from positions import QuarterBack, RunningBack

def get_home_and_away(byte):
    away = ""
    home = ""
    for x in range(3087, 3090):
        home += byte[x]

    for x in range(3119, 3122):
        away += byte[x]

    return home, away

def main():
    f = open("/home/jtaddei/3.nst", "rb")
    byte = f.read()
    home, away = get_home_and_away(byte)
    print "\t\tPASSAT\tCOMP\tPASSTD\tPASSINT\tPASSYDS\t\tRUSAT\tRUSYDS\tRUSTD"
    qb1 = QuarterBack(byte, 1, home=False)
    qb1.print_stats()
    for i in range(1, 5):
        rb = RunningBack(byte, i, home=False)
        rb.print_stats()

#    rb1 = RunningBack(byte, 1)
#    rb1.print_stats()

if __name__ == "__main__":
    main()