from flask import Flask
from flask import request,render_template,redirect,url_for,session,jsonify
import pymysql,json

app=Flask(__name__)

#user类
class User:
    ID: int
    username: str
    password: str
    permission: bool

    def __init__(self, ID=0, username='', password='', permission=0):
        self.ID = ID
        self.username = username
        self.password = password
        self.permission = permission

#定义数据库连接
def connect_db():
    db=pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Lwlllz333',
        database='h-s',
    )
    return db

#在登录之前
@app.before_request
def before_request():
    if 'user' not in session:
        session['user'] = None


#登录页面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        # 登录操作
        username=request.form.get('username',None)
        password=request.form.get('password',None)
        #连接数据库
        db=connect_db()
        cursor=db.cursor()
        cursor.execute('select * from user where username=%s and password=%s',(username,password))
        #获取查询结果
        data=cursor.fetchone( )
        if data:
            session['user']={
                'ID':data[0],
                'username':data[1],
                'permission':data[3]
            }
            cursor.close()
            db.close()
            #根据权限跳转到不同的页面
            if session['user']['permission']==0:
                return {'redirect':url_for('profile_0')}
            else:
                return {'redirect':url_for('profile_1')}
        else:
            cursor.close()
            db.close()
    return render_template('login.html')

#登录成功页面
@app.route('/profile_0')
def profile_0():
    if not session['user']:
        return redirect(url_for('login'))
    return render_template('profile_0.html')

@app.route('/profile_1',methods=['GET','POST'])
def profile_1():
    if not session['user']:
        return redirect(url_for('login'))
    if session['user']['permission'] !=1:
        return redirect(url_for('profile_0'))
    return render_template('profile_1.html')

@app.route('/admin.html')
def admin():
    if not session['user'] or session['user']['permission'] !=1:
        return redirect(url_for('login'))
    return render_template('admin.html')

#注册页面
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        #注册操作
        username=request.form.get('username',None)
        password=request.form.get('password',None)
        #连接数据库
        db=connect_db()
        cursor=db.cursor()
        #首先判断用户名是否存在
        cursor.execute('select * from user where username=%s',(username))
        #如果存在,则返回注册页面
        if cursor.fetchone():
            return render_template('register.html')
        #如果不存在,则将用户名和密码插入数据库
        else:
            #首先计算当前数据库中的用户数量
            cursor.execute('select count(*) from user')
            count=cursor.fetchone()[0]
            #把新用户的ID设置为当前用户数量+1
            ID=count+1
            #插入数据(默认权限为0)
            cursor.execute('insert into user values(%s,%s,%s,%s)',(ID,username,password,0))
            db.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

#从数据库中读取hero表中的数据,并传递给前端的profile_0.html
def get_hero():
    #连接数据库
    db=connect_db()
    cursor=db.cursor()
    cursor.execute('select HNO,HNAME from hero')
    data=cursor.fetchall()
    cursor.close()
    db.close()
    #把data转换成字典
    data=[{'HNO':i[0],'name':i[1]} for i in data]
    return data

def get_heroes():
    # 连接数据库
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT HNO, HNAME FROM hero')
    data = cursor.fetchall()
    cursor.close()
    db.close()
    # 把数据转换成字典列表
    heroes = [{'HNO': row[0], 'name': row[1]} for row in data]
    return heroes

def get_hero_skins(hero_id):
    # 连接数据库
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT SNO, SADDRESS FROM skin WHERE HNO = %s', (hero_id,))
    data = cursor.fetchall()
    cursor.close()
    db.close()
    # 把数据转换成字典列表
    skins = [{'SNO': i[0], 'SADDRESS': 'D:/LMZ/data/skinImage/' + i[1]} for i in data]
    default_skin = skins[0]['SNO'] if skins else None
    return json.dumps({'skins': skins})

# 从数据库中读取hero表中的数据，并返回给前端
@app.route('/api/heroes')
def api_heroes():
    # 连接数据库
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT HNO, HNAME FROM hero')
    data = cursor.fetchall()
    cursor.close()
    db.close()
    # 把数据转换成字典列表
    heroes = [{'HNO': row[0], 'name': row[1]} for row in data]
    return jsonify(heroes)

# 根据HNO在数据库中查询对应英雄的皮肤列表和默认皮肤
@app.route('/api/skin/<int:hero_id>', methods=['GET'])
def api_hero_skins(hero_id):
    # 连接数据库
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT SNO,SNAME,SADDRESS FROM skin WHERE HNO = %s', (hero_id))
    data = cursor.fetchall()
    cursor.close()
    db.close()
    # 把数据转换成字典列表
    skins = [{'SNO': i[0], 'SNAME': i[1],'SADDRESS': '../static/data/skinImage/' + i[2]} for i in data]
    default_skin = skins[0]['SNO'] if skins else None
    return jsonify({'skins': skins, 'defaultSkin': default_skin})

