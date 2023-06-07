const router = new ApeeRouter()

// 获得当前页面的路由
let currentRoute = ''
// 设置当前的页码
let currentPage = 1
// 存储当前页的字体
let currentFonts = []

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
}

function getMaxPage() {
    if (currentRoute == 'home') {
        return 8
    } else if (currentRoute == 'zh') {
        return 387
    } else if (currentRoute == 'en') {
        return 1575
    } else if (currentRoute == 'pic') {
        return 156
    }
}

function getFonts() {
    let toSend = {
        page: currentPage,
        type: currentRoute
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

function setShowPage() {
    $('.all-page').text(getMaxPage())
    $('.current-page').text(currentPage)
}

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
                console.log(response.data)
            } else {
                alert('服务器开小差了\n请稍后再试')
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}

function fontCollect(fontid) {
    
}

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
        if (element[6] == 0) {
            $(select).append(`
                <div class="col-sm-12 p-3 my-2 rounded bg-white text-white fontdata-border-box" data-font-number="${element[2]}">
                    <div class="text-dark d-flex align-items-center justify-content-between">
                        <span class="font-top-name">${element[1]}</span>
                        <span class="font-top-type">${element[3]}</span>
                    </div>
                    <div class="hr-i"></div>
                    <div class="font-img-box d-flex align-items-center justify-content-between">
                        <div class="font-img">
                            <img src="${element[4]}" class="img-fluid" alt="">
                        </div>
                        <div class="font-img-down d-none d-sm-block">
                            <button class="btn btn-primary mr-2 fontstar" id="fontcollect"><span class="collect-font">\uf005</span>收藏</button>
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
                        <span class="font-top-name">${element[1]}</span>
                        <span class="font-top-type">${element[3]}</span>
                    </div>
                    <div class="hr-i"></div>
                    <div class="font-img-box d-flex align-items-center justify-content-between">
                        <div class="font-img">
                            <img src="${element[4]}" class="img-fluid" alt="">
                        </div>
                        <div class="font-img-down d-none d-sm-block">
                            <button class="btn btn-primary mr-2 fontstar" id="fontcollect"><span class="collect-font">\uf005</span>收藏</button>
                            <button class="btn btn-success fontdownload" id="fontdownload">下载</button>
                            <div class="text-dark d-flex justify-content-end pt-3">
                                <span class="font-img-viewnum">共${element[7]}次浏览</span>
                            </div>
                        </div>
                    </div>
                </div>
            `)           
        }   
    }
    $('.font-img-down').on('click', 'button', function () {
        let clickedId = $(this).attr("id")
        let fontId = $(this).closest('.fontdata-border-box').data("font-number")
        console.log(fontId)
        if (clickedId == 'fontdownload') {
            getDownloadUrl(fontId)
        }
    })
    
}

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
}

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
}

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
}

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
}

// 定义路由
router.set(['login', 'register'], whiteBg)
router.set('home', [smokeBg, homePage])
router.set('zh', [smokeBg, zhPage])
router.set('en', [smokeBg, enPage])
router.set('pic', [smokeBg, picPage])

$('.prve-page').click(function () {
    if (currentPage > 1) { 
        currentPage = currentPage - 1
        location.href = '#/' + router.getNowRouteName() + '/' + currentPage
    }
})

$('.next-page').click(function () {
    if (currentPage < getMaxPage() ) {
        currentPage = currentPage + 1
        location.href = '#/' + router.getNowRouteName() + '/' + currentPage
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
                } else {
                    // console.log('登陆失败')
                    alert(response.message)
                }
            },
            error: function (error) {
                console.log(error)
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
                    alert('服务器开小差了\n请稍后再试')
                }
            },
            error: function (error) {
                console.log(error)
            }
        })
    }
})



router.start()