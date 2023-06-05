import pymysql

# 数据库连接
db = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    charset="utf8mb4"
)

dbcursor = db.cursor()
dbcursor.execute("CREATE DATABASE IF NOT EXISTS fontlibrary")
dbcursor.execute("USE fontlibrary")

#创建数据表
dbcursor.execute("CREATE TABLE IF NOT EXISTS `hotfont` (\
                    `id` int,\
                    `font_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_imgurl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_preview` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_download` int NULL DEFAULT NULL,\
                    `font_viewnum` int NULL DEFAULT NULL,\
                    PRIMARY KEY (`id`) USING BTREE\
                    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")


sql = 'SELECT * FROM `fontdata` ORDER BY `font_viewnum` DESC LIMIT 100'
dbcursor.execute(sql)
result = dbcursor.fetchall()

print(result[0])

for i in result:
    sql = "INSERT INTO `hotfont` (id, font_name, font_number, font_type, font_imgurl, font_preview, font_download, font_viewnum) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
    dbcursor.execute(sql, val)
    db.commit()