from flask import Flask
from flask import request,render_template,redirect,url_for,session,g
import pymysql

app=Flask(__name__)

#user类
class User:
    ID: int
    username: str
    password: str
    permission: bool

#在登录之前
@app.before_request
def before_request():
    g.user=None


#登录页面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        # 登录操作
        username=request.form.get('username',None)
        password=request.form.get('password',None)
        print(username,password)
        print(request.form)
        #连接数据库
        db=pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Lwlllz333',
            database='h-s',
        )
        cursor=db.cursor()
        cursor.execute('select * from user where username=%s and password=%s',(username,password))
        #获取查询结果
        data=cursor.fetchone()
        if data:
            user=User()
            user.ID=data[0]
            user.username=data[1]
            user.password=data[2]
            user.permission=data[3]
            session['user_id']=user.ID
            g.user=user
            return redirect(url_for('profile'))
    return render_template('login.html')

#登录成功页面
@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('profile.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)