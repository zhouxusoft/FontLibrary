from flask import Flask, render_template, request, jsonify
import pymysql

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
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
