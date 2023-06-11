from pymysql import Connection

class GetTop():
    def get_info(self): # 获取数据库中的用户信息(用户名和密码)
        pass
    def dict_info(self): # 把用户名和密码保存为字典
        pass

class Get(GetTop):

    def __init__(self):
        self.data_pass = None
        self.data_name = None

    def __get_info(self):
        conn = Connection(
            host='主机',
            port=3306,
            user='用户名',
            password='密码',
            autocommit=True
        )
        cursor = conn.cursor()
        conn.select_db('库名')
        cursor.execute('select name from 表名')
        self.data_name = cursor.fetchall()
        cursor.execute('select password from 表名')
        self.data_pass = cursor.fetchall()
        conn.close()
        return self.data_name,self.data_pass
    def dict_info(self):
        user_name_list = []
        password_list = []
        for username in self.__get_info()[0]:
            user_name_list.append(username[0])
        for password in self.__get_info()[1]:
            password_list.append(password[0])
        user_info_dict = dict(zip(user_name_list, password_list))
        return user_info_dict

if __name__ == '__main__':
    get = Get()
    print(get.dict_info())