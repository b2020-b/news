# 



# 新闻管理系统说明文档

## 一、系统概述

本新闻管理系统基于 Python 的 Flask 框架、PyMySQL 数据库操作库以及 Vue 3 前端框架构建，实现了新闻的发布、编辑、分类、归档、删除等核心功能，同时支持对新闻内容的附件、图片等资料的管理，还具备分词、检索、推荐等操作。

## 二、系统架构

### 后端

- **Flask 框架**：作为 Web 服务器，处理前端的请求并返回相应的数据。
- **PyMySQL**：用于与 MySQL 数据库进行交互，执行数据库的增删改查操作。
- **Jieba**：用于对新闻内容进行分词，实现关键词检索功能。

### 前端

- **Vue 3**：构建用户界面，实现与用户的交互和数据展示。
- **Element Plus**：提供丰富的UI组件库
- **Axios**：用于与后端 API 进行数据交互。

## 三、数据库设计

### 分类表 (categories)

| 字段名 | 类型         | 描述              |
| ------ | ------------ | ----------------- |
| id     | INT          | 分类 ID，自增主键 |
| name   | VARCHAR(255) | 分类名称          |

### 新闻表 (news)

| 字段名       | 类型         | 描述                            |
| ------------ | ------------ | ------------------------------- |
| id           | INT          | 新闻 ID，自增主键               |
| title        | VARCHAR(255) | 新闻标题                        |
| content      | TEXT         | 新闻内容                        |
| category_id  | INT          | 分类 ID，外键关联 categories 表 |
| published_at | TIMESTAMP    | 发布时间，默认当前时间          |
| archived     | BOOLEAN      | 是否归档，默认 false            |

### 附件表 (attachments)

| 字段名    | 类型         | 描述                      |
| --------- | ------------ | ------------------------- |
| id        | INT          | 附件 ID，自增主键         |
| news_id   | INT          | 新闻 ID，外键关联 news 表 |
| file_name | VARCHAR(255) | 文件名                    |
| file_path | VARCHAR(255) | 文件路径                  |

## 四、后端 API 接口（更新）

### 1. 发布新闻

- **URL**：`/news`
- **方法**：`POST`
- **请求参数**：
  - `title`：新闻标题
  - `content`：新闻内容
  - `category_id`：分类 ID
- **响应**：返回新闻 ID

### 2. 编辑新闻

- **URL**：`/news/<int:news_id>`
- **方法**：`PUT`
- **请求参数**：
  - `title`：新闻标题
  - `content`：新闻内容
  - `category_id`：分类 ID
- **响应**：返回成功消息

### 3. 删除新闻

- **URL**：`/news/<int:news_id>`
- **方法**：`DELETE`
- **响应**：返回成功消息

### 4. 获取新闻列表

- **URL**：`/news`
- **方法**：`GET`
- **请求参数**：
  - `keyword`：关键词，用于检索新闻
  - `category_id`：分类 ID，用于筛选特定分类的新闻
- **响应**：返回新闻列表

## 五、前端功能（补充）

### 5. 分类管理

- 自动拉取分类数据并显示在下拉选择器中
- 新建新闻时支持分类选择
- 分类列表实时同步更新

### 6. 新闻状态管理

- 支持新闻发布/归档状态切换
- 状态变更实时反映在标签显示上
- 提供状态过滤功能（示例代码见NewsManagement.vue）

### 1. 发布新闻

- 点击“发布新闻”按钮，弹出发布表单。
- 输入新闻标题、内容和选择分类。
- 点击“发布”按钮，将新闻信息发送到后端。

### 2. 编辑新闻

- 点击新闻列表中的“编辑”按钮，可对新闻进行编辑。
- 编辑完成后，点击保存按钮，将更新后的新闻信息发送到后端。

### 3. 删除新闻

- 点击新闻列表中的“删除”按钮，将新闻信息从数据库中删除。

### 4. 检索新闻

- 在搜索框中输入关键词，可对新闻进行检索。

## 六、部署步骤

### 后端

1. 安装所需的 Python 库：

```bash
pip install flask pymysql jieba
```

2. 创建 MySQL 数据库，并执行数据库表创建语句。
3. 启动后端服务器：

```bash
python  app.py
```

### 前端

1. 创建 Vue 3 项目：

```bash
npm init vite@latest news-management-system -- --template vue
cd news-management-system
npm install
```

2. 安装 Axios：

```bash
npm install axios
```

3. 启动前端开发服务器：

```bash
cd .\frontend\
npm run dev
```

