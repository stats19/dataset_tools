import re


def crossInfotoMysql(dico, connmysql):
    cur_mysql1 = connmysql.cursor()
    cur_mysql2 = connmysql.cursor()

    if not dico.get("elapsed_plus"):
        dico["elapsed_plus"] = "NULL"

    if dico.get("player1") and dico.get("team")  and re.match("^\d+$", dico.get("player1")):



        # print("SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (dico.get("match_api_id"), dico.get("team")))
        cur_mysql1.execute(
            "SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (
                dico.get("match_api_id"), dico.get("team")
            )
        )


        team_match_id = cur_mysql1.fetchone()

        if team_match_id:
            # print(
            #     "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
            #         team_match_id[0], dico.get("player1"))
            # )
            cur_mysql2.execute(
                "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
                    team_match_id[0], dico.get("player1"))
            )
            t_matches_player_id = cur_mysql2.fetchone()
            team_matches_player_id = ""
            if t_matches_player_id:
                dico["team_matches_player_id"] = t_matches_player_id[0]
                # print("team_match_id  : %s\nteam_matches_player_id : %s" % (team_match_id[0], team_matches_player_id))
            else:
                print("========\nplayer1 not found : %s\n=======" % (dico.get("player1")))
                dico["substitute"] = dico.get("player1")
                dico["substitute_team"] = dico.get("team")

    cur_mysql1.close
    cur_mysql2.close
    return dico


