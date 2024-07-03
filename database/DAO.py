from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():
    @staticmethod
    def getYear():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(datetime) as year
                    from sighting s """
        cursor.execute(query, )
        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getShape(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct shape 
                    from sighting s 
                    where year(s.`datetime`) = %s"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from state s """
        cursor.execute(query, )
        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select n.state1 as s1, n.state2  as s2
                    from neighbor n 
                    where n.state1 < n.state2"""
        cursor.execute(query, )
        for row in cursor:
            result.append((row["s1"], row["s2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(anno, forma):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1 as st1, n.state2 as st2 , count(*) as N
                    FROM sighting s , neighbor n 
                    where year(s.`datetime`) = %s
                    and s.shape = %s
                    and (s.state = n.state1 or s.state = n.state2 )
                    and n.state1 < n.state2
                    group by n.state1 , n.state2"""
        cursor.execute(query, (anno, forma,) )
        for row in cursor:
            result.append((row["st1"], row["st2"], row["N"]))

        cursor.close()
        conn.close()
        return result


