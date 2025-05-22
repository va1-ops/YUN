# 自动化刷步数指南

## 功能介绍

本项目新增了以下功能：
1. 自动抓包功能：使用mitmproxy自动捕获并保存关键请求信息
2. 多用户支持：可同时为多个用户配置和运行刷步数任务
3. 定时执行：每天早上6点自动执行刷步数任务
4. Vercel部署支持：可部署到Vercel平台实现云端自动化

## 使用方法

### 1. 本地运行自动抓包

```bash
# 启动mitmproxy代理服务器
mitmdump -s auto_proxy.py

# 配置手机代理后，使用运动APP登录和运动，相关请求会被自动保存
```

### 2. 配置多用户

在项目根目录下创建`user_configs`文件夹，为每个用户创建独立的配置文件：

```ini
# user_configs/用户ID.ini
[User]
token = 你的token
device_id = 你的设备ID
device_name = 你的设备名称
sys_edition = 系统版本
```

### 3. Vercel部署

1. Fork本项目到你的GitHub账号
2. 在Vercel上导入该项目
3. 设置环境变量（如果需要）
4. 部署完成后，Vercel会自动创建一个域名

### 4. API接口

#### 添加新用户
```http
POST https://你的域名/api/run
Content-Type: application/json

{
    "user_id": "用户唯一标识",
    "token": "用户token",
    "device_id": "设备ID",
    "device_name": "设备名称",
    "sys_edition": "系统版本"
}
```

#### 手动触发运行
```http
GET https://你的域名/api/run
```

## 注意事项

1. 请确保你的配置文件中包含正确的用户信息
2. 建议在首次使用时先通过抓包工具获取正确的请求信息
3. 定时任务默认设置为每天早上6点执行，可以在`vercel.json`中修改
4. 请勿频繁触发API接口，以免影响服务稳定性

## 常见问题

1. 如何获取token和device_id？
   - 使用mitmproxy抓包工具，登录APP后自动保存相关信息

2. 定时任务没有执行？
   - 检查Vercel的部署日志
   - 确认配置文件格式正确
   - 验证cron表达式设置

3. 如何修改定时执行时间？
   - 修改`vercel.json`中的crons配置项
   - 格式为："0 6 * * *"（分 时 日 月 星期）

## 安全提醒

1. 请勿将你的个人token和设备信息分享给他人
2. 建议定期更换密码和token
3. 使用HTTPS协议访问API接口
4. 在生产环境中添加适当的访问控制和认证机制