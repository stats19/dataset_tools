
def possessionInfotoMysql(dico, connmysql):
    cur_mysql1 = connmysql.cursor()
    cur_mysql2 = connmysql.cursor()
    cur_mysql3 = connmysql.cursor()
    cur_mysql4 = connmysql.cursor()

    # print("SELECT * FROM teams_matches WHERE match_id = %s" % (dico.get("match_api_id")))
    # cur_mysql1.execute("SELECT * FROM teams_matches WHERE match_id = %s" % (dico.get("match_api_id")))
    #

    if int(dico.get("elapsed")) == 90 and dico.get("awaypos") and dico.get("homepos"):
        # print("SELECT teams_match_id FROM teams_matches WHERE match_id = %s and team_id = %s;" % (dico.get("match_api_id"), dico.get("home_team_api_id")))
        cur_mysql1.execute("SELECT teams_match_id FROM teams_matches WHERE match_id = %s and team_id = %s;" % (dico.get("match_api_id"), dico.get("home_team_api_id")))
        team_match_id_home = cur_mysql1.fetchone()
        # print("team_mach_id_away = %s" % (team_match_id_home[0]))
        dico["team_match_id_home"] = team_match_id_home[0]

        # print("SELECT teams_match_id FROM teams_matches WHERE match_id = %s and team_id = %s;" % (
        # dico.get("match_api_id"), dico.get("away_team_api_id")))
        cur_mysql2.execute("SELECT teams_match_id FROM teams_matches WHERE match_id = %s and team_id = %s;" % (
            dico.get("match_api_id"), dico.get("away_team_api_id")))
        team_match_id_away = cur_mysql2.fetchone()
        # print("team_mach_id_away = %s" % (team_match_id_away[0]))
        dico["team_mach_id_away"] = team_match_id_away[0]
        # return (dico)
    else:
        if int(dico.get("elapsed")) > 80 and dico.get("awaypos") and dico.get("homepos"):
            dico["awaypos"] = (dico.get("awaypos"))
            dico["homepos"] = (dico.get("homepos"))
            # print("SELECT teams_match_id FROM teams_matches WHERE match_id = %s and team_id = %s;" % (dico.get("match_api_id"), dico.get("home_team_api_id")))
            cur_mysql3.execute("SELECT teams_match_id FROM teams_matches WHERE match_id = %s and team_id = %s;" % (
            dico.get("match_api_id"), dico.get("home_team_api_id")))
            team_match_id_home = cur_mysql3.fetchone()
            # print("team_mach_id_away = %s" % (team_match_id_home[0]))
            dico["team_match_id_home"] = team_match_id_home[0]

            # print("SELECT teams_match_id FROM teams_matches WHERE match_id = %s and team_id = %s;" % (
            # dico.get("match_api_id"), dico.get("away_team_api_id")))
            cur_mysql4.execute("SELECT teams_match_id FROM teams_matches WHERE match_id = %s and team_id = %s;" % (
                dico.get("match_api_id"), dico.get("away_team_api_id")))
            team_match_id_away = cur_mysql4.fetchone()
            # print("team_mach_id_away = %s" % (team_match_id_away[0]))
            dico["team_mach_id_away"] = team_match_id_away[0]
    return(dico)

    cur_mysql1.close
    cur_mysql2.close
    cur_mysql3.close
    cur_mysql4.close