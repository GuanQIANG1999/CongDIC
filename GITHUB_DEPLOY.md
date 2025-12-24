# 🚀 使用 GitHub 部署指南

GitHub 本身不能直接运行 Flask 应用，但我们可以用 GitHub 作为代码仓库，配合其他平台自动部署。

## 📋 方案概览

1. **GitHub + Render**（推荐，最简单）
2. **GitHub + PythonAnywhere**
3. **GitHub + Vercel**（需要调整，不太推荐）
4. **GitHub Actions + 自建服务器**

---

## 方案一：GitHub + Render（最推荐）

这是最简单的方法，完全免费，支持自动部署。

### 步骤：

1. **在 GitHub 创建仓库**
   ```bash
   cd /Users/qiangguan/Desktop/Dictionary
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **在 GitHub 网站创建新仓库**
   - 访问 https://github.com/new
   - 仓库名：`congcong-dictionary`（或你喜欢的名字）
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
   - 点击 "Create repository"

3. **推送代码到 GitHub**
   ```bash
   git remote add origin https://github.com/你的用户名/congcong-dictionary.git
   git branch -M main
   git push -u origin main
   ```

4. **在 Render 部署**
   - 访问 https://render.com
   - 使用 GitHub 账号登录
   - 点击 "New +" → "Web Service"
   - 点击 "Connect GitHub"
   - 选择你的仓库 `congcong-dictionary`
   - 设置：
     - **Name**: `congcong-dictionary`
     - **Region**: 选择离你最近的（如 Singapore）
     - **Branch**: `main`
     - **Root Directory**: 留空
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   - 点击 "Create Web Service"

5. **等待部署**
   - Render 会自动从 GitHub 拉取代码
   - 自动安装依赖
   - 自动启动应用
   - 完成后会给你一个 URL

6. **自动部署**
   - 以后每次你 `git push` 代码到 GitHub
   - Render 会自动重新部署应用
   - 无需手动操作！

### 优点：
- ✅ 完全免费
- ✅ 自动部署（代码推送后自动更新）
- ✅ 支持 HTTPS
- ✅ 操作简单

---

## 方案二：GitHub + PythonAnywhere

PythonAnywhere 也支持从 GitHub 自动拉取代码。

### 步骤：

1. **推送代码到 GitHub**（同上）

2. **在 PythonAnywhere 设置**
   - 登录 https://www.pythonanywhere.com
   - 点击 "Web" 标签
   - 点击 "Add a new web app"
   - 选择 Flask 和 Python 版本

3. **配置 GitHub 集成**
   - 在 Web 配置页面
   - 找到 "Source code" 部分
   - 选择 "GitHub"
   - 输入你的仓库地址
   - 设置分支为 `main`

4. **设置自动重载**
   - 每次 GitHub 更新后
   - 在 Web 页面点击 "Reload" 按钮

---

## 方案三：GitHub Actions + 自建服务器

如果你有自己的服务器，可以用 GitHub Actions 自动部署。

### 创建 GitHub Actions 工作流

在项目根目录创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to Server

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/Dictionary
            git pull origin main
            pip3 install -r requirements.txt
            sudo systemctl restart dictionary
```

然后在 GitHub 仓库设置中添加 Secrets：
- `HOST`: 你的服务器 IP
- `USERNAME`: SSH 用户名
- `SSH_KEY`: SSH 私钥

---

## 🎯 推荐流程

**最简单的方式**：

1. ✅ 代码推送到 GitHub（作为代码仓库）
2. ✅ 使用 Render 连接 GitHub 自动部署
3. ✅ 以后每次更新代码，只需 `git push`，Render 自动部署

---

## 📝 日常使用流程

部署完成后，以后更新应用只需要：

```bash
# 1. 修改代码
# 2. 提交更改
git add .
git commit -m "更新说明"
git push origin main

# 3. Render 会自动检测并重新部署
# 4. 等待几分钟，访问网站即可看到更新
```

---

## ❓ 常见问题

**Q: GitHub 可以免费使用吗？**
A: 可以，GitHub 对公开仓库完全免费，私有仓库也有限额免费。

**Q: 必须用 GitHub 吗？**
A: 不是必须的，但用 GitHub 配合 Render 是最简单的部署方式。

**Q: 代码会公开吗？**
A: 如果你选择 Public 仓库，代码会公开。选择 Private 仓库，代码就是私有的。

**Q: 如何保护敏感信息？**
A: 使用环境变量或 GitHub Secrets，不要将密码等敏感信息直接写在代码里。

---

## 🚀 快速开始

如果你还没有 GitHub 账号：
1. 访问 https://github.com 注册
2. 按照上面的"方案一"步骤操作
3. 几分钟就能上线！

祝部署顺利！🎉

