import re


def goalInfotoMysql(dico, connmysql):
    cur_mysql1 = connmysql.cursor()
    cur_mysql2 = connmysql.cursor()
    cur_mysql3 = connmysql.cursor()
    cur_mysql4 = connmysql.cursor()

    dico["scored"] = 1
    dico["onTarget"] = 1

    if not dico.get("elapsed_plus"):
        dico["elapsed_plus"] = "NULL"

    if dico.get("player1") and dico.get("team")  and re.match("^\d+$", dico.get("player1")):

        # print("SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (
        # dico.get("match_api_id"), dico.get("team")))
        cur_mysql1.execute(
            "SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (
                dico.get("match_api_id"), dico.get("team")
            )
        )
        team_match_id = cur_mysql1.fetchone()
        print(team_match_id)
        # print(
        #     "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
        #         team_match_id[0], dico.get("player1"))
        # )
        cur_mysql2.execute(
            "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
                team_match_id[0], dico.get("player1"))
        )
        team_matches_player_id = cur_mysql2.fetchone()
        scorer_id = ""
        if team_matches_player_id:
            scorer_id = (team_matches_player_id[0])
            dico["scorer_id"] = scorer_id
            # print("team_match_id  : %s\nscorer player : %s" % (team_match_id[0], scorer_id))
        else:
            print("========\nplayer1 not found : %s\n=======" % (dico.get("player1")))
            dico["substitute"] = dico.get("player1")
            dico["substitute_team"] = dico.get("team")
            # scorer_id == "NULL";
            dico["scorer_id"] = scorer_id

    assist_id = ""
    if dico.get("player2"):
        cur_mysql3.execute("SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (
            dico.get("match_api_id"), dico.get("team")))

        assist_team_match_id = cur_mysql3.fetchone()
        # print(
        #     "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
        #         assist_team_match_id[0], dico.get("player2"))
        # )

        cur_mysql4.execute(
            "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
                assist_team_match_id[0], dico.get("player2"))
        )
        team_matches_player_assist_id = cur_mysql4.fetchone()
        if team_matches_player_assist_id:
            assist_id = (team_matches_player_assist_id[0])
            # print(victim_id)
            dico["assist_id"] = assist_id
            # print("assist_team_match_id  : %s\nassist player : %s" % (assist_team_match_id[0], assist_id))
        else:
            print("========\nplayer2 not found : %s\n=======" % (dico.get("player2")))
            dico["substitute_player2"] = dico.get("player2")
            dico["substitute_team"] = dico.get("team")
            dico["assist_id"] = "NULL"
    else:
        dico["assist_id"] = "NULL"


    cur_mysql1.close
    cur_mysql2.close
    cur_mysql3.close
    cur_mysql4.close
    print(dico)

    return dico
