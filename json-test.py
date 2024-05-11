import json
import os
import pymysql


def get_plat_conn():
    conn = pymysql.connect(
            host= 'coolcollege.mysql.rds.aliyuncs.com',  # mysql的主机ip
            port=3306,  # 端口
            user='cool',  # 用户名
            passwd='Cx111111@',  # 数据库密码
            charset='utf8',  # 使用字符集
)
    return conn
    
def get_e_conn(host):
    conn = pymysql.connect(
            host= str(host),  # mysql的主机ip
            port=3306,  # 端口
            user='cool',  # 用户名
            passwd='Cx111111@',  # 数据库密码
           charset='utf8',  # 使用字符集
)
    return conn
    
    
def get_enterprise_db_config(ding_corp_id):
    plat_conn = get_plat_conn()
    cur=plat_conn.cursor()
    sql="select id, db_server, db_source_name from enterprise_config where ding_corp_id =" + ding_corp_id
    conn_info = query_one(cur, sql, args).[0]
    print(conn_info);
    return get_e_conn(conn_info[1])
    
    
def query_one(cur, sql, args):
    cur.execute(sql, args)
    return cur.fetchone()    

def update_user(ding_corp_id, active, user_id, now_active):
    plat_conn = get_plat_conn()
    cur=plat_conn.cursor()
    sql="select id, db_server, db_source_name from enterprise_config where ding_corp_id =" + ding_corp_id
    conn_info = query_one(cur, sql, args).[0]
    print(conn_info);
    conn = get_e_conn(conn_info[1])
    cur=conn.cursor()
    update_sql="update coolcollege_enterprise_" + str(conn_info[0]) +".enterprise_user set active=" + str(active) + " where id = " + str(user_id) + " and active =" + str(now_active)
    print(update_sql)
    update_data(cur, conn,sql=update_sql,args=None)
    
def update_data(cur, db,sql, args):
  try:
      cur.execute(sql, args)
      db.commit()
  except Exception as re:
      db.rollback()
      print(re)

def recover_data():
  f = open("C:/Users/syske/Documents/noauth.txt", encoding='utf-8',errors='ignore')
  content = f.read()
  text = json.loads(content)
  #print(text)
  #print(text['data'])
  for d in text['data']:
    #print(d)
    corpId = str(d['corpId'])
    print(corpId)
    userId = str(d['userId'])
    print(userId)
    #update_user(ding_corp_id=corpId, active='1', user_id=userId, now_active='0')
    

if __name__ == '__main__':
    recover_data()

