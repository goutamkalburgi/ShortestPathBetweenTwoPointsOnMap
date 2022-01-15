# This code is written by Goutamkumar Tulajappa Kalburgi. NAU Email ID: gk325@nau.edu
__author__ = "Goutamkumar Tulajappa Kalburgi (gk325@nau.edu)"

import searcher

if __name__ == '__main__':
    s1 = searcher.Searcher('best', '40test1.txt', False)
    # s2.plotGraph()
    s1.setStartGoal('AC', ['M'])
    s1.go()
    s2 = searcher.Searcher('best', '40test1.txt', False)
    # s2.plotGraph()
    s2.setStartGoal('T', ['AL'])
    s2.go()
    s3 = searcher.Searcher('best', '40test1.txt', False)
    # s2.plotGraph()
    s3.setStartGoal('J', ['K'])
    s3.go()
    s4 = searcher.Searcher('best', '40test1.txt', False)
    # s2.plotGraph()
    s4.setStartGoal('R', ['S'])
    s4.go()
    s5 = searcher.Searcher('best', '40test1.txt', False)
    # s2.plotGraph()
    s5.setStartGoal('K', ['U'])
    s5.go()



