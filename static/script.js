const router = new ApeeRouter()

// 获得当前页面的路由
let currentRoute = ''
// 设置当前的页码
let currentPage = 1
// 存储当前页的字体
let currentFonts = []
// 存储下载链接
let downloadUrl = ''
// 存储用户的收藏列表
let userCollect = []
// 存储每种字体的数量
let fontNum = []
// 定义每一页的字体数量
let perPageNum = 20
// 记录用户的登陆状态
let userLogin = false
// 存储当前字体的预览码
let fontPreviewNum = ''
// 存储用户对当前字体的收藏状态
let collectFlag = 0
// 记录当前的选择是否免费
let fontFree = 0
// 记录当前的搜索关键字
let searchKey = ''
// 记录搜索结果的数量
let searchFontNum = 0

// 设置背景色
const whiteBg = (route) => {
    document.body.style.backgroundColor = 'white'
    currentRoute = router.getNowRouteName()
}
// 设置背景色
const smokeBg = (route) => {
    document.body.style.backgroundColor = 'whitesmoke'
    currentRoute = router.getNowRouteName()
    $("html, body").animate({ scrollTop: 0 }, 300)
    getCollect()
    setFreeBtn()
}
// 设置用户中心按钮样式
function setUserFont() {
    $.ajax({
        url: '/checkLogin',
        type: 'POST',
        contentType: 'application/json',
        async: false,
        success: function (response) {
            if (response.success) {
                $('.user-font').text('\uf21b')
                $('.custom-dropdown-menu').empty()
                $('.custom-dropdown-menu').append(`
                    <li><a class="dropdown-item" id="mycollect" href="#/like">我的收藏</a></li>
                    <li><span class="dropdown-item" id="logout" data-bs-toggle="modal"
                    data-bs-target="#logoutmodal">退出登录</span></li>
                `)
                $('#yeslogout').click(function () {
                    clearCookie()
                })
                $('#mycollect').click(function () {
                    let toSend = {
                        page: currentPage,
                        type: currentRoute,
                        num: perPageNum
                    }
                    $.ajax({
                        url: '/getFont',
                        type: 'POST',
                        data: JSON.stringify(toSend),
                        contentType: 'application/json',
                        async: false,
                        success: function (response) {
                            // console.table(response.data)
                            currentFonts = response.data
                        },
                        error: function (error) {
                            console.log(error)
                        }
                    })
                    setFonts()
                })
            } else {
                $('.user-font').text('\uf007')
                $('.custom-dropdown-menu').empty()
                $('.custom-dropdown-menu').append(`
                    <li><a class="dropdown-item" href="#/login">前往登录</a></li>
                `)
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}
setUserFont()
// 获取每种字体的数量
function getFontNum() {
    let toSend = {
        free: fontFree
    }
    $.ajax({
        url: '/getFontNum',
        type: 'POST',
        data: JSON.stringify(toSend),
        contentType: 'application/json',
        async: false,
        success: function (response) {
            fontNum = response.data
            // console.log(fontNum)
        },
        error: function (error) {
            console.log(error)
        }
    })
}
getFontNum()
// 获取当前类型字体的页数
function getMaxPage() {
    if (currentRoute == 'home') {
        return Math.ceil(fontNum[3] / perPageNum)
    } else if (currentRoute == 'zh') {
        return Math.ceil(fontNum[0] / perPageNum)
    } else if (currentRoute == 'en') {
        return Math.ceil(fontNum[1] / perPageNum)
    } else if (currentRoute == 'pic') {
        return Math.ceil(fontNum[2] / perPageNum)
    } else if (currentRoute == 'like') {
        return Math.ceil(fontNum[4] / perPageNum)
    } else if (currentRoute == 'search') {
        return Math.ceil(searchFontNum / perPageNum)
    }
}
// 获取当前页面的字体信息
function getFonts() {
    let toSend = {
        page: currentPage,
        type: currentRoute,
        num: perPageNum,
        free: fontFree
    }
    $.ajax({
        url: '/getFont',
        type: 'POST',
        data: JSON.stringify(toSend),
        contentType: 'application/json',
        async: false,
        success: function (response) {
            // console.table(response.data)
            currentFonts = response.data
        },
        error: function (error) {
            console.log(error)
        }
    })
    setFonts()
}
// 设置翻页时下面显示的当前页码和总页码
function setShowPage() {
    $('.all-page').text(getMaxPage())
    $('.current-page').text(currentPage)
}
// 显示下载弹窗
function showDownload(fontid) {
    for (let i = 0; i < currentFonts.length; i++) {
        if (currentFonts[i][2] == fontid) {
            $('#downloadfontimg').prop('src', currentFonts[i][4])
            break
        }
    }
    $('#downloadbtn').click()
    $('#yesdownload').click(function () {
        downloadFont()
    })
}
// 下载字体方法
function downloadFont() {
    let iframe_box = document.querySelector('#iframe_box')
    while (iframe_box.firstChild) {
        iframe_box.removeChild(iframe_box.firstChild)
    }
    iframe_box.innerHTML = iframe_box.innerHTML + '<iframe src="' + downloadUrl + '"><iframe>'
}
// 获取下载链接
function getDownloadUrl(fontid) {
    let toSend = {
        id: fontid,
        type: 'font'
    }
    $.ajax({
        url: '/download',
        type: 'POST',
        data: JSON.stringify(toSend),
        contentType: 'application/json',
        success: function (response) {
            if (response.success == true) {
                // console.log(response.data)
                downloadUrl = response.data
                showDownload(fontid)
            } else {
                if (response.data == 'cookieErr') {
                    clearCookie()
                    alert(response.message)
                } else {
                    alert('该字体暂时无法下载')
                }
            }
        },
        error: function (error) {
            // console.log(error)
            alert('服务器开小差了\n请稍后再试')
        }
    })
}
// 获取链接并下载
function getAndDownloadUrl(fontid) {
    let toSend = {
        id: fontid,
        type: 'font'
    }
    $.ajax({
        url: '/download',
        type: 'POST',
        data: JSON.stringify(toSend),
        contentType: 'application/json',
        success: function (response) {
            if (response.success == true) {
                // console.log(response.data)
                downloadUrl = response.data
                downloadFont()
            } else {
                if (response.data == 'cookieErr') {
                    clearCookie()
                    alert(response.message)
                } else {
                    alert('该字体暂时无法下载')
                }
            }
        },
        error: function (error) {
            // console.log(error)
            alert('服务器开小差了\n请稍后再试')
        }
    })
}
// 获取收藏夹字体信息
function getCollect() {
    $.ajax({
        url: '/getCollect',
        type: 'POST',
        contentType: 'application/json',
        async: false,
        success: function (response) {
            if (response.success == true) {
                userCollect = response.data
                if (collectFlag) {
                    $('#fontinfocollect').text('收藏')
                } else {
                    $('#fontinfocollect').text('已收藏')
                }
            } else {
                userCollect = []
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}
// 点击收藏效果
function fontCollect(fontid) {
    // 判断当前字体的id
    for (let i = 0; i < currentFonts.length; i++) {
        if (currentFonts[i][2] == fontid) {
            fontid = currentFonts[i][0]
            break
        }
    }
    let toSend = {
        fontid: fontid,
    }
    collectFlag = 0
    // 判断当前字体收藏状态
    for (let i = 0; i < userCollect.length; i++) {
        if (userCollect[i][2] == fontid) {
            collectFlag = 1
            toSend.collectid = userCollect[i][0]
            break
        }
    }
    toSend.flag = collectFlag
    // 发送收藏修改请求
    $.ajax({
        url: '/changeCollect',
        type: 'POST',
        data: JSON.stringify(toSend),
        contentType: 'application/json',
        async: false,
        success: function (response) {
            if (response.success == true) {
                getCollect()
                // 更新前端显示效果
                if (collectFlag) {
                    let select = '[data-font-id="' + fontid + '"]'
                    $(select).find('span').css('font-weight', '300')
                } else {
                    let select = '[data-font-id="' + fontid + '"]'
                    $(select).find('span').css('font-weight', '600')
                }
            } else {
                alert(response.data)
            }
        },
        error: function (error) {
            console.log(error)
            alert('服务器开小差了\n请稍后再试')
        }
    })
}
// 获取每日一言 
function getSentence() {
    let text = '我会一直写代码，直到我看不清屏幕的那一天。'
    let xhr = new XMLHttpRequest()
    xhr.open('POST', 'https://v1.hitokoto.cn/', false)
    xhr.send()
    let resData = JSON.parse(xhr.responseText)
    if (resData) {
        text = resData.hitokoto
    }
    return text
}
// 设置页面 显示当前的字体信息
function setFonts() {
    let select = '#font-box-' + currentRoute
    $(select).empty()
    for (let i = 0; i < currentFonts.length; i++) {
        const element = currentFonts[i]
        if (element[3] == 1) {
            element[3] = '中文字体'
        } else if (element[3] == 2) {
            element[3] = '英文字体'
        } else {
            element[3] = '图形字体'
        }
        /**
         * <span class="badge bg-success d-flex align-items-center ml-3">商用免费</span>
         * <span class="badge bg-danger d-flex align-items-center ml-3">付费</span>
         */
        if (element[6] == 0) {
            $(select).append(`
                <div class="col-sm-12 p-3 my-2 rounded bg-white text-white fontdata-border-box" data-font-number="${element[2]}">
                    <div class="text-dark d-flex align-items-center justify-content-between">
                        <span class="font-top-name d-flex" data-font-id-name="${element[0]}">${element[1]}
                            <div class="p-2"></div>
                        </span>
                        <span class="font-top-type">${element[3]}</span>
                    </div>
                    <div class="hr-i"></div>
                    <div class="font-img-box d-flex align-items-center justify-content-between">
                        <div class="font-img">
                            <img src="${element[4]}" class="img-fluid" alt="">
                        </div>
                        <div class="font-img-down d-none d-sm-block">
                            <button class="btn btn-primary mr-2 fontstar" id="fontcollect" data-font-id="${element[0]}"><span class="collect-font">\uf005</span>收藏</button>
                            <button class="btn btn-success fontdownload" id="fontdownload" disabled>下载</button>
                            <div class="text-dark d-flex justify-content-end pt-3">
                                <span class="font-img-viewnum">共${element[7]}次浏览</span>
                            </div>
                        </div>
                    </div>
                </div>
            `)
        } else {
            $(select).append(`
                <div class="col-sm-12 p-3 my-2 rounded bg-white text-white fontdata-border-box" data-font-number="${element[2]}">
                    <div class="text-dark d-flex align-items-center justify-content-between">
                        <span class="font-top-name d-flex" data-font-id-name="${element[0]}">${element[1]}
                            <div class="p-2"></div>
                        </span>
                        <span class="font-top-type">${element[3]}</span>
                    </div>
                    <div class="hr-i"></div>
                    <div class="font-img-box d-flex align-items-center justify-content-between">
                        <div class="font-img">
                            <img src="${element[4]}" class="img-fluid" alt="">
                        </div>
                        <div class="font-img-down d-none d-sm-block">
                            <button class="btn btn-primary mr-2 fontstar" id="fontcollect" data-font-id="${element[0]}"><span class="collect-font">\uf005</span>收藏</button>
                            <button class="btn btn-success fontdownload" id="fontdownload">下载</button>
                            <div class="text-dark d-flex justify-content-end pt-3">
                                <span class="font-img-viewnum">共${element[7]}次浏览</span>
                            </div>
                        </div>
                    </div>
                </div>
            `)
        }
        if (element[8] == 1) {
            let select = '[data-font-id-name="' + element[0] + '"]'
            $(select).append(`<span class="badge bg-success d-flex align-items-center ml-3">商用免费</span>`)
        } else if (element[8] == -1) {
            let select = '[data-font-id-name="' + element[0] + '"]'
            $(select).append(`<span class="badge bg-danger d-flex align-items-center ml-3">付费</span>`)
        }
        for (let j = 0; j < userCollect.length; j++) {
            if (userCollect[j][2] == element[0]) {
                let select = '[data-font-id="' + element[0] + '"]'
                $(select).find('span').css('font-weight', '600')
            }
        }
    }
    // console.log(userCollect)
    $('.font-img-down').on('click', 'button', function () {
        let clickedId = $(this).attr("id")
        let fontId = $(this).closest('.fontdata-border-box').data("font-number")
        // console.log(fontId)
        if (clickedId == 'fontdownload') {
            getDownloadUrl(fontId)
        } else if (clickedId == 'fontcollect') {
            fontCollect(fontId)
        }
    })
    $('.font-img').click(function () {
        let fontid = $(this).closest('.fontdata-border-box').data("font-number")
        for (let i = 0; i < currentFonts.length; i++) {
            if (currentFonts[i][2] == fontid) {
                $('#fontinfoimg').prop('src', currentFonts[i][4])
                let mapsrc = currentFonts[i][4].replace(/cover/g, "charmap")
                $('#fontinfoimgcharmap').prop('src', mapsrc)
                fontPreviewNum = currentFonts[i][5]
                if (currentFonts[i][6] == 0) {
                    $('#fontyesdownload').prop('disabled', true)
                } else {
                    $('#fontyesdownload').prop('disabled', false)
                }
                $('#fontinfocollect').text('收藏')
                for (let j = 0; j < userCollect.length; j++) {
                    if (userCollect[j][2] == currentFonts[i][0]) {
                        $('#fontinfocollect').text('已收藏')
                        break
                    }
                }
                break
            }
        }
        $('#fontinfobtn').click()
        let msg = getSentence()
        $('#clickpreviewinput').val(msg)
        $('#clickpreview').click()
        $('#fontyesdownload').off('click')
        $('#fontyesdownload').click(function () {
            getAndDownloadUrl(fontid)
            $(this).prop('disabled', true)
            $(this).find('.spinner-border').removeClass('d-none')
            setTimeout(function () {
                $('#fontyesdownload').prop('disabled', false)
                $('#fontyesdownload').find('.spinner-border').addClass('d-none')
            }, 3000)
        })
        $('#fontinfocollect').off('click')
        $('#fontinfocollect').click(function () {
            fontCollect(fontid)
            $(this).prop('disabled', true)
            $(this).find('.spinner-border2').removeClass('d-none')
            setTimeout(function () {
                $('#fontinfocollect').prop('disabled', false)
                $('#fontinfocollect').find('.spinner-border2').addClass('d-none')
            }, 1000)
        })
    })
}
// 点击获取预览效果
$('#clickpreview').click(function () {
    let text = $('#clickpreviewinput').val()
    let src = `https://previewer.fonts.net.cn/canvas.php?font=${fontPreviewNum}&text=${text}`
    $('#fontinfoimgpreview').prop('src', src)
})
// 点击切换显示所有或免费
$('.nav-tabs').on('click', 'button', function () {
    let clickedId = $(this).attr("id")
    if (clickedId == 'nav-home-tab') {
        if (fontFree != 0) {
            location.href = `#/${currentRoute}/1`
            $('.font-home-hot-title').text(getCurrentTypeName())
            fontFree = 0
            setFreeBtn()
            getFontNum()
            // console.log(fontFree)
            setShowPage()
            setFontNum()
        }
    } else if (clickedId == 'nav-profile-tab') {
        if (fontFree != 1) {
            location.href = `#/${currentRoute}/1/free`
            $('.font-home-hot-title').text(getCurrentTypeName() + ' > 商用免费')
            fontFree = 1
            setFreeBtn()
            getFontNum()
            // console.log(fontFree)
            setShowPage()
            setFontNum()
        }
    }
})

function getCurrentTypeName() {
    if (currentRoute == 'home') {
        return '热门字体'
    } else if (currentRoute == 'zh') {
        return '中文字体'
    } else if (currentRoute == 'en') {
        return '英文字体'
    } else if (currentRoute == 'pic') {
        return '图形字体'
    } else if (currentRoute == 'search') {
        return '搜索字体'
    }
}

// 设置商用免费和所有字体按钮选择样式
function setFreeBtn() {
    if (fontFree == 0) {
        $('.nav-all').addClass('active')
        $('.nav-free').removeClass('active')
    } else if (fontFree == 1) {
        $('.nav-all').removeClass('active')
        $('.nav-free').addClass('active')
    }
}
// 设置顶部的字体数量
function setFontNum() {
    if (currentRoute == 'home') {
        $('.font-num').text(fontNum[3])
    } else if (currentRoute == 'zh') {
        $('.font-num').text(fontNum[0])
    } else if (currentRoute == 'en') {
        $('.font-num').text(fontNum[1])
    } else if (currentRoute == 'pic') {
        $('.font-num').text(fontNum[2])
    } else if (currentRoute == 'like') {
        $('.font-num').text(fontNum[4])
    } else if (currentRoute == 'search') {
        $('.font-num').text(searchFontNum)
    }
}
// 跳转首页页面执行
const homePage = (route) => {
    page = parseInt(router.routeList.home.args[0])
    if (Number.isInteger(page) && page > 0 && page < getMaxPage() + 1) {
        currentPage = page
    } else {
        currentPage = 1
    }
    // console.log('当前第', currentPage, '页')
    getFonts()
    setShowPage()
    setFontNum()
    if (fontFree == 0) {
        $('.font-home-hot-title').text(getCurrentTypeName())
    } else {
        $('.font-home-hot-title').text(getCurrentTypeName() + ' > 商用免费')
    }
    $('#link-home').addClass('current')
    $('#link-zh').removeClass('current')
    $('#link-en').removeClass('current')
    $('#link-pic').removeClass('current')
}
// 跳转中文页面执行
const zhPage = (route) => {
    page = parseInt(router.routeList.zh.args[0])
    if (Number.isInteger(page) && page > 0 && page < getMaxPage() + 1) {
        currentPage = page
    } else {
        currentPage = 1
    }
    // console.log('当前第', currentPage, '页')
    getFonts()
    setShowPage()
    setFontNum()
    if (fontFree == 0) {
        $('.font-home-hot-title').text(getCurrentTypeName())
    } else {
        $('.font-home-hot-title').text(getCurrentTypeName() + ' > 商用免费')
    }
    $('#link-home').removeClass('current')
    $('#link-zh').addClass('current')
    $('#link-en').removeClass('current')
    $('#link-pic').removeClass('current')
}
// 跳转英文页面执行
const enPage = (route) => {
    page = parseInt(router.routeList.en.args[0])
    if (Number.isInteger(page) && page > 0 && page < getMaxPage() + 1) {
        currentPage = page
    } else {
        currentPage = 1
    }
    // console.log('当前第', currentPage, '页')
    getFonts()
    setShowPage()
    setFontNum()
    if (fontFree == 0) {
        $('.font-home-hot-title').text(getCurrentTypeName())
    } else {
        $('.font-home-hot-title').text(getCurrentTypeName() + ' > 商用免费')
    }
    $('#link-home').removeClass('current')
    $('#link-zh').removeClass('current')
    $('#link-en').addClass('current')
    $('#link-pic').removeClass('current')
}
// 跳转图形页面执行
const picPage = (route) => {
    page = parseInt(router.routeList.pic.args[0])
    if (Number.isInteger(page) && page > 0 && page < getMaxPage() + 1) {
        currentPage = page
    } else {
        currentPage = 1
    }
    // console.log('当前第', currentPage, '页')
    getFonts()
    setShowPage()
    setFontNum()
    if (fontFree == 0) {
        $('.font-home-hot-title').text(getCurrentTypeName())
    } else {
        $('.font-home-hot-title').text(getCurrentTypeName() + ' > 商用免费')
    }
    $('#link-home').removeClass('current')
    $('#link-zh').removeClass('current')
    $('#link-en').removeClass('current')
    $('#link-pic').addClass('current')
}
// 跳转收藏页面执行
const likePage = (route) => {
    checkCookie()
    if (!userLogin) {
        alert('请先登录')
        location.href = '#/home'
    } else {
        getFontNum()
        page = parseInt(router.routeList.like.args[0])
        if (Number.isInteger(page) && page > 0 && page < getMaxPage() + 1) {
            currentPage = page
        } else {
            currentPage = 1
        }
        if (getMaxPage() > 1) {
            $('#collect-page-box').css('visibility', 'visible')
        } else {
            $('#collect-page-box').css('visibility', 'hidden')
        }
        console.log(fontNum[4])
        // console.log('当前第', currentPage, '页')
        getFonts()
        setShowPage()
        setFontNum()
        if (fontNum[4] == 0) {
            $('#font-box-like').append(`
                <div class="col-sm-12 p-3 my-2 rounded bg-white text-dark d-flex justify-content-center">
                    <img src="https://static.fonts.net.cn/3.1.0.23051202/assets/images/empty.png"></img>
                </div>
                <a class="btn btn-outline-primary my-3" href="#/home">返回首页</a>
            `)
        }
    }
}
// 跳转搜索页面执行
const searchPage = (route) => {
    if (searchKey == '') {
        location.href = '#/home'
    }
    if (fontFree == 0) {
        $('.font-home-hot-title').text(getCurrentTypeName() + ' > ' + searchKey)
    } else {
        $('.font-home-hot-title').text(getCurrentTypeName() + ' > 商用免费' + ' > ' + searchKey)
    }
    $('#link-home').removeClass('current')
    $('#link-zh').removeClass('current')
    $('#link-en').removeClass('current')
    $('#link-pic').removeClass('current')
    let toSend = {
        page: currentPage,
        num: perPageNum,
        key: searchKey,
        free: fontFree
    }
    $.ajax({
        url: '/search',
        type: 'POST',
        data: JSON.stringify(toSend),
        contentType: 'application/json',
        success: function (response) {
            if (response.success) {
                currentFonts = response.data
                searchFontNum = response.fontnum
                setFonts()
                setFontNum()
                setShowPage()
                if (getMaxPage() > 1) {
                    $('#search-page-box').css('visibility', 'visible')
                } else {
                    $('#search-page-box').css('visibility', 'hidden')
                }
                if (searchFontNum == 0) {
                    $('#font-box-search').append(`
                        <div class="col-sm-12 p-3 my-2 rounded bg-white text-dark d-flex justify-content-center">
                            <img src="https://static.fonts.net.cn/3.1.0.23051202/assets/images/empty.png"></img>
                        </div>
                        <a class="btn btn-outline-primary my-3" href="#/home">返回首页</a>
                    `)
                }
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}
// 检测登陆状态
function checkCookie() {
    $.ajax({
        url: '/userCheckCookie',
        type: 'POST',
        contentType: 'application/json',
        async: false,
        success: function (response) {
            userLogin = response.success
        },
        error: function (error) {
            console.log(error)
        }
    })
}

// 定义路由
router.set(['login', 'register'], whiteBg)
router.set('home', [smokeBg, homePage])
router.set('zh', [smokeBg, zhPage])
router.set('en', [smokeBg, enPage])
router.set('pic', [smokeBg, picPage])
router.set('like', [smokeBg, likePage])
router.set('search', [smokeBg, searchPage])

$('#font-btn-search').click(function () {
    if ($('#font-input-search').val() != '') {
        searchKey = $('#font-input-search').val()
        $('#font-input-search').val('')
        location.href = '#/search'
    }
})

// 上一页按钮
$('.prve-page').click(function () {
    if (currentPage > 1) {
        currentPage = currentPage - 1
        if (fontFree == 1) {
            location.href = '#/' + router.getNowRouteName() + '/' + currentPage + '/free'
        } else {
            location.href = '#/' + router.getNowRouteName() + '/' + currentPage
        }
    }
})
// 下一页按钮
$('.next-page').click(function () {
    if (currentPage < getMaxPage()) {
        currentPage = currentPage + 1
        if (fontFree == 1) {
            location.href = '#/' + router.getNowRouteName() + '/' + currentPage + '/free'
        } else {
            location.href = '#/' + router.getNowRouteName() + '/' + currentPage
        }
    }
})

// 密码框小眼睛切换
const passwords = document.querySelectorAll('.passwordBox')
const logoButtons = document.querySelectorAll('.logoButton')
for (let i = 0; i < logoButtons.length; i++) {
    logoButtons[i].onclick = function () {
        if (passwords[i].type === 'password') {
            passwords[i].setAttribute('type', 'text')
            logoButtons[i].classList.add('hide')
        }
        else {
            passwords[i].setAttribute('type', 'password')
            logoButtons[i].classList.remove('hide')
        }
    }
}

const msg = document.getElementsByClassName("msg")[0]
const from = document.getElementsByClassName("from")[0]
// 获取每日一言
const xhr = new XMLHttpRequest()
xhr.open('POST', 'https://v1.hitokoto.cn/', false)
xhr.send()
const resData = JSON.parse(xhr.responseText)
let datamsg = resData.hitokoto
let datafrom = '—— 「 ' + resData.from + ' 」'
// 修改每日一言内容
msg.textContent = datamsg
from.textContent = datafrom

// 判断注册框内容合法性
const userLengthCase = document.getElementById('nameLength')
const lengthCase = document.getElementById('length')
const recheckCase = document.getElementById('recheck')
const rbtn = document.getElementById('registerbtn')
let pwd
let rpwd
let username
let userNameOK, checkPasswordOK, recheckPasswordOK = 0

// 判断输入是否都正确
function inputOK(userNameOK, checkPasswordOK, recheckPasswordOK) {
    let a = userNameOK
    let b = checkPasswordOK
    let c = recheckPasswordOK
    if (a == 1 && b == 1 && c == 1) {
        rbtn.disabled = false;
        rbtn.classList.remove('default')
        rbtn.classList.add('sbtn')
    } else {
        rbtn.disabled = true;
        rbtn.classList.remove('sbtn')
        rbtn.classList.add('default')
    }
}
//用于检测输入是否有空白符
function hasWhiteSpace(str) {
    return /\s/g.test(str);
}
// 检测用户名是否合法
function userName(data) {
    username = data
    //用于判断用户名长度是否在1-12字符之间
    const length = new RegExp('(^.{1,12}$)')

    if (length.test(data) && !hasWhiteSpace(data)) {
        userLengthCase.classList.add('valid')
        userNameOK = 1;
    }
    else {
        userLengthCase.classList.remove('valid')
        userNameOK = 0;
    }

    inputOK(userNameOK, checkPasswordOK, recheckPasswordOK)
}
// 检测密码是否合法
function checkPassword(data) {
    pwd = data

    const length = new RegExp('(?=.{6,})')

    if (length.test(data) && !hasWhiteSpace(data)) {
        lengthCase.classList.add('valid')
        checkPasswordOK = 1;
    }
    else {
        lengthCase.classList.remove('valid')
        checkPasswordOK = 0;
    }

    recheckPassword(rpwd)

    inputOK(userNameOK, checkPasswordOK, recheckPasswordOK)
}
// 检测两次输入密码是否相同
function recheckPassword(data) {
    rpwd = data

    if (data === '') {
        recheckCase.classList.remove('valid')
    }
    else if (data === pwd) {
        recheckCase.classList.add('valid')
        recheckPasswordOK = 1;
    }
    else {
        recheckCase.classList.remove('valid')
        recheckPasswordOK = 0;
    }

    inputOK(userNameOK, checkPasswordOK, recheckPasswordOK)
}
// 清除cookie
function clearCookie() {
    $.ajax({
        url: '/clearCookie',
        type: 'POST',
        contentType: 'application/json',
        success: function (response) {
            setUserFont()
        },
        error: function (error) {
            console.log(error)
            alert('服务器开小差了\n请稍后再试')
        }
    })
}
// 登录功能
$('#loginbtn').click(function () {
    let username = $('#usernameInput').val() // 获取用户名输入框的内容
    let password = $('#passwordInput').val() // 获取密码输入框的内容
    // console.log('Username:', username)
    // console.log('Password:', password)
    let toSend = {
        username: username,
        password: password,
    }
    if (username && password) {
        $.ajax({
            url: '/login',
            type: 'POST',
            data: JSON.stringify(toSend),
            contentType: 'application/json',
            success: function (response) {
                //  console.log(response)
                if (response.success == true) {
                    // console.log('登陆成功')
                    alert(response.message)
                    location.href = '#/home'
                    setUserFont()
                } else {
                    // console.log('登陆失败')
                    alert(response.message)
                }
            },
            error: function (error) {
                console.log(error)
                alert('服务器开小差了\n请稍后再试')
            }
        })
    }
})
// 注册功能
$('#registerbtn').click(function () {
    let username = $('#rusernameInput').val() // 获取用户名输入框的内容
    let password = $('#rpasswordInput').val() // 获取密码输入框的内容
    let toSend = {
        username: username,
        password: password,
    }
    if (username && password) {
        $.ajax({
            url: '/register',
            type: 'POST',
            data: JSON.stringify(toSend),
            contentType: 'application/json',
            success: function (response) {
                //  console.log(response)
                if (response.success == true) {
                    alert(response.message)
                    location.href = '#/login'
                } else {
                    alert(response.message)
                }
            },
            error: function (error) {
                console.log(error)
                alert('服务器开小差了\n请稍后再试')
            }
        })
    }
})

let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

$('.dropdown').hover(
    function () {
        $(this).addClass('show')
        $(this).find('.dropdown-menu').addClass('show')
    },
    function () {
        $(this).removeClass('show')
        $(this).find('.dropdown-menu').removeClass('show')
    }
)

router.start()