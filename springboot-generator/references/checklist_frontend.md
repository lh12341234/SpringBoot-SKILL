# 前端开发详细清单 (Frontend Checklist)


## 1. 前端规划

### 方案 A: 仅有小程序端
- [ ] **Input**: 后端源码、`REQUIREMENTS.md`、`DESIGN_API.md`。
- [ ] **Output**: `frontend/PLAN_FRONTEND_MINIPROGRAM.md`。
- [ ] **Tech Stack**: uni-app, Vue 3, Pinia, uni-app API, 自定义 request 封装。
- [ ] **Design System**:
  - **强制调用**: 在开始编写 UI 代码前，必须加载 `frontend-design` Skill。
  - **审美要求**: 拒绝默认 UI 库样式，必须实现现代、独特的设计语言（卡片式、毛玻璃、微动效）。
  - **小程序特性**: 遵循微信小程序设计规范，适配安全区域（刘海屏）。
- [ ] **UX 规范 (关键)**:
  - ** picker/picker-view**: 所有枚举值、状态、外键关联必须使用 picker 组件，禁止让用户手动输入 ID。
  - **ID 透明化**: 表单交互中，用户只能看到和选择"名称"（Name），ID 的绑定由前端逻辑完成。
  - **字典处理**: 所有状态字段必须封装为 picker 组件。
- [ ] **Key Requirements**:
  - 编码：UTF-8。
  - 语言：中文。
  - 会话管理：App Launch 时检查本地 storage 的 token 和 userInfo。

### 方案 B: 仅有Web端
- [ ] **Input**: 后端源码、`REQUIREMENTS.md`、`DESIGN_API.md`。
- [ ] **Output**: `PLAN_FRONTEND_WEB.md`。
- [ ] **Tech Stack**: Vue 3, Vite, Pinia, Vue Router, Element Plus, Axios。
- [ ] **Design System**:
  - **强制调用**: 在开始编写 UI 代码前，必须加载 `frontend-design` Skill。
  - **审美要求**: 拒绝默认 UI 库样式，必须实现现代、独特的设计语言（如毛玻璃、卡片式、微动效）。
- [ ] **UX 规范 (关键)**:
  - **下拉优先**: 所有枚举值、状态、外键关联（如场馆、用户）必须使用下拉选择组件 (`el-select`)，禁止让用户手动输入 ID 或状态码。
  - **ID 透明化**: 表单交互中，用户只能看到和选择"名称"（Name），ID 的绑定与传输由前端逻辑在后台完成，界面上应隐藏纯数字 ID。
  - **字典处理**: 所有状态字段必须封装为字典组件。
- [ ] **Key Requirements**:
  - 编码：UTF-8。
  - 语言：中文。
  - 会话管理：页面刷新自动调用 `/api/auth/me` 恢复 Token 和用户信息。

### 方案 C: 双端都有（小程序 + Web）
- [ ] **Output**:
  - `frontend/PLAN_FRONTEND_MINIPROGRAM.md`
  - `frontend/PLAN_FRONTEND_WEB.md`
- [ ] **共用设计**: 后端 API 设计对双端通用，接口响应格式一致。
- [ ] **分别实现**:
  - 小程序端遵循方案 A 的所有要求
  - Web端遵循方案 B 的所有要求
- [ ] **功能对等**: 确保核心功能在两端都能正常使用（小程序端可适当简化）。

## 2. 迭代开发
- [ ] 按照 `frontend/快速开始.md` (如果存在) 或标准流程初始化。
- [ ] **按计划执行**：每完成一个模块，更新对应的 `PLAN_FRONTEND_*.md` 状态。

## 3. 管理员与权限

### Web端 (Element Plus)
- [ ] **路由守卫 (Guards)**:
  - 登录成功后判断角色。
  - `ROLE_ADMIN` -> 跳转 `/admin/dashboard` (后台管理布局)。
  - `ROLE_USER` -> 跳转 `/` 或 `/home` (前台布局)。
- [ ] **后台管理系统**:
  - 侧边栏菜单（动态生成或静态配置）。
  - 用户管理、数据统计等管理功能。
  - 管理员入口：平台管理员角色需增加一个按钮进入后端管理系统。

### 小程序端 (uni-app)
- [ ] **页面跳转逻辑**:
  - 登录成功后判断角色。
  - `ROLE_ADMIN` -> `uni.redirectTo` 跳转管理员页面（`/pages/admin/dashboard/index`）
  - `ROLE_USER` -> `uni.switchTab` 跳转首页（`/pages/tabbar/home/index`）
  - 服务商角色 -> 跳转服务商工作台（`/provider-pages/tabbar/dashboard/index`）
- [ ] **分包加载**: 管理员页面使用 subPackages（`admin-pages`）独立分包。
- [ ] **权限控制**: 未授权角色访问管理页面时自动跳转回首页。

## 4. 集成验证

### Web端
- [ ] 检查所有 API 调用是否通过 Axios 拦截器处理（携带 Token）。
- [ ] 验证后端返回 401/403 时的前端处理（跳转登录）。

### 小程序端
- [ ] 检查所有 API 调用是否通过自定义 request 封装处理（携带 Bearer Token）。
- [ ] 验证后端返回 401/403 时的小程序处理（清除本地 storage，跳转登录页）。
- [ ] 验证分包加载是否正常（管理员分包、服务商分包）。
- [ ] 图片上传必须为手动上传文件（Web: 上传组件；小程序: chooseImage+upload）；禁止图片URL手工输入。
