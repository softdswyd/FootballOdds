import MyConnector

FootballLeagueList = [21, 284, 17, 9, 12, 37, 36, 39, 35, 31, 34, 8, 11, 40, 33, 23, 157, 29, 150, 16, 25, 60, 61, 4, 358]

def GetFootballTeams():
    AllTeamList = []
    for leagueCode in FootballLeagueList:
        url = 'http://info.nowscore.com/jsData/teamInfo/team%d.js?version=20181111141201' % leagueCode
        content, flag = MyConnector.OpenUrlWithoutProxy(url)
        if flag:
            arrTeam = content.split('var')
            teamList = (','+arrTeam[2][12:-3]).split(',[')
            leagueTealList = []
            for team in teamList:
                if len(team) == 0:
                    continue
                teamDetail = []
                detailList = team.split(',')
                teamDetail.append(detailList[0])
                teamDetail.append(detailList[3][1:-1])
                teamDetail.append(detailList[1][1:-1])
                teamDetail.append(detailList[2][1:-1])
                leagueTealList.append(teamDetail)
            AllTeamList.append(leagueTealList)
        else:
            print('WARNING: Cannot Get League [ %d ] .')
    index = 1
    for key1 in AllTeamList:
        for key2 in key1:
            insertSql = 'INSERT INTO Teams VALUES( %d, \'%s\', \'%s\', \'%s\', \'%s\');' % \
                        (index, str(key2[0]), key2[1], key2[2], key2[3])
            print(insertSql)
            index = index + 1
    return AllTeamList