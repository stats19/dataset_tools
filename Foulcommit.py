import re


def foulsInfotoMysql(dico, connmysql):

    cur_mysql1 = connmysql.cursor()
    cur_mysql2 = connmysql.cursor()
    cur_mysql3 = connmysql.cursor()
    cur_mysql4 = connmysql.cursor()
    cur_mysql5 = connmysql.cursor()

    if not dico.get("elapsed_plus"):
        dico["elapsed_plus"] = "NULL"

    if dico.get("player1") and dico.get("team") and re.match("^\d+$", dico.get("player1")):

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
        culprit_id = ""
        if team_matches_player_id:
            culprit_id = (team_matches_player_id[0])
            dico["culprit_id"] = culprit_id
        else:
            print("========\nplayer1 not found : %s\n=======" %(dico.get("player1")))
            dico["substitute"] = dico.get("player1")
            dico["substitute_team"] = dico.get("team")
            # culprit_id == "NULL";
            dico["culprit_id"] = culprit_id
        team_coupable = int(dico.get("team"))
        cur_mysql3.execute(
            "SELECT team_id FROM teams_matches WHERE match_id = %s;" % (
                dico.get("match_api_id")))
        teams = cur_mysql3.fetchall()

        teamvictime = ''
        for value in teams:
            team = (value[0])
            if team_coupable != team:
                teamvictime = team
                dico["team_victim"] = str(teamvictime)
        # print(("SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (match_api_id, teamvictime)))
        cur_mysql4.execute("SELECT teams_match_id FROM teams_matches WHERE match_id = %s AND team_id = %s;" % (
            dico.get("match_api_id"), teamvictime))

        victim_team_match_id = cur_mysql4.fetchone()
        victim_id = ""
        if dico.get("player2"):
            # print(
            #     "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
            #         victim_team_match_id[0], dico.get("player2"))
            # )

            cur_mysql5.execute(
                "SELECT team_matches_player_id FROM teams_matches_players where teams_match_id = %s and player_id = %s;" % (
                    victim_team_match_id[0], dico.get("player2"))
            )
            team_matches_player_victim_id = cur_mysql5.fetchone()
            if team_matches_player_victim_id:
                victim_id = (team_matches_player_victim_id[0])
                dico["victim_id"] = victim_id
            else:
                print("========\nplayer2 not found : %s\n=======" %(dico.get("player2")))
                dico["substitute_player2"] = dico.get("player2")
                dico["substitute_team2"] = dico.get("team_victim")
                dico["victim_id"] = "NULL"
        else :
            victim_id = "NULL"
            dico["victim_id"] = victim_id


    cur_mysql5.close()
    cur_mysql4.close()
    cur_mysql3.close()
    cur_mysql2.close()
    cur_mysql1.close()
    return dico