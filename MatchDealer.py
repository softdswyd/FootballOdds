import MyConnector
import TeamDealer
import re
from time import sleep

TopFootballLeague = [36, 31, 34, 8, 11, 29, 4, 358, 60, 61]
HOMEPAGE = 'http://info.nowscore.com'
MATCHYEARPATTERN = r'<script type="text/javascript"  src="/jsData/LeagueSeason/.*?\.js"></script>'
MATCHYEARPATTERN1 = r'\d{4}-\d{4}'
MATCHYEARPATTERN2 = r'\d{4}'
MATCHINFOPATTERN1 = r'<script type="text/javascript"  src="/jsData/matchResult/.*?"></script>'
MATCHINFOPATTERN2 = r'\[\d{1,7}.*?\'\d{4}-\d{2}-\d{2}.*?\]'
MATCHROUNDPATTERN = r'jh\["R_\d{1,2}"\]'

def UrlTranform( oldUrl ):
    newUrl = oldUrl
    if oldUrl.find('284_809') != -1:
        newUrl = oldUrl.replace('284_809', '284_808')
    elif oldUrl.find('284_1085') != -1:
        newUrl = oldUrl.replace('284_1085', '284_808')
    elif oldUrl.find('17_1274') != -1:
        newUrl = oldUrl.replace('17_1274', '17_94')
    elif oldUrl.find('17_97') != -1:
        newUrl = oldUrl.replace('17_97', '17_94')
    elif oldUrl.find('9_131') != -1:
        newUrl = oldUrl.replace('9_131', '9_132')
    elif oldUrl.find('9_130') != -1:
        newUrl = oldUrl.replace('9_130', '9_132')
    elif oldUrl.find('12_1779') != -1:
        newUrl = oldUrl.replace('12_1779', '12_1778')
    elif oldUrl.find('37_90') != -1:
        newUrl = oldUrl.replace('37_90', '37_87')
    elif oldUrl.find('39_138') != -1:
        newUrl = oldUrl.replace('39_138', '39_135')
    elif oldUrl.find('35_148') != -1:
        newUrl = oldUrl.replace('35_148', '35_139')
    elif oldUrl.find('40_343') != -1:
        newUrl = oldUrl.replace('40_343', '40_261')
    elif oldUrl.find('40_262') != -1:
        newUrl = oldUrl.replace('40_262', '40_261')
    elif oldUrl.find('40_263') != -1:
        newUrl = oldUrl.replace('40_263', '40_261')
    elif oldUrl.find('33_1301') != -1:
        newUrl = oldUrl.replace('33_1301', '33_546')
    elif oldUrl.find('33_547') != -1:
        newUrl = oldUrl.replace('33_547', '33_546')
    elif oldUrl.find('23_1124') != -1:
        newUrl = oldUrl.replace('23_1124', '23_1123')
    elif oldUrl.find('157_1786') != -1:
        newUrl = oldUrl.replace('157_1786', '157_1787')
    elif oldUrl.find('150_1128') != -1:
        newUrl = oldUrl.replace('150_1128', '150_1115')
    elif oldUrl.find('150_1122') != -1:
        newUrl = oldUrl.replace('150_1122', '150_1115')
    elif oldUrl.find('16_1288') != -1:
        newUrl = oldUrl.replace('16_1288', '16_98')
    elif oldUrl.find('16_703') != -1:
        newUrl = oldUrl.replace('16_703', '16_98')
    elif oldUrl.find('16_99') != -1:
        newUrl = oldUrl.replace('16_99', '16_98')
    elif oldUrl.find('16_100') != -1:
        newUrl = oldUrl.replace('16_100', '16_98')
    elif oldUrl.find('16_101') != -1:
        newUrl = oldUrl.replace('16_101', '16_98')
    elif oldUrl.find('25_1412') != -1:
        newUrl = oldUrl.replace('25_1412', '25_943')
    elif oldUrl.find('25_944') != -1:
        newUrl = oldUrl.replace('25_944', '25_943')
    elif oldUrl.find('21_1968') != -1:
        newUrl = oldUrl.replace('21_1968', '21_165')
    elif oldUrl.find('21_168') != -1:
        newUrl = oldUrl.replace('21_168', '21_165')

    return newUrl

