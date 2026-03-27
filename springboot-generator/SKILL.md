---
name: springboot-generator
description: 专门用于生成 Spring Boot 项目代码的助手。涵盖从需求分析到后端(Java 17+)+前端(Vue 3)的完整代码生成流程，强制执行安全规范与最佳实践。支持 Web(Vue 3 + Element Plus)和小程序(uni-app)两种前端方案。
---

# Spring Boot Generator Skill

此技能专注于快速、标准化地生成 Spring Boot 全栈项目代码。

## 核心能力

- **技术栈锁定**: JDK 17+, Spring Boot 3+, Vue 3.
- **前端方案 (自动检测)**:
  - **Web端 (默认首选)**: Vue 3, Vite, Pinia, Vue Router, Element Plus
  - **小程序端**: uni-app, Vue 3, Pinia, uni-app API
- **自动审计**: 包含参数绑定修复(-parameters)、Swagger集成、安全加固。
- **UI 生成**: 集成 frontend-design 技能，生成高颜值界面。

## 生成流程

请按顺序执行以下阶段：

### Phase 1: 设计生成 (Design)
**目标**：产出并验证所有核心设计文档。
1. **需求分析**：读取/生成需求文档与任务清单。
2. **完整性检查**：审计需求文档是否涵盖所有逻辑分支。
3. **数据库设计**：生成 ER 图或 SQL 设计文档（无外键，含索引）。
4. **API 设计**：输出详细接口文档。
5. **一致性审计**：执行 `Quality Gate A`（检查 DB + API 是否完全覆盖需求）。

### Phase 2: 后端实现 (Backend Implementation)
**目标**：基于 JDK 17 + Spring Boot 构建后端。
1. **骨架生成**：创建项目结构。
   - **关键**: 必须在 `pom.xml` 中配置 `<parameters>true</parameters>`。
   - **默认数据库基线**: 默认使用本地 MySQL 作为数据库，不要擅自切换为 PostgreSQL、SQLite 或其他数据库。
   - **默认连接参数**: 生成 `application.yml` / `application-dev.yml` / `application.properties` 时，默认按本机 MySQL 环境配置；密码固定使用 `QWlh759153.`。
   - **默认数据源约定**: 未经用户明确指定时，优先使用 `localhost:3306`、`root` 用户、MySQL 8.x 驱动与方言，保证生成项目可直接对接本地 MySQL。
2. **核心层构建**：生成 Entity, Repository, 建表 SQL。
3. **基础设施集成**：
   - 集成 `SpringDoc` (Swagger) 实现 API 文档自动生成。
   - 配置 `Spring Security` (或同等组件) 实现基础安全。
4. **业务填充**：实现 Service/Mapper 与 Controller。
5. **实现审计**：
   - 执行 `Security Gate`（检查密码加密、CORS 配置、SQL 注入风险）。
   - 执行 `Quality Gate B`（检查后端功能是否满足需求）。
   - 执行 `Quality Gate C`（检查接口实现是否符合 API 文档）。
   - 执行 `Quality Gate D`（检查 DB 结构是否支撑当前业务）。
   
### Phase 3: 前端规划 (Frontend Planning)
**目标**：规划前端方案和架构。
1. **方案判定**：
   - **默认使用Web端** → **Vue 3 + Element Plus** 方案
   - 仅在用户明确要求小程序端时 → 使用 **uni-app + Vue 3 + Pinia** 方案
2. **初始化规划**：基于后端代码与设计文档，输出前端开发计划 (`frontend_plan.md`)。
3. **Web端架构定义** (默认):
   - **框架**: Vue 3 (Composition API), Vite, Pinia, Vue Router, Element Plus
   - **依赖版本** (固定使用，不得更改):
     ```json
     {
       "vue": "^3.4.0",
       "vite": "^5.4.0",
       "pinia": "^2.1.0",
       "vue-router": "^4.4.0",
       "element-plus": "^2.8.0",
       "axios": "^1.7.0",
       "sass-embedded": "^1.97.3"
     }
     ```
   - **项目结构** (固定使用):
     ```
     src/
     ├── main.js                    # 入口
     ├── App.vue                    # 根组件
     ├── router/
     │   └── index.js               # 路由配置
     ├── views/                     # 页面
     ├── components/                # 组件
     ├── store/                     # Pinia
     ├── utils/
     │   └── request.js             # 请求封装
     ├── api/                       # API
     └── styles/
         └── common.scss            # 全局变量(必须导入)
     ```
   - **小程序端补充约束**: 若用户明确要求生成小程序端，则不要沿用 Web 端结构和依赖，必须切换到下述 uni-app 兼容规则。
