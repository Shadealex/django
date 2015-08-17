import psycopg2
from ipwhois import IPWhois



# conn = psycopg2.connect("dbname='ipjet' user='ipjet' host='localhost'")
conn = psycopg2.connect("dbname='ipjet' user='ipjet' host='ipjet.nest.ipnet' password='ipjet123'")
cur = conn.cursor()
sql = """ SELECT id FROM report_ip WHERE country='NULL' OR description='NULL' OR address='NULL' OR name='NULL';"""
cur.execute(sql)
users = cur.fetchall()
count = 1
for x in users:
        sql = """SELECT ip FROM report_ip WHERE id=%s"""
        cur.execute(sql % (x[0]))
        ip = cur.fetchall()
        try:
                obj = IPWhois(ip[0][0])
                result = obj.lookup()
                print result
                address = str("'"+result['nets'][0]['address']+"'")
                country = str("'"+result['nets'][0]['country']+"'")
                description = str("'"+result['nets'][0]['description']+"'")
                name = str("'"+result['nets'][0]['name']+"'")
        except:
                address = str("'IPNET'")
                country = str("'IPNET'")
                description = str("'IPNET'")
                name = str("'IPNET'")

        try:
                sql_update = """UPDATE report_ip SET country=%s, description=%s, address=%s, name=%s WHERE id=%s;"""
                cur.execute(sql_update % (country, description, address, name, x[0]))
                conn.commit()
        except:
                conn.rollback()
                sql_update = """UPDATE report_ip SET country='NONAME', description='NONAME', address='NONAME', name='NONAME' WHERE id=%s;"""
                cur.execute(sql_update % (x[0]))
                conn.commit()
        print count
        count += 1
        print cur.query
        print cur.statusmessage
cur.close()
conn.close()