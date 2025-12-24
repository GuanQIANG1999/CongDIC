# 🚀 上线部署指南

本指南将帮助你将"聪聪思培单词卡"应用部署到互联网上。

## 📋 部署前准备

1. **确保所有文件已保存**
2. **测试本地运行正常**
3. **准备好 Git**（如果使用 Git 部署）

---

## 方法一：使用 Render（推荐，最简单免费）

Render 是一个现代化的云平台，对 Flask 应用支持很好，完全免费。

### 步骤：

1. **注册账号**
   - 访问 https://render.com
   - 使用 GitHub 账号登录（如果没有，先注册 GitHub）

2. **准备 Git 仓库**
   ```bash
   # 在项目目录下
   git init
   git add .
   git commit -m "Initial commit"
   
   # 在 GitHub 创建新仓库，然后推送
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git branch -M main
   git push -u origin main
   ```

3. **在 Render 创建 Web Service**
   - 登录 Render，点击 "New +" → "Web Service"
   - 连接你的 GitHub 仓库
   - 设置：
     - **Name**: `congcong-dictionary`（或你喜欢的名字）
     - **Region**: 选择离你最近的区域
     - **Branch**: `main`
     - **Root Directory**: 留空
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   - 点击 "Create Web Service"

4. **等待部署完成**
   - Render 会自动构建和部署
   - 完成后会给你一个 URL，如：`https://congcong-dictionary.onrender.com`

5. **访问应用**
   - 使用 Render 提供的 URL 访问
   - 登录信息：
     - 用户名：`congcong`
     - 密码：`congcong1996`

**优点**：完全免费，自动部署，支持 HTTPS，操作简单

---

## 方法二：使用 PythonAnywhere（免费，适合初学者）

PythonAnywhere 专门为 Python 应用设计，有图形界面，操作简单。

### 步骤：

1. **注册账号**
   - 访问 https://www.pythonanywhere.com
   - 注册免费账号（免费版有使用限制，但足够个人使用）

2. **上传文件**
   - 登录后，点击 "Files" 标签
   - 在 `/home/你的用户名/` 下创建 `Dictionary` 文件夹
   - 上传所有项目文件（app.py, requirements.txt, templates 文件夹等）

3. **安装依赖**
   - 点击 "Consoles" → "Bash"
   - 运行：
     ```bash
     cd Dictionary
     pip3.10 install --user -r requirements.txt
     ```

4. **创建 Web App**
   - 点击 "Web" 标签
   - 点击 "Add a new web app"
   - 选择 "Flask"
   - 选择 Python 3.10
   - 设置路径为：`/home/你的用户名/Dictionary/app.py`

5. **配置 WSGI 文件**
   - 点击 WSGI configuration file 链接
   - 删除所有内容，替换为：
     ```python
     import sys
     path = '/home/你的用户名/Dictionary'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```

6. **配置静态文件（可选）**
   - 在 Web 标签的 "Static files" 部分
   - URL: `/static/`
   - Directory: `/home/你的用户名/Dictionary/static/`

7. **重新加载应用**
   - 点击绿色的 "Reload" 按钮
   - 访问你的应用 URL（格式：`你的用户名.pythonanywhere.com`）

**优点**：有图形界面，操作直观，适合初学者

---

## 方法三：使用 Heroku（经典选择）

Heroku 是老牌的云平台，但免费版已停止，需要付费。

### 步骤：

1. **安装 Heroku CLI**
   - macOS: `brew install heroku/brew/heroku`
   - 或访问 https://devcenter.heroku.com/articles/heroku-cli

2. **登录 Heroku**
   ```bash
   heroku login
   ```

3. **创建应用**
   ```bash
   cd /Users/qiangguan/Desktop/Dictionary
   heroku create 你的应用名
   ```

4. **部署**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **访问**
   ```bash
   heroku open
   ```

**注意**：Heroku 免费版已停止，现在需要付费使用。

---

## 方法四：使用 VPS 服务器（如阿里云、腾讯云）

如果你有自己的服务器，可以这样部署：

### 步骤：

1. **连接服务器**
   ```bash
   ssh root@你的服务器IP
   ```

2. **安装依赖**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **上传项目文件**
   ```bash
   # 使用 scp 上传
   scp -r /Users/qiangguan/Desktop/Dictionary root@你的服务器IP:/var/www/
   ```

4. **安装 Python 依赖**
   ```bash
   cd /var/www/Dictionary
   pip3 install -r requirements.txt
   pip3 install gunicorn
   ```

5. **使用 Gunicorn 运行**
   ```bash
   gunicorn -w 4 -b 127.0.0.1:5000 app:app
   ```

6. **配置 Nginx（可选）**
   创建 `/etc/nginx/sites-available/dictionary`：
   ```nginx
   server {
       listen 80;
       server_name 你的域名或IP;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   然后：
   ```bash
   sudo ln -s /etc/nginx/sites-available/dictionary /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. **使用 systemd 管理服务（可选）**
   创建 `/etc/systemd/system/dictionary.service`：
   ```ini
   [Unit]
   Description=Dictionary App
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/var/www/Dictionary
   ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   然后：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable dictionary
   sudo systemctl start dictionary
   ```

---

## 🔧 部署前检查清单

- [ ] 确保 `requirements.txt` 包含所有依赖
- [ ] 确保 `Procfile` 存在（如果使用 Heroku/Render）
- [ ] 检查 `app.py` 中的端口设置（生产环境建议使用环境变量）
- [ ] 确保数据库路径正确（SQLite 文件会保存在服务器上）
- [ ] 测试本地运行正常

---

## 🌐 部署后访问

部署成功后，使用以下信息登录：

- **用户名**: `congcong`
- **密码**: `congcong1996`

---

## 💡 推荐方案

- **最简单**：使用 Render（方法一）
- **最适合初学者**：使用 PythonAnywhere（方法二）
- **需要更多控制**：使用 VPS（方法四）

---

## ❓ 常见问题

**Q: 部署后数据库在哪里？**
A: SQLite 数据库文件会保存在服务器上，所有数据都会持久化保存。

**Q: 如何备份数据？**
A: 定期下载 `dictionary.db` 文件即可。

**Q: 可以修改登录信息吗？**
A: 可以，修改 `app.py` 中的默认用户信息，然后删除数据库文件重新初始化。

**Q: 如何更新应用？**
A: 修改代码后，重新部署即可（Git 推送会自动触发部署）。

---

祝部署顺利！🎉

