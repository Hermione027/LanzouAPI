# LanzouAPI

## 项目简介
蓝奏云外链解析API服务，支持解析蓝奏云文件分享链接，生成直链或直接下载。提供Python和PHP两种实现版本。

## 主要特性
- 支持检测文件是否被取消
- 支持带密码的文件分享链接（但不支持分享的文件夹）
- 支持生成直链或直接下载
- 增加iOS应用在线安装
- 解析最终直链
- 自动识别旧版链接替换为新版并解析
- 提供Python和PHP双版本实现

## 快速开始

### 环境要求
- **Python版本**: Python 3.6+
- **PHP版本**: PHP 7.0+

### 安装步骤
```bash
git clone https://github.com/yourusername/LanzouAPI.git
cd LanzouAPI
```

### 启动服务
#### Python版本
```bash
python app.py
```

#### PHP版本
```bash
php -S localhost:8000
```

服务默认运行在 `http://localhost:8000`

## API 接口

### 认证
无需认证，直接调用API

### 直接下载文件
```http
GET /?url={蓝奏云链接}&type=down&pwd={密码}
```

参数：
- `url`: 蓝奏云文件分享链接（必填）
- `type`: 固定值 `down`（必填）
- `pwd`: 文件提取密码（可选）

示例：
```
http://localhost:8000/?url=https://www.lanzouq.com/iGNHA6th9cd&type=down
```

### 获取直链
```http
GET /?url={蓝奏云链接}&pwd={密码}
```

参数：
- `url`: 蓝奏云文件分享链接（必填）
- `pwd`: 文件提取密码（可选）

示例：
```
http://localhost:8000/?url=https://www.lanzous.com/i42Xxebssfg&pwd=1234
```

## 配置说明
无需额外配置，开箱即用

## 项目结构
```
LanzouAPI/
├── app.py                # Python版本主服务文件
├── index.php             # PHP版本主服务文件
├── LICENSE               # 许可证文件
├── README.md             # 项目文档
```

## 常见问题
### Q: 如何选择Python还是PHP版本？
A: 
- Python版本适合需要扩展功能的场景
- PHP版本部署更简单，适合基础需求

### Q: PHP版本需要额外配置吗？
A: 标准PHP环境即可运行，无需特殊配置

### Q: 如何获取蓝奏云文件链接？
A: 在蓝奏云网页版选择"分享文件"，获取分享链接

### Q: 支持文件夹分享链接吗？
A: 暂不支持文件夹分享链接，仅支持单个文件链接

## 许可证
本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 贡献
欢迎提交 Issue 和 Pull Request 改进项目

> **免责声明**  
> 因调用量过大导致服务器IP被屏蔽，今后不再提供示例站点，请自行搭建服务  
> 本项目仅供学习交流，不保证稳定性，作者保留停更或删除项目的权利
