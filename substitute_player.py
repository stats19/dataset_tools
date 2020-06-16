import json
import sqlite3

import pymysql

connsqlite = sqlite3.connect('C:\\Users\\Pierre\\Downloads\\database.sqlite\\database.sqlite')


##MySQL
connmysql = pymysql.connect(host='127.0.0.1', user='root', passwd="password", db='pa19', port=3306)

with open("C:/Users/Pierre/PycharmProjects/xmlscript/substitute.sql", "a") as substitutesql:
    with open("C:/Users/Pierre/PycharmProjects/xmlscript/test3.txt", "r") as substitutesplayers:
        for line in substitutesplayers:
            ds = json.loads(line) #this contains the json
            substitutesdico = {}
            for match_id, players_infos in ds.items():
                print(match_id)
                # print(players_infos)
                for player_info in players_infos:
                    print(player_info)
                    player = player_info.get("player")
                    if player != "None":
                        cur_mysql1 = connmysql.cursor()
                        cur_mysql2 = connmysql.cursor()
                        cur_mysql1.execute("SELECT * FROM pa19.player where player_api_id = %s;" %(player))
                        mysql_player_info = cur_mysql1.fetchall()
                        if mysql_player_info:
                            cur_mysql2.execute("SELECT teams_match_id FROM teams_matches WHERE team_id=%s and match_id=%s;" %(player_info.get("team"), match_id))
                            teams_match_id  = cur_mysql2.fetchone()
                            print(
                                "INSERT INTO teams_matches_players (player_id, teams_match_id, first_team) VALUES (%s, %s, 0)" % (
                                player_info.get("player"), teams_match_id[0]))
                            substitutesql.write("%s\n" % ("INSERT INTO teams_matches_players (player_id, teams_match_id, first_team) VALUES (%s, %s, 0);" % (
                                player_info.get("player"), teams_match_id[0])))
                            cur_mysql2.close()
                            continue
                        else :
                            cur_sqlite1 = connsqlite.cursor()
                            cur_mysql3 = connmysql.cursor()
                            cur_sqlite1.execute("SELECT * FROM Player p where player_api_id = %s;" %(player))
                            player_carac = cur_sqlite1.fetchone()
                            if player_carac:
                                player_api_id = player_carac[1]
                                player_name = player_carac[2]
                                player_fifa_api_id = player_carac[3]
                                birthday = player_carac[4]
                                height = player_carac[5]
                                weight = player_carac[6]
                                print("INSERT INTO player (player_api_id, player_name, player_fifa_api_id, birthday, height, weight) VALUES (%s, \"%s\", %s, \"%s\", %s, %s)" %(player_api_id, player_name, player_fifa_api_id, birthday, height, weight))
                                substitutesql.write("%s\n" % ("INSERT INTO player (player_api_id, player_name, player_fifa_api_id, birthday, height, weight) VALUES (%s, \"%s\", %s, \"%s\", %s, %s);" %(player_api_id, player_name, player_fifa_api_id, birthday, height, weight)))
                                cur_mysql3.execute(
                                    "SELECT teams_match_id FROM teams_matches WHERE team_id=%s and match_id=%s;" % (
                                    player_info.get("team"), match_id))
                                teams_match_id = cur_mysql3.fetchone()
                                print(
                                    "INSERT INTO teams_matches_players (player_id, teams_match_id, first_team) VALUES (%s, %s, 0);" % (
                                        player_info.get("player"), teams_match_id[0]))
                                substitutesql.write("%s\n" %(
                                    "INSERT INTO teams_matches_players (player_id, teams_match_id, first_team) VALUES (%s, %s, 0);" % (
                                        player_info.get("player"), teams_match_id[0])) )

                                cur_mysql3.close()
                            else :
                                print("player not found in two BDD")
                                continue
                            cur_sqlite1.close()
                        cur_mysql1.close()


