import requests

# keyword = input('搜索：')
keyword = '中文'
url = f'https://www.fonts.net.cn/font-search-result.html?q={keyword}'
response = requests.get(url)
data = response.content.decode('utf-8', 'ignore')

data = data.split('<ul class="site_font_list">')[1]
data = data.split('</ul>')[0]

datas = data.split('</li>')
print(datas[0])

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