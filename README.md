# 📚 聪聪思培单词卡

一个专为学习设计的在线单词卡应用，支持添加单词、单词卡复习，界面可爱美观。

## ✨ 功能特点

- 🔐 密码登录保护
- ➕ 添加单词（单词、释义、例句）
- 🃏 单词卡翻转复习
- 📊 学习统计（总单词数、已掌握、待复习）
- 🎨 可爱美观的界面设计
- 📱 响应式设计，支持手机和电脑

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

应用会在 `http://localhost:5000` 启动

### 3. 登录

默认账号：
- 用户名：`admin`
- 密码：`admin123`

**⚠️ 重要：首次使用后请修改默认密码！**

## 📦 部署上线

**详细部署指南请查看 [DEPLOY.md](DEPLOY.md)**

### 方法一：使用 Render（推荐，最简单免费）

1. **注册 Render 账号**
   - 访问 https://render.com
   - 使用 GitHub 账号登录

2. **准备 Git 仓库并推送代码到 GitHub**

3. **在 Render 创建 Web Service**
   - 连接 GitHub 仓库
   - 设置 Build Command: `pip install -r requirements.txt`
   - 设置 Start Command: `gunicorn app:app`

4. **等待部署完成，访问提供的 URL**

详细步骤请查看 [DEPLOY.md](DEPLOY.md)

### 方法二：使用 PythonAnywhere（免费）

1. **注册账号**
   - 访问 https://www.pythonanywhere.com
   - 注册免费账号

2. **上传文件**
   - 在 Files 页面，上传所有项目文件

3. **创建 Web App**
   - 在 Web 页面，点击 "Add a new web app"
   - 选择 Flask，Python 3.10
   - 设置 Source code 路径为 `/home/yourusername/Dictionary`
   - 设置 WSGI configuration file，修改为：
     ```python
     import sys
     path = '/home/yourusername/Dictionary'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```

4. **安装依赖**
   - 在 Bash 控制台运行：
     ```bash
     pip3.10 install --user -r requirements.txt
     ```

5. **访问应用**
   - 在 Web 页面点击 "Reload" 按钮
   - 访问你的应用 URL

### 方法三：使用 VPS（如阿里云、腾讯云）

1. **连接服务器**
   ```bash
   ssh user@your-server-ip
   ```

2. **安装 Python 和依赖**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install -r requirements.txt
   pip3 install gunicorn
   ```

3. **上传项目文件**
   使用 scp 或 git 上传项目到服务器

4. **使用 Gunicorn 运行**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

5. **使用 Nginx 反向代理（可选）**
   配置 Nginx 将请求转发到 Gunicorn

6. **使用 systemd 管理服务（可选）**
   创建 systemd service 文件实现开机自启

## 🔒 修改默认密码

在 `app.py` 中，找到初始化数据库的部分，修改密码：

```python
default_user = User(
    username='admin',
    password_hash=bcrypt.hashpw('你的新密码'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
)
```

或者运行后通过代码修改，或直接删除数据库文件 `dictionary.db` 重新初始化。

## 📁 项目结构

```
Dictionary/
├── app.py              # Flask 应用主文件
├── requirements.txt    # Python 依赖
├── dictionary.db       # SQLite 数据库（运行后自动生成）
├── templates/          # HTML 模板
│   ├── login.html     # 登录页面
│   └── index.html       # 主页面
└── README.md          # 说明文档
```

## 🎨 自定义

- **修改颜色主题**：在 `templates/index.html` 和 `templates/login.html` 的 `<style>` 标签中修改颜色值
- **修改默认用户**：在 `app.py` 的数据库初始化部分修改
- **添加更多功能**：在 `app.py` 中添加新的路由和功能

## ⚠️ 注意事项

1. 生产环境请修改 `SECRET_KEY` 为更安全的随机字符串
2. 建议使用环境变量存储敏感信息
3. 定期备份 `dictionary.db` 数据库文件
4. 如需多用户支持，需要修改代码添加用户注册功能

## 💝 使用提示

- 点击单词卡可以翻转查看释义
- 复习时可以标记"已掌握"或"还需努力"
- 已掌握的单词会显示 ✅ 标记
- 所有数据保存在本地数据库中

祝学习愉快！📚✨

