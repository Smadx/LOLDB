import pymysql

DBHOST='localhost'
DBUSER='root'
DBPASS='123456'
DBNAME='lol'

#链接数据库
def get_db():
    try:
        db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS,database=DBNAME)
        print("数据库成功连接！")
    except:
        db = None
    return db

def db_close():
    db = get_db()
    if db is not None:
        db.close()

# 增加英雄
def add_hero(HNO, HNAME):
    db = get_db()
    cursor = db.cursor()
    sql = "INSERT INTO hero(HNO, HNAME) VALUES ('%d','%s')" % \
        (HNO, HNAME)
    try:
    # 执行sql语句
        cursor.execute(sql)
        print(cursor.rowcount)  # 打印插入的行数
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

# 修改英雄姓名
def update_hero(prev_name, HNAME):
    db = get_db()
    cursor = db.cursor()
    sql = "UPDATE hero SET HNAME='%s' WHERE HNAME=%s" % \
        (HNAME, prev_name)
    try:
        # 执行sql语句
        cursor.execute(sql)
        print(cursor.rowcount)  # 打印更新的行数
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

# 删除英雄
def delete_role(HNAME):
    db = get_db()
    cursor = db.cursor()
    sql = "DELETE FROM hero WHERE HNAME=%s" % (HNAME)
    try:
        # 执行sql语句
        cursor.execute(sql)
        print(cursor.rowcount)  # 打印删除的行数
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()


#用户表   
# 修改用户权限
def update_user(username, permission):
    db = get_db()
    cursor = db.cursor()
    sql = "UPDATE user SET permission='%d' WHERE username=%s" % \
        (permission, username)
    try:
        # 执行sql语句
        cursor.execute(sql)
        print(cursor.rowcount)  # 打印更新的行数
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

# 修改用户密码
def update_user(username, password):
    db = get_db()
    cursor = db.cursor()
    sql = "UPDATE user SET password='%s' WHERE username=%s" % \
        (password,username)
    try:
        # 执行sql语句
        cursor.execute(sql)
        print(cursor.rowcount)  # 打印更新的行数
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

#删除用户
def delete_user(username):
    db = get_db()
    cursor = db.cursor()
    sql = "DELETE FROM user WHERE username=%s" % (username)
    try:
        # 执行sql语句
        cursor.execute(sql)
        print(cursor.rowcount)  # 打印删除的行数
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()