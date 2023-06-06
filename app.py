from flask import Flask, render_template, request, jsonify
import pymysql
import bcrypt

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
    print(data)
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
        is_password_match = bcrypt.checkpw(user_password_bytes, hashed_passowrd)
        if is_password_match:
            return jsonify({'success': True, 'message': '登陆成功'})
        else:
            return jsonify({'success': False, 'message': '用户名或密码不正确'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码不正确'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    sql = "SELECT * FROM `usertable` WHERE username = %s"
    val = (data['username'],)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # 判断该用户名是否存在
    if len(result) > 0:
        return jsonify({'success': False, 'message': '用户名已存在'})
    else:
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO `usertable` (`username`, `password`, `nickname`) VALUES (%s, %s, %s)"
        val = (data['username'], hashed_password, data['username'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '注册成功'})
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
