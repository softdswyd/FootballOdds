import MyConnector
import os
from time import sleep

RESULTSAVEPATH = 'D:\\PythonProjects\\FootballOdds\\OddsBackups\\%s.txt'
FAMOUSCOMPANY = [1129, 90, 432, 81, 517, 115, 474, 499, 82, 422, 80, 450, 60, 110, 545, 177, 370, 4, 97, 104, 649,
                 158, 70, 71, 88, 9, 255, 173, 281, 18, 16]

def ParseResponseWithDetail( matchId, content ):
    oddsList = []
    indexList = {}
    rawList = content.strip().split('var ')
    for rawInfo in rawList:
        if rawInfo.strip().startswith('game=Array('):
            allDataList = rawInfo.strip()[11:-1].split('",')
            for companyOdd in allDataList:
                detailList = companyOdd[1:-1].split('|')
                if int(detailList[0]) in FAMOUSCOMPANY:
                    indexList[detailList[1]] = [detailList[0], detailList[5], detailList[16]]
    # print(indexList)
    for rawInfo in rawList:
        if rawInfo.strip().startswith('gameDetail=Array('):
            allDataList = rawInfo.strip()[17:-1].split('",')
            for companyOdd in allDataList:
                index = companyOdd[1:].split('^')[0]
                if index in indexList.keys():
                    companyOddsList = companyOdd[1:-1].split('^')[1].split(';')
                    startFlag = 1
                    for oddsDetail in companyOddsList:
                        detail = oddsDetail.split('|')
                        if 1 == startFlag:
                            # 终赔
                            sql = 'INSERT INTO MatchEuropeanOdds_%s (VictoryOdd, DrawOdd, LoseOdd, ReturnRate, ReleaseTime, ' \
                               'StartFlag, EndFlag, SecondStartFlag, MatchId) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',' \
                               '0, 1, 0, \'%s\');\n' % (indexList[index][0], detail[0], detail[1], detail[2], indexList[index][2], detail[3], matchId)
                        elif startFlag == len(companyOddsList):
                            # 初赔
                            sql = 'INSERT INTO MatchEuropeanOdds_%s (VictoryOdd, DrawOdd, LoseOdd, ReturnRate, ReleaseTime, ' \
                               'StartFlag, EndFlag, SecondStartFlag, MatchId) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',' \
                               '1, 0, 0, \'%s\');\n' % (indexList[index][0], detail[0], detail[1], detail[2], indexList[index][1], detail[3], matchId)
                        else:
                            sql = 'INSERT INTO MatchEuropeanOdds_%s (VictoryOdd, DrawOdd, LoseOdd, ReturnRate, ReleaseTime, ' \
                                  'StartFlag, EndFlag, SecondStartFlag, MatchId) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',' \
                                  '0, 0, 0, \'%s\');\n' % (indexList[index][0], detail[0], detail[1], detail[2], '', detail[3], matchId)
                        oddsList.append(sql)
                        startFlag = startFlag + 1
    #print(oddsList)
    return oddsList

def ParseResponseWithoutDetail( matchId, content ):
    # TODO:将发布时间进行格式转换
    oddsList = []
    rawList = content.strip().split(';')
    for rawInfo in rawList:
        if rawInfo.strip().startswith('game=Array('):
            allDataList = rawInfo.strip()[11:-1].split('",')
            for companyOdd in allDataList:
                detailList = companyOdd[1:-1].split('|')
                if int(detailList[0]) in FAMOUSCOMPANY:
                    sql1 = 'INSERT INTO MatchEuropeanOdds_%s (VictoryOdd, DrawOdd, LoseOdd, ReturnRate, ReleaseTime, ' \
                           'StartFlag, EndFlag, SecondStartFlag, MatchId) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',' \
                           '1, 0, 0, \'%s\');\n' % (detailList[0], detailList[3], detailList[4], detailList[5], detailList[9], detailList[20], matchId)
                    vodd = detailList[10]
                    dodd = detailList[11]
                    lodd = detailList[12]
                    if vodd == '':
                        vodd = detailList[3]
                    if dodd == '':
                        dodd = detailList[4]
                    if lodd == '':
                        lodd = detailList[5]
                    sql2 = 'INSERT INTO MatchEuropeanOdds_%s (VictoryOdd, DrawOdd, LoseOdd, ReturnRate, ReleaseTime, ' \
                           'StartFlag, EndFlag, SecondStartFlag, MatchId) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',' \
                           '0, 1, 0, \'%s\');\n' % (detailList[0], vodd, dodd, lodd, detailList[16], detailList[20], matchId)
                    oddsList.append(sql1)
                    oddsList.append(sql2)
    #print(oddsList)
    return oddsList

def ParseResponse( matchId, content):
    if content.find('var gameDetail=Array') == -1:
        # oddsList = ParseResponseWithoutDetail( matchId, content)
        return None
    else:
        oddsList = ParseResponseWithDetail( matchId, content)
    return oddsList


def GetMatchesOdds(indexPath):
    with open( indexPath, 'r', encoding='utf-8') as inf:
        line = inf.readline()
        while line:
            elementList = line.strip()[27:-2].split(',')
            matchId = elementList[0]
            matchIndex = elementList[10][2:-1]
            print('id[ %s ], index[ %s ]' % (matchId, matchIndex))
            detailUrl = 'http://1x2.nowscore.com/%s.js' % matchIndex
            content, flag = MyConnector.OpenUrlWithoutProxy(detailUrl)
            if flag:
                with open(RESULTSAVEPATH % matchIndex, 'w', encoding='utf-8') as outf:
                    outf.write(content)
                oddsList = ParseResponse( matchId, content)
                if oddsList:
                    with open('d:\\oddsData.sql', 'a', encoding='utf-8') as outf2:
                        for line in oddsList:
                            outf2.write(line)
            else:
                print('WARNING: Get Match [ %s ]\'s Odds Info Failed.' % detailUrl)
            line = inf.readline()
            sleep(1)



