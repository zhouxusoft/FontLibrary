import requests
import pymysql

# 数据库连接
db = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    charset="utf8mb4"
)

dbcursor = db.cursor()
dbcursor.execute("CREATE DATABASE IF NOT EXISTS font")
dbcursor.execute("USE font")

#创建数据表
dbcursor.execute("CREATE TABLE IF NOT EXISTS `fontdata` (\
                    `id` int NOT NULL AUTO_INCREMENT,\
                    `font_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_imgurl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_download` int NULL DEFAULT NULL,\
                    `font_viewnum` int NULL DEFAULT NULL,\
                    PRIMARY KEY (`id`) USING BTREE\
                    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
dbcursor.execute("CREATE TABLE IF NOT EXISTS `fonttype` (\
                    `id` int NOT NULL AUTO_INCREMENT,\
                    `type_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    PRIMARY KEY (`id`) USING BTREE\
                    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")


keyword = input('搜索：')
# url = f'https://www.fonts.net.cn/font-search-result.html?q={keyword}'
url = 'https://www.fonts.net.cn/fonts-zh-1.html'
response = requests.get(url)
data = response.content.decode('utf-8', 'ignore')

data = data.split('<ul class="site_font_list">')[1]
data = data.split('</ul>')[0]

datas = data.split('</li>')
# print(datas[0])

for i in datas:
    if i == '':
        continue
    else:
        print('-' * 100)
        # 分割出字体名称
        fontName = i.split('title="')[1]
        fontName = fontName.split('"')[0]
        print('字体名称：', fontName)
        # 分割出字体编号
        fontId = i.split('font-detail-link="')[1]
        fontId = fontId.split('"')[0]
        print('字体编号：', fontId)
        # 分割出字体类型
        fontType = i.split('title="')[2]
        fontType = fontType.split('"')[0]
        print('字体类型：', fontType)
        # 分割出字体图片链接
        fontImg = i.split('<img src="')[1]
        fontImg = 'https:' + fontImg.split('"')[0]
        print('字体图片：', fontImg)
        # 分割出字体可下载信息
        fontDownload = i.split('icon-download">')
        if len(fontDownload) > 1:
            fontDownload = 1
        else:
            fontDownload = 0
        print('支持下载：', fontDownload)
        # 分割出字体的浏览次数
        fontViewNum = i.split('<p><span>共')[1]
        fontViewNum = fontViewNum.split('次浏览</span></p>')[0]
        fontViewNum = int(fontViewNum)
        print('浏览次数：', fontViewNum)

        # 判断此字体类型是否已经存在于字体类型数据表中
        sql = "SELECT * FROM fonttype WHERE type_name = %s"
        val = (fontType,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        # 若存在 则找到这个字体类型的id
        if len(result) > 0:
            fontTypeId = result[0][0]
        # 若不存在 则创建该类型 并获得分配的id
        else:
            sql = "INSERT INTO fonttype (type_name) VALUES (%s)"
            val = (fontType,)
            dbcursor.execute(sql, val)
            db.commit()
            sql = "SELECT * FROM fonttype WHERE type_name = %s"
            val = (fontType,)
            dbcursor.execute(sql, val)
            result = dbcursor.fetchall()
            fontTypeId = result[0][0]

        # 将字体数据插入字体数据表中
        sql = "INSERT INTO fontdata (font_name, font_number, font_type, font_imgurl, font_download, font_viewnum) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (fontName, fontId, fontTypeId, fontImg, fontDownload, fontViewNum)
        dbcursor.execute(sql, val)
        db.commit()