# 根据HNO在数据库中查询对应英雄的语音
@app.route('/api/voice/<int:hero_id>', methods=['GET'])
def api_hero_voice(hero_id):
    # 连接数据库
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT VNO,CONDI,VADDRESS FROM voice WHERE HNO = %s', (hero_id))
    data = cursor.fetchall()
    cursor.close()
    db.close()
    # 把数据转换成字典列表
    voices = [{'VNO': i[0], 'CONDI': i[1],'VADDRESS': '../static/data/voice/' + i[2]} for i in data]
    return jsonify({'voices': voices})


#管理员界面

#管理英雄表
#添加英雄
@app.route('/api/add/heroes',methods=['GET','POST'])
def add_hero():
    if request.method == 'POST':
        HNAME=request.form.get('heroName',None)
        db = connect_db()
        cursor = db.cursor()
        #查询英雄是否存在
        sql = "SELECT * FROM hero WHERE HNAME='%s' " % (HNAME)
        cursor.execute(sql)
        if cursor.fetchone():
            print("英雄已存在")
            return
        #查询当前最大编号
        sql = "SELECT MAX(HNO) FROM hero"
        cursor.execute(sql)
        HNO=cursor.fetchone()[0]+1
        sql = "INSERT INTO hero(HNO, HNAME) VALUES ('%d','%s')" % \
            (HNO, HNAME)
        try:
        # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        cursor.close()
        db.close()
    return redirect(url_for('admin'))

#修改英雄姓名
@app.route('/api/update/heroes',methods=['GET','POST'])
def update_hero():
    if request.method == 'POST':
        prevHeroName=request.form.get('prevHeroName',None)
        updateHeroName=request.form.get('updateHeroName',None)
        db = connect_db()
        cursor = db.cursor()
        #查询英雄是否存在
        sql = "SELECT * FROM hero WHERE HNAME='%s' " % (prevHeroName)
        cursor.execute(sql)
        if not cursor.fetchone():
            print("英雄不存在")
            return
        sql = "UPDATE hero SET HNAME='%s' WHERE HNAME='%s'" % \
            (updateHeroName, prevHeroName)
        try:
        # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        cursor.close()
        db.close()
    return redirect(url_for('admin'))

#删除英雄
@app.route('/api/delete/heroes',methods=['GET','POST'])
def delete_hero():
    if request.method == 'POST':
        heroName=request.form.get('heroName',None)
        db = connect_db()
        cursor = db.cursor()
        #查询英雄是否存在
        sql = "SELECT * FROM hero WHERE HNAME='%s' " % (heroName)
        cursor.execute(sql)
        if not cursor.fetchone():
            print("英雄不存在")
            return
        #首先删除英雄的皮肤
        sql = "DELETE FROM skin WHERE HNO=(SELECT HNO FROM hero WHERE HNAME='%s')" % (heroName)
        try:
        # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        #删除英雄的语音
        sql = "DELETE FROM voice WHERE HNO=(SELECT HNO FROM hero WHERE HNAME='%s')" % (heroName)
        try:
        # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        #删除英雄
        sql = "DELETE FROM hero WHERE HNAME='%s'" % (heroName)
        try:
        # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        cursor.close()
        db.close()
    return redirect(url_for('admin'))

#管理用户
#修改用户权限
@app.route('/api/update/permission',methods=['GET','POST'])
def update_permission():
    if request.method == 'POST':
        username=request.form.get('username',None)
        permission=request.form.get('permission',None)
        db = connect_db()
        cursor = db.cursor()
        #查询用户是否存在
        sql = "SELECT * FROM user WHERE username='%s' " % (username)
        cursor.execute(sql)
        if not cursor.fetchone():
            print("用户不存在")
            return
        sql = "UPDATE user SET permission='%s' WHERE username='%s'" % \
            (permission, username)
        try:
        # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        cursor.close()
        db.close()
    return redirect(url_for('admin'))

#修改用户密码
@app.route('/api/update/password',methods=['GET','POST'])
def update_password():
    if request.method == 'POST':
        username=request.form.get('username',None)
        password=request.form.get('password',None)
        print(request.form)
        db = connect_db()
        cursor = db.cursor()
        #查询用户是否存在
        sql = "SELECT * FROM user WHERE username='%s'" % (username)
        cursor.execute(sql)
        if not cursor.fetchone():
            print(sql)
            print("用户不存在")
            return
        sql = "UPDATE user SET password='%s' WHERE username='%s'" % \
            (password, username)
        print(sql)
        try:
        # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        cursor.close()
        db.close()
    return redirect(url_for('admin'))

#删除用户
@app.route('/api/delete/user',methods=['GET','POST'])
def delete_user():
    if request.method == 'POST':
        username=request.form.get('username',None)
        db = connect_db()
        cursor = db.cursor()
        #查询用户是否存在
        sql = "SELECT * FROM user WHERE username='%s' " % (username)
        cursor.execute(sql)
        if not cursor.fetchone():
            print("用户不存在")
            return
        sql = "DELETE FROM user WHERE username='%s'" % (username)
        try:
        # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        cursor.close()
        db.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.secret_key='jbvquywgdyudb6768qw6798632asyudgfasuydfyusgifewy2783'
    app.run('0.0.0.0', port=8080, debug=True)