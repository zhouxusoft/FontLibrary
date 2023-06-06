const router = new ApeeRouter()
// 设置背景色
const whiteBg = (route) => {
    document.body.style.backgroundColor = 'white'
}
// 设置背景色
const smokeBg = (route) => {
    document.body.style.backgroundColor = 'whitesmoke'
}

// 定义路由
router.set(['login', 'register'], whiteBg)
router.set(['home', 'zh', 'en', 'pic'], smokeBg)

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
                } else {
                    alert(response.message)
                }
            },
            error: function (error) {
                console.log(error)
            }
        })
    }
})

router.start()