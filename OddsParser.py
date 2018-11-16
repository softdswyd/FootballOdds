import TeamDealer
import MatchDealer
import OddsDealer

if __name__ == '__main__':
    # TeamDealer.GetFootballTeams()
    # MatchDealer.GetMatchesInfo()
    indexPath = 'd:\\50001-700001.sql'
    OddsDealer.GetMatchesOdds(indexPath)