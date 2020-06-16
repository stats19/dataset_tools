import pymysql
# import cryptography
import sqlite3
import xml.etree.ElementTree as ET

from Corner import cornerInfotoMysql
from Cross import crossInfotoMysql
from Foulcommit import foulsInfotoMysql
from Goal import goalInfotoMysql
from Possession import possessionInfotoMysql
from Shoton import shotonInfotoMysql
from Shotoff import shotoffInfotoMysql



##SQLite
connsqlite = sqlite3.connect('C:\\Users\\Pierre\\Downloads\\database.sqlite\\database.sqlite')
cur_sqlite = connsqlite.cursor()

##MySQL
connmysql = pymysql.connect(host='127.0.0.1', user='root', passwd="password", db='pa19_clean', port=3306)
cur_mysql = connmysql.cursor()

list_match_mysql = [489044]


# with open("C:/Users/Pierre/PycharmProjects/xmlscript/xml.sql", "a") as xmlsql:
for match in list_match_mysql:
    cur_sqlite = connsqlite.cursor()
    cur_sqlite.execute(
        '''SELECT home_team_api_id, away_team_api_id, match_api_id, goal, shoton, shotoff, foulcommit, card, cross, corner, possession  FROM "Match" WHERE match_api_id=%s;''' % (
            match))
    match_info = cur_sqlite.fetchall()

    for sqlitedata in match_info:
        substitute_player_list = []

        home_team_api_id = sqlitedata [0]
        away_team_api_id = sqlitedata[1]
        match_api_id = sqlitedata[2]
        goal = ("<xml>%s</xml>" % (sqlitedata[3]))
        shoton = ("<xml>%s</xml>" % (sqlitedata[4]))
        shotoff = ("<xml>%s</xml>" % (sqlitedata[5]))
        foulcommit = ("<xml>%s</xml>" % (sqlitedata[6]))
        card = ("<xml>%s</xml>" % (sqlitedata[7]))
        cross = ("<xml>%s</xml>" % (sqlitedata[8]))
        corner = ("<xml>%s</xml>" % (sqlitedata[9]))
        possession = ("<xml>%s</xml>" % (sqlitedata[10]))


        print("=============================================================================================================================")
        print("#######  GOAL  #######")
        goal_search = (ET.fromstring(goal)).findall('./goal/value')
        for attrib in goal_search:
            dico = {}
            dico["match_api_id"] = (match_api_id)
            for field in attrib:
                if field.tag != "stats":
                    dico[field.tag] = field.text

            print(dico)
            final_goal_dico = goalInfotoMysql(dico, connmysql)
            if final_goal_dico.get("scorer_id"):
                print(
                    "INSERT INTO `shots` (scorerId, assist, event_incident_typefk, elapsed, elapsed_plus, type, goalType, scored, onTarget) VALUES (%s, %s, %s, %s, %s, \"%s\", \"%s\", %s, %s);" % (
                        final_goal_dico.get("scorer_id"),
                        final_goal_dico.get("assist_id"),
                        final_goal_dico.get("event_incident_typefk"),
                        final_goal_dico.get("elapsed"),
                        final_goal_dico.get("elapsed_plus"),
                        final_goal_dico.get("type"),
                        final_goal_dico.get("goal_type"),
                        final_goal_dico.get("scored"),
                        final_goal_dico.get("onTarget")
                    ))
                sqlcmd = (
                        "INSERT INTO `shots` (scorerId, assist, event_incident_typefk, elapsed, elapsed_plus, type, goalType, scored, onTarget) VALUES (%s, %s, %s, %s, %s, \"%s\", \"%s\", %s, %s);" % (
                    final_goal_dico.get("scorer_id"),
                    final_goal_dico.get("assist_id"),
                    final_goal_dico.get("event_incident_typefk"),
                    final_goal_dico.get("elapsed"),
                    final_goal_dico.get("elapsed_plus"),
                    final_goal_dico.get("type"),
                    final_goal_dico.get("goal_type"),
                    final_goal_dico.get("scored"),
                    final_goal_dico.get("onTarget")
                ))

                # xmlsql.write("%s\n" % (sqlcmd))

            # if final_goal_dico.get("substitute"):
            #     substitutesdico = {}
            #     substitutesdico["player"] = final_goal_dico.get("substitute")
            #     substitutesdico["team"] = final_goal_dico.get("team")
            #     substitute_player_list.append(substitutesdico)
            # if final_goal_dico.get("substitute_player2"):
            #     substitutesdico = {}
            #     substitutesdico["player"] = final_goal_dico.get("substitute_player2")
            #     substitutesdico["team"] = final_goal_dico.get("substitute_team")
            #     substitute_player_list.append(substitutesdico)
            # print(final_goal_dico)



        print("=============================================================================================================================")
        print("#######  SHOTON  #######")
        shoton_search = (ET.fromstring(shoton)).findall('./shoton/value')
        for attrib in shoton_search:
            dico = {}
            dico["match_api_id"] = (match_api_id)
            for field in attrib:
                if field.tag != "stats":
                    dico[field.tag] = field.text
            print(dico)
            final_shoton_dico = shotonInfotoMysql(dico, connmysql)

            # if final_shoton_dico.get("substitute"):
            #     substitutesdico = {}
            #     substitutesdico["player"] = final_shoton_dico.get("substitute")
            #     substitutesdico["team"] = final_shoton_dico.get("team")
            #     substitute_player_list.append(substitutesdico)

            if final_shoton_dico.get("shooter_id"):
                print(
                    "INSERT INTO `shots` (scorerId, event_incident_typefk, elapsed, elapsed_plus, elapsed_plus, type, scored, onTarget) VALUES (%s, %s, %s, %s, \"%s\", %s, %s);" % (
                        final_shoton_dico.get("shooter_id"),
                        final_shoton_dico.get("event_incident_typefk"),
                        final_shoton_dico.get("elapsed"),
                        final_shoton_dico.get("elapsed_plus"),
                        final_shoton_dico.get("subtype"),
                        final_shoton_dico.get("scored"),
                        final_shoton_dico.get("onTarget")
                    ))
                sqlcmd = (
                        "INSERT INTO `shots` (scorerId, event_incident_typefk, elapsed, elapsed_plus, elapsed_plus, type, scored, onTarget) VALUES (%s, %s, %s, %s, \"%s\", %s, %s);" % (
                    final_shoton_dico.get("shooter_id"),
                    final_shoton_dico.get("event_incident_typefk"),
                    final_shoton_dico.get("elapsed"),
                    final_shoton_dico.get("elapsed_plus"),
                    final_shoton_dico.get("subtype"),
                    final_shoton_dico.get("scored"),
                    final_shoton_dico.get("onTarget")
                ))

                # xmlsql.write("%s\n" % (sqlcmd))

                # print(final_shoton_dico)



        print("=============================================================================================================================")
        print("#######  SHOTOFF  #######")
        shotoff_search = (ET.fromstring(shotoff)).findall('./shotoff/value')
        for attrib in shotoff_search:
            dico = {}
            dico["match_api_id"] = (match_api_id)
            for field in attrib:
                if field.tag != "stats":
                    dico[field.tag] = field.text
            print(dico)
            final_shotoff_dico = shotoffInfotoMysql(dico, connmysql)

            # if final_shoton_dico.get("substitute"):
            #     substitutesdico = {}
            #     substitutesdico["player"] = final_shotoff_dico.get("substitute")
            #     substitutesdico["team"] = final_shotoff_dico.get("team")
            #     substitute_player_list.append(substitutesdico)

            if final_shotoff_dico.get("shooter_id"):
                print(
                    "INSERT INTO `shots` (scorerId, event_incident_typefk, elapsed, elapsed_plus, type, scored, onTarget) VALUES (%s, %s, %s, %s, \"%s\", %s, %s);" % (
                        final_shotoff_dico.get("shooter_id"),
                        final_shotoff_dico.get("event_incident_typefk"),
                        final_shotoff_dico.get("elapsed"),
                        final_shotoff_dico.get("elapsed_plus"),
                        final_shotoff_dico.get("subtype"),
                        final_shotoff_dico.get("scored"),
                        final_shotoff_dico.get("onTarget")
                    ))
                sqlcmd = (
                        "INSERT INTO `shots` (scorerId, event_incident_typefk, elapsed, elapsed_plus, type, scored, onTarget) VALUES (%s, %s, %s, %s, \"%s\", %s, %s);" % (
                    final_shotoff_dico.get("shooter_id"),
                    final_shotoff_dico.get("event_incident_typefk"),
                    final_shotoff_dico.get("elapsed"),
                    final_shotoff_dico.get("elapsed_plus"),
                    final_shotoff_dico.get("subtype"),
                    final_shotoff_dico.get("scored"),
                    final_shotoff_dico.get("onTarget")
                ))
                # xmlsql.write("%s\n" % (sqlcmd))
                # print(final_shotoff_dico)

        print("=============================================================================================================================")
        print("#######  FOULCOMMIT  #######")
        foulcommit_search = (ET.fromstring(foulcommit)).findall('./foulcommit/value')
        for attrib in foulcommit_search:
            print("foulcommit")
            dico = {}
            dico["match_api_id"] = (match_api_id)
            dico["away_team_api_id"] = (away_team_api_id)
            dico["home_team_api_id"] = (home_team_api_id)
            for field in attrib:
                if field.tag != "stats":
                    dico[field.tag] = field.text
            listcard = []
            card_search = (ET.fromstring(card)).findall('./card/value')
            for attrib in card_search:
                carddico = {}
                carddico["match_api_id"] = (match_api_id)
                carddico["away_team_api_id"] = (away_team_api_id)
                carddico["home_team_api_id"] = (home_team_api_id)
                for field in attrib:
                    if field.tag != "stats":
                        carddico[field.tag] = field.text
                if dico.get("player1") == carddico.get("player1") and int(dico.get("elapsed"))-2 <= int(carddico.get("elapsed")) <= int(dico.get("elapsed"))+2:
                    print("============   CARD   ============")
                    dico["type"] = carddico.get("subtype")
                    if carddico.get("card_type") == "y":
                        dico["card_type"] = 1
                    if carddico.get("card_type") == "r":
                        dico["card_type"] = 2
                    if carddico.get("card_type") == "y2":
                        dico["card_type"] = 3
                    elif "card_type" not in dico:
                        dico["card_type"] = 0
                else :
                    listcard.append(carddico)
            print(dico)
            final_foulcommit_dico = foulsInfotoMysql(dico, connmysql)
            if final_foulcommit_dico.get("card_type") == None:
                dico["card_type"] = 0
            if final_foulcommit_dico.get("culprit_id"):
                print(
                    "INSERT INTO `fouls` (event_incident_typefk, elapsed, elapsed_plus, culprit_id, victim_id, type, card) VALUES (%s, %s, %s, %s, %s, \"%s\", %s);" % (
                        final_foulcommit_dico.get("event_incident_typefk"),
                        final_foulcommit_dico.get("elapsed"),
                        final_foulcommit_dico.get("elapsed_plus"),
                        final_foulcommit_dico.get("culprit_id"),
                        final_foulcommit_dico.get("victim_id"),
                        final_foulcommit_dico.get("type"),
                        final_foulcommit_dico.get("card_type")
                    ))

                sqlcmd = (
                        "INSERT INTO `fouls` (event_incident_typefk, elapsed, elapsed_plus, culprit_id, victim_id, type, card) VALUES (%s, %s, %s, %s, %s, \"%s\", %s);" % (
                    final_foulcommit_dico.get("event_incident_typefk"),
                    final_foulcommit_dico.get("elapsed"),
                    final_foulcommit_dico.get("elapsed_plus"),
                    final_foulcommit_dico.get("culprit_id"),
                    final_foulcommit_dico.get("victim_id"),
                    final_foulcommit_dico.get("type"),
                    final_foulcommit_dico.get("card_type")
                ))
                # xmlsql.write("%s\n" % (sqlcmd))

                # if final_foulcommit_dico.get("substitute"):
                #     substitutesdico = {}
                #     substitutesdico["player"] = final_foulcommit_dico.get("substitute")
                #     substitutesdico["team"] = final_foulcommit_dico.get("team")
                #     substitute_player_list.append(substitutesdico)
                # if final_foulcommit_dico.get("substitute_player2"):
                #     substitutesdico = {}
                #     substitutesdico["player"] = final_foulcommit_dico.get("substitute_player2")
                #     substitutesdico["team"] = final_foulcommit_dico.get("substitute_team2")
                #     substitute_player_list.append(substitutesdico)
                # print(final_foulcommit_dico)

        print("=======================   FOULCOMMIT NOT REFERENCED WITH CARD   =======================")
        for dico in listcard:
            print(dico)
            final_foulcommit_dico = foulsInfotoMysql(dico, connmysql)
            final_foulcommit_dico["type"] = dico.get("subtype")
            if final_foulcommit_dico.get("card_type") == "y" :
                dico["card_type"] = 1
            if final_foulcommit_dico.get("card_type") == "r" :
                dico["card_type"] = 2
            if final_foulcommit_dico.get("card_type") == "y2" :
                dico["card_type"] = 3
            if final_foulcommit_dico.get("culprit_id") and final_foulcommit_dico.get("card_type"):
                print(final_foulcommit_dico)
                print(
                    "INSERT INTO `fouls` (event_incident_typefk, elapsed, elapsed_plus, culprit_id, victim_id, type, card) VALUES (%s, %s, %s, %s, %s, \"%s\", %s);" % (
                        final_foulcommit_dico.get("event_incident_typefk"),
                        final_foulcommit_dico.get("elapsed"),
                        final_foulcommit_dico.get("elapsed_plus"),
                        final_foulcommit_dico.get("culprit_id"),
                        final_foulcommit_dico.get("victim_id"),
                        final_foulcommit_dico.get("type"),
                        final_foulcommit_dico.get("card_type")
                    ))
                sqlcmd = (
                        "INSERT INTO `fouls` (event_incident_typefk, elapsed, elapsed_plus, culprit_id, victim_id, type, card) VALUES (%s, %s, %s, %s, %s, \"%s\", %s);" % (
                    final_foulcommit_dico.get("event_incident_typefk"),
                    final_foulcommit_dico.get("elapsed"),
                    final_foulcommit_dico.get("elapsed_plus"),
                    final_foulcommit_dico.get("culprit_id"),
                    final_foulcommit_dico.get("victim_id"),
                    final_foulcommit_dico.get("type"),
                    final_foulcommit_dico.get("card_type")
                ))
                # xmlsql.write("%s\n" % (sqlcmd))

                # if final_foulcommit_dico.get("substitute"):
                #     substitutesdico = {}
                #     substitutesdico["player"] = final_foulcommit_dico.get("substitute")
                #     substitutesdico["team"] = final_foulcommit_dico.get("team")
                #     substitute_player_list.append(substitutesdico)
                # if final_foulcommit_dico.get("substitute_player2"):
                #     substitutesdico = {}
                #     substitutesdico["player"] = final_foulcommit_dico.get("substitute_player2")
                #     substitutesdico["team"] = final_foulcommit_dico.get("substitute_team2")
                #     substitute_player_list.append(substitutesdico)
                # print(final_foulcommit_dico)

        ######### END OF FOULCOMMIT #########


        print("=============================================================================================================================")
        print("#######  CROSS  #######")
        shoton_search = (ET.fromstring(cross)).findall('./cross/value')
        for attrib in shoton_search:
            dico = {}
            dico["match_api_id"] = (match_api_id)
            for field in attrib:
                if field.tag != "stats":
                    dico[field.tag] = field.text
            print(dico)
            final_cross_dico = crossInfotoMysql(dico, connmysql)

            if final_cross_dico.get("team_matches_player_id"):
                print(
                    "INSERT INTO `crosses` (teams_matches_players_id, elapsed, elapsed_plus, type, event_incident_typefk) VALUES (%s, %s, %s, \"%s\", %s);" % (
                        final_cross_dico.get("team_matches_player_id"),
                        final_cross_dico.get("elapsed"),
                        final_cross_dico.get("elapsed_plus"),
                        final_cross_dico.get("type"),
                        final_cross_dico.get("event_incident_typefk")
                    ))

                sqlcmd =(
                        "INSERT INTO `crosses` (teams_matches_players_id, elapsed, elapsed_plus, type, event_incident_typefk) VALUES (%s, %s, %s, \"%s\", %s);" % (
                    final_cross_dico.get("team_matches_player_id"),
                    final_cross_dico.get("elapsed"),
                    final_cross_dico.get("elapsed_plus"),
                    final_cross_dico.get("type"),
                    final_cross_dico.get("event_incident_typefk")
                ))
                # xmlsql.write("%s\n" % (sqlcmd))

                # if final_cross_dico.get("substitute"):
                #     substitutesdico = {}
                #     substitutesdico["player"] = final_cross_dico.get("substitute")
                #     substitutesdico["team"] = final_cross_dico.get("substitute_team")
                #     substitute_player_list.append(substitutesdico)
                # print(final_cross_dico)

        print("=============================================================================================================================")
        print("#######  CORNER  #######")
        shoton_search = (ET.fromstring(corner)).findall('./corner/value')
        for attrib in shoton_search:
            dico = {}
            dico["match_api_id"] = (match_api_id)
            for field in attrib:
                if field.tag != "stats":
                    dico[field.tag] = field.text

            print(dico)
            final_corner_dico = cornerInfotoMysql(dico, connmysql)

            if final_corner_dico.get("team_matches_player_id"):
                print(final_corner_dico)
                print(
                    "INSERT INTO `corners` (teams_matches_players_id, elapsed, elapsed_plus, type) VALUES (%s, %s, %s, \"%s\") WHERE teams_match_id = %s" % (
                        final_corner_dico.get("team_matches_player_id"),
                        final_corner_dico.get("elapsed"),
                        final_corner_dico.get("elapsed_plus"),
                        final_corner_dico.get("type"),
                        final_corner_dico.get("match_api_id")
                    ))
                sqlcmd = (
                        "INSERT INTO `corners` (teams_matches_players_id, elapsed, elapsed_plus, type) VALUES (%s, %s, %s, \"%s\") WHERE teams_match_id = %s" % (
                    final_corner_dico.get("team_matches_player_id"),
                    final_corner_dico.get("elapsed"),
                    final_corner_dico.get("elapsed_plus"),
                    final_corner_dico.get("type"),
                    final_corner_dico.get("match_api_id")
                ))
                # xmlsql.write("%s\n" % (sqlcmd))

                # if final_corner_dico.get("substitute"):
                #     substitutesdico = {}
                #     substitutesdico["player"] = final_corner_dico.get("substitute")
                #     substitutesdico["team"] = final_corner_dico.get("substitute_team")
                #     substitute_player_list.append(substitutesdico)
                # print(final_corner_dico)

        print("=============================================================================================================================")
        print("#######  POSSESSION  #######")
        possession_search = (ET.fromstring(possession)).findall('./possession/value')
        for attrib in possession_search:
            dico = {}
            dico["match_api_id"] = (match_api_id)
            dico["away_team_api_id"] = (away_team_api_id)
            dico["home_team_api_id"] = (home_team_api_id)
            for field in attrib:
                if field.tag != "stats":
                    dico[field.tag] = field.text
            print(dico)
            final_possession_dico = possessionInfotoMysql(dico, connmysql)

            if final_possession_dico:
                print(final_possession_dico)
                if final_possession_dico.get("team_match_id_home") and final_possession_dico.get("team_mach_id_away"):
                    print("UPDATE teams_matches SET possession = %s WHERE teams_match_id = %s;\n"
                              "UPDATE teams_matches SET possession = %s WHERE teams_match_id = %s;" % (final_possession_dico.get("awaypos"), final_possession_dico.get("team_mach_id_away"), final_possession_dico.get("homepos"), final_possession_dico.get("team_match_id_home")))

                    sqlcmd = ("UPDATE teams_matches SET possession = %s WHERE teams_match_id = %s;\n"
                              "UPDATE teams_matches SET possession = %s WHERE teams_match_id = %s;" % (final_possession_dico.get("awaypos"), final_possession_dico.get("team_mach_id_away"), final_possession_dico.get("homepos"), final_possession_dico.get("team_match_id_home")))

                    # xmlsql.write("%s\n" % (sqlcmd))
                # print("UPDATE teams_matches SET possession = %s WHERE teams_match_id_home = %s;" % (final_foulcommit_dico.get("homepos"),
                #                                                                                     final_foulcommit_dico.get(
                #                                                                                         "team_mach_id_away")))

    cur_sqlite.close()
# substitute_player = {}
# print("list of substitutes players")
# substitute_player[str(match_api_id)] = substitute_player_list
#
# with open("C:/Users/Pierre/PycharmProjects/xmlscript/test.txt", "a") as substitutesplayers:
#     substitutesplayers.write("%s\n" %(str(substitute_player)))
# print(substitute_player)


cur_mysql.close()

