import requests
import pymysql
import time
import random

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
dbcursor.execute("CREATE TABLE IF NOT EXISTS `fontdata` (\
                    `id` int NOT NULL AUTO_INCREMENT,\
                    `font_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_imgurl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_preview` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    `font_download` int NULL DEFAULT NULL,\
                    `font_viewnum` int NULL DEFAULT NULL,\
                    PRIMARY KEY (`id`) USING BTREE\
                    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")
dbcursor.execute("CREATE TABLE IF NOT EXISTS `fonttype` (\
                    `id` int NOT NULL AUTO_INCREMENT,\
                    `type_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,\
                    PRIMARY KEY (`id`) USING BTREE\
                    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;")


'''
    搜索获取字体信息
'''
# keyword = input('搜索：')
# url = f'https://www.fonts.net.cn/font-search-result.html?q={keyword}'
# response = requests.get(url)
# data = response.content.decode('utf-8', 'ignore')

# data = data.split('<ul class="site_font_list">')[1]
# data = data.split('</ul>')[0]

# datas = data.split('</li>')
# # print(datas[0])

# for i in datas:
#     if i == '':
#         continue
#     else:
#         print('-' * 100)
#         # 分割出字体名称
#         fontName = i.split('title="')[1]
#         fontName = fontName.split('"')[0]
#         print('字体名称：', fontName)
#         # 分割出字体编号
#         fontId = i.split('font-detail-link="')[1]
#         fontId = fontId.split('"')[0]
#         print('字体编号：', fontId)
#         # 分割出字体类型
#         fontType = i.split('title="')[2]
#         fontType = fontType.split('"')[0]
#         print('字体类型：', fontType)
#         # 分割出字体图片链接
#         fontImg = i.split('<img src="')[1]
#         fontImg = 'https:' + fontImg.split('"')[0]
#         print('字体图片：', fontImg)
#         # 分割出字体可下载信息
#         fontDownload = i.split('icon-download">')
#         if len(fontDownload) > 1:
#             fontDownload = 1
#         else:
#             fontDownload = 0
#         print('支持下载：', fontDownload)
#         # 分割出字体预览链接
#         fontPreview = i.split('preview-file="')[1]
#         fontPreview = fontPreview.split('"')[0]
#         print('预览链接：', fontPreview)
#         # https://previewer.fonts.net.cn/canvas.php?font=41579-038eb649ff913a15f440145abc1b32aa.ttf&text=%E8%BE%BE%E7%93%A6

#         # 分割出字体的浏览次数
#         fontViewNum = i.split('<p><span>共')[1]
#         fontViewNum = fontViewNum.split('次浏览</span></p>')[0]
#         fontViewNum = int(fontViewNum)
#         print('浏览次数：', fontViewNum)

#         # 判断此字体类型是否已经存在于字体类型数据表中
#         sql = "SELECT * FROM fonttype WHERE type_name = %s"
#         val = (fontType,)
#         dbcursor.execute(sql, val)
#         result = dbcursor.fetchall()
#         # 若存在 则找到这个字体类型的id
#         if len(result) > 0:
#             fontTypeId = result[0][0]
#         # 若不存在 则创建该类型 并获得分配的id
#         else:
#             sql = "INSERT INTO fonttype (type_name) VALUES (%s)"
#             val = (fontType,)
#             dbcursor.execute(sql, val)
#             db.commit()
#             sql = "SELECT * FROM fonttype WHERE type_name = %s"
#             val = (fontType,)
#             dbcursor.execute(sql, val)
#             result = dbcursor.fetchall()
#             fontTypeId = result[0][0]

#         # 将字体数据插入字体数据表中
#         sql = "INSERT INTO fontdata (font_name, font_number, font_type, font_imgurl, font_preview, font_download, font_viewnum) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#         val = (fontName, fontId, fontTypeId, fontImg, fontPreview, fontDownload, fontViewNum)
#         dbcursor.execute(sql, val)
#         db.commit()

'''
    获取中文字体分类的字体信息
'''
for j in range(1, 774):
    url = f'https://www.fonts.net.cn/fonts-zh-{j}.html'
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
            # 分割出字体预览链接
            fontPreview = i.split('preview-file="')
            if len(fontPreview) > 1:
                fontPreview = fontPreview[1]
                fontPreview = fontPreview.split('"')[0]
            else:
                fontPreview = '无法预览'
            print('预览链接：', fontPreview)
            # https://previewer.fonts.net.cn/canvas.php?font=41579-038eb649ff913a15f440145abc1b32aa.ttf&text=%E8%BE%BE%E7%93%A6

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
            sql = "INSERT INTO fontdata (font_name, font_number, font_type, font_imgurl, font_preview, font_download, font_viewnum) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (fontName, fontId, fontTypeId, fontImg, fontPreview, fontDownload, fontViewNum)
            dbcursor.execute(sql, val)
            db.commit()
    print('=' * 100)
    print('-+-中文字体-+-\n当前第', j, '页')
    print('=' * 100)
    randomnum = random.randint(0, 1000)
    stime = randomnum / 1000
    time.sleep(stime)

'''
    获取英文字体分类的字体信息
'''
for j in range(1, 3151):
    url = f'https://www.fonts.net.cn/fonts-en-{j}.html'
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
            # 分割出字体预览链接
            fontPreview = i.split('preview-file="')
            if len(fontPreview) > 1:
                fontPreview = fontPreview[1]
                fontPreview = fontPreview.split('"')[0]
            else:
                fontPreview = '无法预览'
            print('预览链接：', fontPreview)
            # https://previewer.fonts.net.cn/canvas.php?font=41579-038eb649ff913a15f440145abc1b32aa.ttf&text=%E8%BE%BE%E7%93%A6

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
            sql = "INSERT INTO fontdata (font_name, font_number, font_type, font_imgurl, font_preview, font_download, font_viewnum) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (fontName, fontId, fontTypeId, fontImg, fontPreview, fontDownload, fontViewNum)
            dbcursor.execute(sql, val)
            db.commit()
    print('=' * 100)
    print('-+-英文字体-+-\n当前第', j, '页')
    print('=' * 100)
    randomnum = random.randint(0, 1000)
    stime = randomnum / 1000
    time.sleep(stime)

'''
    获取图型字体分类的字体信息
'''
for j in range(1, 263):
    url = f'https://www.fonts.net.cn/fonts-pic-{j}.html'
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
            # 分割出字体预览链接
            fontPreview = i.split('preview-file="')
            if len(fontPreview) > 1:
                fontPreview = fontPreview[1]
                fontPreview = fontPreview.split('"')[0]
            else:
                fontPreview = '无法预览'
            print('预览链接：', fontPreview)
            # https://previewer.fonts.net.cn/canvas.php?font=41579-038eb649ff913a15f440145abc1b32aa.ttf&text=%E8%BE%BE%E7%93%A6

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
            sql = "INSERT INTO fontdata (font_name, font_number, font_type, font_imgurl, font_preview, font_download, font_viewnum) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (fontName, fontId, fontTypeId, fontImg, fontPreview, fontDownload, fontViewNum)
            dbcursor.execute(sql, val)
            db.commit()
    print('=' * 100)
    print('-+-图形字体-+-\n当前第', j, '页')
    print('=' * 100)
    randomnum = random.randint(0, 1000)
    stime = randomnum / 1000
    time.sleep(stime)