def GetMatchesInfo():
    index = 1
    for leagueId in TeamDealer.FootballLeagueList:
        if leagueId in TopFootballLeague:
            leagueUrl = 'http://info.nowscore.com/cn/League/%d.html' % leagueId
        else:
            leagueUrl = 'http://info.nowscore.com/cn/SubLeague/%d.html' % leagueId
        content, flag = MyConnector.OpenUrlWithoutProxy(leagueUrl)
        if flag:
            matchYearUrlList = re.findall( MATCHYEARPATTERN, content)
            matchYearUrl = HOMEPAGE + matchYearUrlList[0][37:-11]
            matchYearList = []
            matchYearContent, myFlag = MyConnector.OpenUrlWithoutProxy(matchYearUrl)
            if myFlag:
                matchYearList = re.findall( MATCHYEARPATTERN1, matchYearContent )
                if len(matchYearList) == 0:
                    matchYearList = re.findall( MATCHYEARPATTERN2, matchYearContent )
                if len(matchYearList) == 0:
                    print('WARNING: Get League [ %d ] Year List Failed.' % leagueId)
                    continue
            else:
                print('WARNING: Open League [ %d ] Year List Page Failed.' % leagueId)
                continue
            for year in matchYearList:
                matchRawUrl = 'http://info.nowscore.com/cn/SubLeague/%s/%d.html' % (year, leagueId)
                # print(matchRawUrl)
                print('Now Getting League [ %d ] in Year [ %s ] Matches Data.' % (leagueId, year))
                matchContent, matchRawFlag = MyConnector.OpenUrlWithoutProxy(matchRawUrl)
                if matchRawFlag:
                    matchRawList = re.findall(MATCHINFOPATTERN1, matchContent)
                    matchInfoUrl = HOMEPAGE + matchRawList[0][37:-11]
                    matchInfoUrl = UrlTranform(matchInfoUrl)
                    print('MatchInfo Url:%s' %matchInfoUrl)
                    matchInfoContent, matchFlag = MyConnector.OpenUrlWithoutProxy(matchInfoUrl)
                    if matchFlag:
                        matchInfosList = []
                        matchList = matchInfoContent.split(';')
                        # print(matchList)
                        for match in matchList:
                            if match.strip().startswith('jh'):
                                pos = match.find('=')
                                matchRound = match[:pos][7:-3]
                                #print(matchRound)
                                matchInfoList = re.findall(MATCHINFOPATTERN2, match)
                                for matchRawDetail in matchInfoList:
                                    matchDetailList = matchRawDetail[1:-2].split(',')
                                    matchInfos = []
                                    matchInfos.append(matchDetailList[0])
                                    matchInfos.append(matchDetailList[1])
                                    matchInfos.append(matchDetailList[3][1:-1])
                                    matchInfos.append(matchDetailList[4])
                                    matchInfos.append(matchDetailList[5])
                                    matchInfos.append(matchDetailList[6][1:-1])
                                    matchInfos.append(matchDetailList[7][1:-1])
                                    matchInfos.append(matchDetailList[8][1:-1])
                                    matchInfos.append(matchDetailList[9][1:-1])
                                    matchInfos.append(matchRound)
                                    matchInfosList.append(matchInfos)
                        # print(matchInfosList)
                        with open('d:\\data.sql', 'a', encoding='utf-8') as outf:
                            print('League [ %d ] in Year [ %s ] has [ %f ] matches. ' % ( leagueId, year, len(matchInfosList)))
                            for data in matchInfosList:
                                if data[5] == '':
                                    continue
                                insertSql = 'INSERT INTO Matches VALUES' \
                                            '(%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', ' \
                                            '\'%s\', \'%s\', \'%s\', \'%s\');\n' % \
                                            (index, data[3], data[4], data[5], data[1], data[2], data[9],
                                             data[6], data[7], data[8], data[0])
                                outf.write(insertSql)
                                index = index + 1
                else:
                    print('WARNING: Open MatchInfo [ %d, %s ] List Page Failed.' % (leagueId, year))
                sleep(5)
        else:
            print('Get League [ %d ] Year Failed.' % leagueId)
        #break