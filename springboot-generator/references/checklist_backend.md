# 后端开发详细清单 (Backend Checklist)

## 1. 需求与任务
- [ ] **Input**: 读取原始需求描述。
- [ ] **Output**: 生成 `REQUIREMENTS.md` 和 `TODO_BACKEND.md`。
- [ ] **Action**: 确保每个功能点都有对应的验收标准。

## 2. 完整性自检
- [ ] 检查是否存在逻辑漏洞（例如：有充值功能但没有扣款逻辑）。
- [ ] 补充遗漏的边缘情况（Edge Cases）。

## 3. 数据库设计
- [ ] **Output**: `DESIGN_DATABASE.md` 或 `.sql` 文件。
- [ ] **Rule**:
  - 不使用物理外键（Foreign Keys），在应用层维护关联。
  - 关键查询字段必须设计索引（Index）。
  - 包含 `create_time`, `update_time` 等审计字段。

## 4. 接口文档
- [ ] **Output**: `DESIGN_API.md` (OpenAPI/Swagger 风格)。
- [ ] 定义 URL, Method, Request Body, Response, Error Codes。

## 5. 设计审计 (Gate A)
- [ ] 对比 `DESIGN_DATABASE.md` 和 `DESIGN_API.md` vs `REQUIREMENTS.md`。
- [ ] 确保每个需求都有对应的数据表和接口。

## 6. 骨架生成
- [ ] JDK 17
- [ ] Spring Boot (最新稳定版)
- [ ] **关键配置**: 在 `pom.xml` 的 `maven-compiler-plugin` 中开启 `<parameters>true</parameters>`，防止 Controller 参数名丢失导致 400 错误。
- [ ] **API 文档**: 引入 `springdoc-openapi-starter-webmvc-ui` 依赖，自动生成 Swagger UI。
- [ ] Project Structure: `Controller`, `Service`, `Mapper/Repository`, `Entity`, `DTO`, `VO`.

## 7. 核心代码生成
- [ ] Entity 类（使用 Lombok）。
- [ ] Repository 接口 / Mapper XML。
- [ ] DDL SQL 脚本（确保与 Entity 一致）。
- [ ] 补齐具体 Service 业务逻辑。

## 8. 功能与安全审计 (Gate B)
- [ ] 遍历 `REQUIREMENTS.md`，检查 Service 层逻辑是否覆盖所有条目。
- [ ] **Security Check**:
  - [ ] 密码是否已加密存储（BCrypt/Argon2）。
  - [ ] SQL 是否全部通过 JPA/MyBatis 参数化执行（防注入）。
  - [ ] CORS 是否已配置且仅允许特定前端域名。

## 9. 接口一致性审计 (Gate C)
- [ ] 检查 Controller 实现是否与 `DESIGN_API.md` 定义一致（参数、返回值）。

## 10. 结构一致性审计 (Gate D)
- [ ] 检查最终代码中的 Entity 是否与 `DESIGN_DATABASE.md` 和 `DESIGN_API.md` 冲突。
