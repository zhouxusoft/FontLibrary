# Font Library
> 字体库爬虫展示项目

## 技术栈

- Python Flask
- MySQL
- BootStrap
  
## 开源依赖

- [Apee-Router](https://github.com/oyps/apee-router)

## 项目信息

- 作者：Godxu
- 博客：godxu.top
- 完成日期
    - 2023/6/12

## 开发环境

- Windows 10
- VS Code

## 使用说明

- 安装Flask: `pip install flask`
- 安装Pymysql: `pip install pymysql`
- 安装BCrypt: `pip install bcrypt`
- 修改getinfo/pp.py && getinfo/hot.py && app.py 中的数据库连接信息
- 运行getinfo/pp.py 爬取信息: `python getinfo/pp.py`
- 运行getinfo/hot.py 整理信息: `python getinfo/hot.py`
- 运行项目: `flask run`

## 项目文件结构

- getinfo: 数据爬取
- templates：前端 HTML 代码
- static：静态资源
- app.py: 项目运行文件
