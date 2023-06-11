from flask import Flask, render_template, request, jsonify, make_response
import pymysql
import bcrypt
import requests
from datetime import datetime, timedelta

# 数据库连接
db = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    db="fontlibrary",
    charset="utf8mb4"
)

dbcursor = db.cursor()
dbcursor.execute("CREATE DATABASE IF NOT EXISTS fontlibrary")

# 创建数据表
dbcursor.execute("CREATE TABLE IF NOT EXISTS `access-token`(\
                    `id` int NOT NULL AUTO_INCREMENT,\
                    `userId` int NOT NULL,\
                    `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                    `setTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                    PRIMARY KEY (`id`) USING BTREE\
                    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
dbcursor.execute("CREATE TABLE IF NOT EXISTS `usertable`  (\
                    `id` int NOT NULL AUTO_INCREMENT,\
                    `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                    `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                    `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,\
                    `createtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                    PRIMARY KEY (`id`) USING BTREE\
                    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
dbcursor.execute("CREATE TABLE IF NOT EXISTS `fontcollect`  (\
                    `id` int NOT NULL AUTO_INCREMENT,\
                    `user_id` int NULL DEFAULT NULL,\
                    `font_id` int NULL DEFAULT NULL,\
                    `set_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                    PRIMARY KEY (`id`) USING BTREE\
                    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")

app = Flask(__name__)

fontnum = [0, 0, 0, 0]
ffontnum = [0, 0, 0, 0]

'''
    请求前判断数据库连接
'''
@app.before_request
def before_request():
    if not db.open:
        db.connect()

'''
    默认进入页面
'''
@app.route('/')
def index():
    global fontnum
    global ffontnum
    sql = "SELECT * FROM `fontdata` WHERE `font_type` = 1"
    dbcursor.execute(sql,)
    zhnum= len(dbcursor.fetchall())
    sql = "SELECT * FROM `fontdata` WHERE `font_type` = 2"
    dbcursor.execute(sql,)
    ennum= len(dbcursor.fetchall())
    sql = "SELECT * FROM `fontdata` WHERE `font_type` = 3"
    dbcursor.execute(sql,)
    picnum= len(dbcursor.fetchall())
    sql = "SELECT * FROM `hotfont`"
    dbcursor.execute(sql,)
    hotnum= len(dbcursor.fetchall())
    like = 0
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if check['success']:
        userid = int(token.split('$')[2])
        sql = "SELECT * FROM `fontcollect` WHERE `user_id` = %s"
        val = (userid,)
        dbcursor.execute(sql, val)
        like = len(dbcursor.fetchall())
    fontnum = [zhnum, ennum, picnum, hotnum, like]

    sql = "SELECT * FROM `fontdata` WHERE `font_type` = 1 AND `font_free` = 1"
    dbcursor.execute(sql,)
    fzhnum= len(dbcursor.fetchall())
    sql = "SELECT * FROM `fontdata` WHERE `font_type` = 2 AND `font_free` = 1"
    dbcursor.execute(sql,)
    fennum= len(dbcursor.fetchall())
    sql = "SELECT * FROM `fontdata` WHERE `font_type` = 3 AND `font_free` = 1"
    dbcursor.execute(sql,)
    fpicnum= len(dbcursor.fetchall())
    sql = "SELECT * FROM `hotfont` WHERE `font_free` = 1"
    dbcursor.execute(sql,)
    fhotnum= len(dbcursor.fetchall())
    ffontnum = [fzhnum, fennum, fpicnum, fhotnum, like]

    return render_template('index.html')

'''
    登录请求处理
'''
@app.route('/login', methods=['POST'])
def login():
    if not db.open:
        db.connect()
    data = request.get_json()
    # print(data)
    # 从用户表中查询用户， 并对密码作出判断
    sql = "SELECT * FROM `usertable` WHERE username = %s"
    val = (data['username'],)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # 判断该用户名是否存在
    if len(result) > 0:
        # 将用户输入的密码转换为字节串
        user_password_bytes = data['password'].encode('utf-8')
        # 将数据库中的密码转换为字节串
        hashed_passowrd = result[0][2].encode('utf-8')
        # 使用 checkpw() 函数比较哈希值和用户输入的密码
        is_password_match = bcrypt.checkpw(
            user_password_bytes, hashed_passowrd)
        if is_password_match:
            # 生成accesstoken
            access = f'${result[0][3]}${result[0][0]}'
            token = bcrypt.hashpw(access.encode('utf-8'), bcrypt.gensalt())
            accesstoken = access + token.decode('utf-8')
            # print(accesstoken)
            # 将该用户原有的token删除
            sql = "DELETE FROM `access-token` WHERE `userId` = %s"
            val = (result[0][0])
            dbcursor.execute(sql, val)
            db.commit()
            # 将accesstoken存入数据库
            sql = "INSERT INTO `access-token` (`userId`, `token`) VALUES (%s, %s)"
            val = (result[0][0], accesstoken)
            dbcursor.execute(sql, val)
            db.commit()
            response = make_response(
                jsonify({'success': True, 'message': '登录成功'}))
            response.set_cookie('access-token', accesstoken,
                                max_age=15*24*3600, httponly=True)
            return response
        else:
            return jsonify({'success': False, 'message': '用户名或密码不正确'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码不正确'})

'''
    注册请求处理
'''
@app.route('/register', methods=['POST'])
def register():
    if not db.open:
        db.connect()
    data = request.get_json()
    # print(data)
    sql = "SELECT * FROM `usertable` WHERE username = %s"
    val = (data['username'],)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # 判断该用户名是否存在
    if len(result) > 0:
        return jsonify({'success': False, 'message': '注册失败\n用户名已存在'})
    else:
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO `usertable` (`username`, `password`, `nickname`) VALUES (%s, %s, %s)"
        val = (data['username'], hashed_password, data['username'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '注册成功'})

'''
    获取字体信息
'''
@app.route('/getFont', methods=['POST'])
def getFont():
    data = request.get_json()
    perPageNum = data['num']
    free = data['free']
    if free != 1:
        free = (0, -1, 1)
    else:
        free = (1,)
    getId = perPageNum * (data['page'] - 1)
    if data['type'] == 'en':
        sql = "SELECT * FROM `fontdata` WHERE `font_type` = 2 AND `font_free` IN %s ORDER BY id LIMIT %s OFFSET %s"
        val = (free, perPageNum, getId)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    elif data['type'] == 'pic':
        sql = "SELECT * FROM `fontdata` WHERE `font_type` = 3 AND `font_free` IN %s ORDER BY id LIMIT %s OFFSET %s"
        val = (free, perPageNum, getId)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    elif data['type'] == 'home':
        sql = "SELECT * FROM `hotfont` WHERE `font_free` IN %s ORDER BY id LIMIT %s OFFSET %s"
        val = (free, perPageNum, getId)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    elif data['type'] == 'zh':
        sql = "SELECT * FROM `fontdata` WHERE `font_type` = 1 AND `font_free` IN %s ORDER BY id LIMIT %s OFFSET %s"
        val = (free, perPageNum, getId)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    elif data['type'] == 'like':
        token = request.cookies.get('access-token')
        check = checkCookie(token)
        if check['success']:
            userid = int(token.split('$')[2])
            sql = "SELECT * FROM `fontdata` JOIN `fontcollect` ON fontdata.id = fontcollect.font_id WHERE fontcollect.user_id = %s ORDER BY fontcollect.id DESC LIMIT %s OFFSET %s"
            val = (userid, perPageNum, getId)
            dbcursor.execute(sql, val)
            result = dbcursor.fetchall()
    return jsonify({'success': True, 'data': result})

'''
    获取下载链接
'''
@app.route('/download', methods=['POST'])
def download():
    token = request.cookies.get('access-token')
    # print(token)
    check = checkCookie(token)
    if check['success']:
        data = request.get_json()
        # 定义请求的 URL
        url = "https://www.fonts.net.cn/font-download.html"
        # 发送 POST 请求
        response = requests.post(url, data=data)
        # 获取响应结果
        if response.status_code == 200:
            if response.json()['success'] == True:
                result = response.json()['data']['url']
                return jsonify({'success': True, 'data': result})
            else:
                return jsonify({'success': False, 'data': response.status_code})
        else:
            return jsonify({'success': False, 'data': response.status_code})
    else:
        return jsonify({'success': False, 'data': 'cookieErr', 'message': check['message']})
    
'''
    获取收藏列表
'''
@app.route('/getCollect', methods=['POST'])
def getCollect():
    token = request.cookies.get('access-token')
    # print(token)
    check = checkCookie(token)
    if check['success']:
        userid = int(token.split('$')[2])
        sql = "SELECT * FROM `fontcollect` WHERE `user_id` = %s"
        val = (userid,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'data': []})
    
'''
    更新收藏列表
'''
@app.route('/changeCollect', methods=['POST'])
def changeCollect():
    data = request.get_json()
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if check['success']:
        userid = int(token.split('$')[2])
        if data['flag'] == 0:
            sql = "INSERT INTO `fontcollect` (`user_id`, `font_id`) VALUES (%s, %s)"
            val = (userid, data['fontid'])
            dbcursor.execute(sql, val)
            db.commit()
        if data['flag'] == 1:
            sql = "DELETE FROM `fontcollect` WHERE id = %s"
            val = (data['collectid'],)
            dbcursor.execute(sql, val)
            db.commit()
        return jsonify({'success': True, 'data': ''})
    else:
        return jsonify({'success': False, 'data': '登陆后方可使用收藏功能'})

'''
    获取字体每种类型的数量
'''
@app.route('/getFontNum', methods=['POST'])
def getFontNum():
    data = request.get_json()
    like = 0
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if check['success']:
        userid = int(token.split('$')[2])
        sql = "SELECT * FROM `fontcollect` WHERE `user_id` = %s"
        val = (userid,)
        dbcursor.execute(sql, val)
        like = len(dbcursor.fetchall())
    fontnum[4] = like
    ffontnum[4] = like

    if data['free'] == 1:
        return jsonify({'success': True, 'data': ffontnum})
    else:
        return jsonify({'success': True, 'data': fontnum})

'''
    返回用户登录状态
'''
@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if check['success']:
        return jsonify({'success': True, 'data': ''})
    else:
        return jsonify({'success': False, 'data': ''})
    
'''
    清除前端cookie
'''
@app.route('/clearCookie', methods=['POST'])
def clearCookie():
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if check['success']:
        sql = "DELETE FROM `access-token` WHERE `token` = %s"
        val = (token)
        dbcursor.execute(sql, val)
        db.commit()
    response = make_response()
    response.set_cookie('access-token', '', expires=0, httponly=True)
    return response

'''
    校验登录状态
'''
@app.route('/userCheckCookie', methods=['POST'])
def userCheckCookie():
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if check['success']:
        return jsonify({'success': True, 'data': ''})
    else:
        return jsonify({'success': False, 'data': ''})

'''
    返回字体搜索结果
'''
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    key = '%' + data['key'] + '%'
    free = data['free']
    perPageNum = data['num']
    getId = perPageNum * (data['page'] - 1)
    if free != 1:
        free = (0, -1, 1)
    else:
        free = (1,)
    sql = "SELECT * FROM `fontdata` WHERE `font_name` like %s AND `font_free` IN %s"
    val = (key, free)
    dbcursor.execute(sql, val)
    fontnum = len(dbcursor.fetchall())
    sql = "SELECT * FROM `fontdata` WHERE `font_name` like %s AND `font_free` IN %s ORDER BY id LIMIT %s OFFSET %s"
    val = (key, free, perPageNum, getId)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    return jsonify({'success': True, 'data': result, 'fontnum': fontnum})

def checkCookie(token):
    sql = "SELECT * FROM `access-token` WHERE `token` = %s"
    val = (token,)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    if len(result) > 0:
        current_time = datetime.now() 
        if isTimeOut(result[0][3], current_time):
            return ({'success': False, 'message': '登陆已过期，请重新登录'})
        return  ({'success': True, 'message': '可下载'})
    else:
        return ({'success': False, 'message': '登陆后方可下载'})

def isTimeOut(time1, time2):
    # 计算时间差值
    difference = abs(time2 - time1)
    # 判断差值是否大于15天
    if difference.days > 15:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)