4. **小程序端兼容规则** (仅在用户明确要求小程序端时启用):
   - **兼容基线项目**: `D:\Project\C26022704基于浇花系统的 微信小程序\frontend`
   - **核心原则**: 生成的小程序前端必须尽量与该可运行项目保持版本、目录结构、入口写法和请求封装风格一致，优先保证可直接运行和部署成功。
   - **依赖版本** (固定使用，不得擅自升级、替换或混搭):
     ```json
     {
       "@dcloudio/uni-app": "3.0.0-4020920240930001",
       "@dcloudio/uni-mp-weixin": "3.0.0-4020920240930001",
       "@dcloudio/vite-plugin-uni": "3.0.0-4020920240930001",
       "vue": "^3.4.0",
       "pinia": "^2.1.0",
       "vite": "^5.4.0",
       "sass-embedded": "^1.97.3"
     }
     ```
   - **脚本** (固定使用):
     ```json
     {
       "dev:mp-weixin": "uni -p mp-weixin",
       "build:mp-weixin": "uni build -p mp-weixin"
     }
     ```
   - **构建配置**: `vite.config.js` 保持 `defineConfig({ plugins: [uni()] })` 这种最简形式，不额外添加高风险插件或复杂构建配置。
   - **入口写法**: `src/main.js` 必须使用 `createSSRApp(App)` + `createPinia()` 初始化，保持与基线项目一致。
   - **项目结构** (优先保持一致):
     ```
     src/
     ├── App.vue
     ├── main.js
     ├── manifest.json
     ├── pages.json
     ├── api/
     ├── pages/
     ├── store/
     │   ├── index.js
     │   └── user.js
     ├── styles/
     │   └── common.scss
     └── utils/
         └── request.js
     ```
   - **页面组织**: 优先使用 `pages/tabbar/...`、`pages/login/...`、`pages/[业务模块]/...` 的目录方式，不随意改成其他风格。
   - **请求封装**: 优先沿用 `uni.request` Promise 封装模式，统一处理 `token`、`401` 失效跳转、`uni.showToast` 报错提示、`uploadFile` 上传。
   - **状态管理**: 保持 `src/store/index.js` 仅做导出聚合，用户登录态放在 `src/store/user.js`。
   - **实现限制**: 不引入与基线项目差异过大的请求库、UI 库、状态管理方案、自动导入插件、实验性语法或自定义运行时封装，避免导致微信开发者工具或 uni-app 构建失败。
   - **缺少基线信息时的处理**: 若当前任务无法读取基线项目，或用户未提供关键配置文件，必须先向用户索要 `frontend/package.json`、`vite.config.js`、`src/main.js`、`src/utils/request.js` 后再生成，不得凭经验臆造。
5. **设计系统**：**必须加载 `frontend-design` Skill**，拒绝默认样式，追求现代美学。
6. **字典管理**：规划所有下拉菜单的字典项来源。

### Phase 4: 前端实现 (Frontend Implementation)
**目标**：基于计划文档开发前端。
1. **快速开始**：按固定结构初始化 Web 项目。
   - 创建 `package.json` (使用固定依赖版本)
   - 创建 `src/styles/common.scss` (包含所有变量)
   - 创建 `src/utils/request.js` (封装请求，携带 Token)
   - 创建 `src/store/` 目录结构
   - 配置 `router/index.js` 与 `vite.config.js`
   - 若用户要求小程序端，则改为按“**小程序端兼容规则**”初始化，不得套用 Web 端脚手架结构。
2. **迭代开发**：按计划文档逐个模块实现。
   - **交互规范**: 严禁让用户输入 ID，必须使用 picker 组件。
   - **样式规范**: 每个页面 `<style lang="scss" scoped>` 第一行必须是 `@import '@/styles/common.scss';`
   - **编码规范**: UTF-8，中文界面
   - **小程序兼容要求**: 对于 uni-app 页面、路由、请求、上传、登录态恢复等实现，优先复制基线项目的写法和组织方式，不为追求“更现代”而换成另一套工程风格。
3. **状态管理**：
   - 用户状态: `store/user.js` (token, userInfo)
   - App 启动时从 storage 恢复登录状态
4. **最终集成测试**：验证前后端交互逻辑。

### Phase 5: 测试数据生成 (Test Data)
**目标**：生成可直接执行的数据库初始化 SQL，让项目启动后立即有数据可用。
1. **分析数据依赖**：根据数据库表结构确定插入顺序（主表先于关联表）。
2. **生成 `init_data.sql`**：
   - 覆盖所有业务表，每张表至少 3~5 条有意义的数据。
   - 数据必须符合业务逻辑（如状态值、枚举值、日期关系均合法）。
   - 包含适度的"异常场景"数据（如已跳过、已删除等边界状态），方便测试。
   - 使用固定 `id`，保证外键引用正确。
   - 文件顶部注明使用说明（先执行建表 SQL，再执行本文件）。
3. **生成验证查询**：在文件末尾以注释形式附上 3~5 条 SELECT 语句，用于快速核实数据是否正确导入。

## 审计指令 (Quality Gates)

当用户要求“检查 X 是否满足 Y”时，请严格对比两者：
- **Missing Features**: 需求有但设计/代码没写的。
- **Redundant Features**: 设计/代码有但需求没提的（需确认）。
- **Data Mismatch**: 字段类型、长度、必填项在各层是否一致。

## 参考资料
- 详细后端步骤：请参考 `references/checklist_backend.md`
- 详细前端步骤：请参考 `references/checklist_frontend.md`
