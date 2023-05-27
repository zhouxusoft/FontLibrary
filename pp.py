import requests
import pymysql

db = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    charset="utf8mb4"
)

dbcursor = db.cursor()
dbcursor.execute("CREATE DATABASE IF NOT EXISTS font")
dbcursor.execute("USE font")

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
        fontName = i.split('title="')[1]
        fontName = fontName.split('"')[0]
        print('字体名称：' + fontName)

        fontId = i.split('font-detail-link="')[1]
        fontId = fontId.split('"')[0]
        print('字体编号：' + fontId)

        fontType = i.split('title="')[2]
        fontType = fontType.split('"')[0]
        print('字体类型：' + fontType)

        fontImg = i.split('<img src="')[1]
        fontImg = 'https:' + fontImg.split('"')[0]
        print('字体图片：' + fontImg)

        fontDownload = i.split('icon-download">')
        if len(fontDownload) > 1:
            fontDownload = '本地下载'
        else:
            fontDownload = '无法下载'
        print('字体下载：' + fontDownload)

        fontViewNum = i.split('<p><span>共')[1]
        fontViewNum = fontViewNum.split('次浏览</span></p>')[0]
        print('浏览次数：' + fontViewNum)