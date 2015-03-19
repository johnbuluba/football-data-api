import os
import re
from datetime import datetime
import unittest

from httmock import all_requests, HTTMock, with_httmock

from football_data_api import FootballData, SoccerSeason, Team, LeagueTable, Fixture, Player



TESTDATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')


@all_requests
def mock_router(url, request):
    r = {'status_code': 200}
    if url.path == '/alpha/soccerseasons':
        r['content'] = get_test_data('soccerseasons.json')

    elif re.match("/alpha/soccerseasons/\d+$", url.path):
        r['content'] = get_test_data('soccerseasons_id.json')

    elif re.match("/alpha/soccerseasons/\d+/teams", url.path):
        r['content'] = get_test_data('soccerseasons_id_teams.json')

    elif re.match("/alpha/soccerseasons/\d+/leagueTable", url.path):
        r['content'] = get_test_data('soccerseasons_id_leagueTable.json')

    elif re.match("/alpha/soccerseasons/\d+/fixtures", url.path):
        r['content'] = get_test_data('soccerseasons_id_fixtures.json')

    elif re.match("/alpha/teams/\d+$", url.path):
        r['content'] = get_test_data('teams_id.json')

    elif re.match("/alpha/teams/\d+/fixtures$", url.path):
        r['content'] = get_test_data('teams_id_fixtures.json')

    elif re.match("/alpha/teams/\d+/players", url.path):
        r['content'] = get_test_data('teams_id_players.json')

    return r


def get_test_data(filename):

    with open(os.path.join(TESTDATA_FOLDER, filename), 'r') as content_file:
        content = content_file.read().replace('"self":', '"_self":')
    return content.encode()


class TestSoccerSeason(unittest.TestCase):

    @with_httmock(mock_router)
    def testGetById(self):
        season = FootballData().soccerseason(351)
        self.assertIsInstance(season, SoccerSeason)
        self.assertIsInstance(season.id, int)
        self.assertIsInstance(season.caption, str)
        self.assertIsInstance(season.lastUpdated, datetime)
        self.assertIsInstance(season.league, str)
        self.assertIsInstance(season.numberOfGames, int)
        self.assertIsInstance(season.numberOfTeams, int)
        self.assertIsInstance(season.year, int)

        teams = season.teams
        self.assertIsInstance(teams, list)
        for team in teams:
            self.assertIsInstance(team, Team)

        leagueTable = season.leagueTable
        self.assertIsInstance(leagueTable, list)
        for league in leagueTable:
            self.assertIsInstance(league, LeagueTable)

        fixtures = season.fixtures
        self.assertIsInstance(fixtures, list)
        for fixture in fixtures:
            self.assertIsInstance(fixture, Fixture)


    @with_httmock(mock_router)
    def testGetAllSoccerseasons(self):

        seasons = FootballData().soccerseason.all()
        self.assertIsInstance(seasons, list)
        for season in seasons:
            self.assertIsInstance(season, SoccerSeason)


class TestTeam(unittest.TestCase):

    @with_httmock(mock_router)
    def testGetById(self):
        team = FootballData().teams(50)
        self.assertIsInstance(team, Team)
        self.assertIsInstance(team.id, int)
        self.assertIsInstance(team.code, str)
        self.assertIsInstance(team.crestUrl, str)
        self.assertIsInstance(team.name, str)
        self.assertIsInstance(team.shortName, str)
        self.assertIsInstance(team.squadMarketValue, str)


        fixtures = team.fixtures
        self.assertIsInstance(fixtures, list)
        for fixture in fixtures:
            self.assertIsInstance(fixture, Fixture)

        players = team.players
        self.assertIsInstance(players, list)
        for player in players:
            self.assertIsInstance(player, Player)


