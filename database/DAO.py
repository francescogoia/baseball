from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct t.`year` 
            from teams t 
            where t.`year` >= 1980
            order by t.`year` desc 
            """
        cursor.execute(query)
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                    select *
                    from teams t 
                    where t.`year` = %s
                    """
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(Team(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryOfTeams(anno, idMap):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """
                select t.teamCode, t.ID,sum(s.salary) as tot_salary
                from salaries s, teams t , appearances a 
                where s.`year` = t.`year` and t.`year` = a.`year` 
                    and a.`year` = %s
                    and t.ID = a.teamID 
                    and a.playerID = s.playerID 
                group by t.teamCode 
                       """
        cursor.execute(query, (anno,))
        result = {}
        for row in cursor:
            result[idMap[row["ID"]]] = row["tot_salary"]  # dizionario Team: salary

        cursor.close()
        conn.close()
        return result
