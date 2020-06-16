import re


def shotoffInfotoMysql(dico, connmysql):
    cur_mysql1 = connmysql.cursor()
    cur_mysql2 = connmysql.cursor()

    dico["scored"] = 0
    dico["onTarget"] = 0

    if not dico.get("elapsed_plus"):
        dico["elapsed_plus"] = "NULL"
    if dico.get("player1") and dico.get("team") and re.match("^\d+$", dico.get("player1")):

        # print("SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (dico.get("match_api_id"), dico.get("team")))
        cur_mysql1.execute(
            "SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (
                dico.get("match_api_id"), dico.get("team")
            )
        )
        team_match_id = cur_mysql1.fetchone()

        # print(
        #     "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
        #         team_match_id[0], dico.get("player1"))
        # )
        cur_mysql2.execute(
            "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
                team_match_id[0], dico.get("player1"))
        )
        team_matches_player_id = cur_mysql2.fetchone()
        shooter_id = ""
        if team_matches_player_id:
            shooter_id = (team_matches_player_id[0])
            dico["shooter_id"] = shooter_id
            # print("team_match_id  : %s\nscorer player : %s" % (team_match_id[0], shooter_id))
        else:
            print("========\nplayer1 not found : %s\n=======" % (dico.get("player1")))
            dico["substitute"] = dico.get("player1")
            dico["substitute_team"] = dico.get("team")

    return dico
    cur_mysql1.close
    cur_mysql2.close
