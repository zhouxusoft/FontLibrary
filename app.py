from flask import Flask, render_template, request, jsonify, make_response
import pymysql
import bcrypt
import requests

db = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    charset="utf8mb4"
)

dbcursor = db.cursor()
dbcursor.execute("CREATE DATABASE IF NOT EXISTS fontlibrary")
dbcursor.execute("USE fontlibrary")

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

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
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
                jsonify({'success': True, 'message': '登陆成功'}))
            response.set_cookie('access-token', accesstoken,
                                max_age=15*24*3600, httponly=True)
            return response
        else:
            return jsonify({'success': False, 'message': '用户名或密码不正确'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码不正确'})


@app.route('/register', methods=['POST'])
def register():
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


@app.route('/getFont', methods=['POST'])
def getFont():
    data = request.get_json()
    getId = 15 * (data['page'] - 1) + 1
    if data['type'] == 'en':
        getId = getId + 7736
        sql = "SELECT * FROM `fontdata` WHERE id >= %s AND id <= 39231 ORDER BY id LIMIT 20"
        val = (getId,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    elif data['type'] == 'pic':
        getId = getId + 39231
        sql = "SELECT * FROM `fontdata` WHERE id >= %s ORDER BY id LIMIT 20"
        val = (getId,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    elif data['type'] == 'home':
        getId = getId - 1
        sql = "SELECT * FROM `hotfont` LIMIT 20 OFFSET %s"
        val = (getId,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    else:
        sql = "SELECT * FROM `fontdata` WHERE id >= %s AND id <= 7736 ORDER BY id LIMIT 20"
        val = (getId,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    return jsonify({'success': True, 'data': result})


@app.route('/download', methods=['POST'])
def download():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
