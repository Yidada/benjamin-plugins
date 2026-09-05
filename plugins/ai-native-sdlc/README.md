# AI-Native SDLC · Benjamin 的全局开发工具包

一个 Codex Plugin，包含七个 Skills。全局范围是当前用户的 Codex；具体技术栈、命令和代码规范继续由项目提供。

| 入口 | 用途 | 触发 |
|---|---|---|
| `$ai-native-sdlc` | 完整开发流程与证据记录 | 必须明确调用 |
| `$sdlc-plan` | 明确问题、验收条件和任务计划 | 可按软件规划任务自动选用 |
| `$sdlc-design` | 方案、接口、数据和兼容性设计 | 可按设计任务自动选用 |
| `$sdlc-build` | 功能实现、修复和重构 | 可按编码任务自动选用 |
| `$sdlc-test` | 测试、评估和代码审查 | 可按验证任务自动选用 |
| `$sdlc-release` | PR、发布和回滚 | 可按交付任务自动选用 |
| `$sdlc-maintain` | 故障诊断和维护改进 | 可按维护任务自动选用 |

## 开始使用

安装后，在目标项目中新建 Codex 任务：

```text
用 $ai-native-sdlc start 实现 <需求>，交付本地代码并完成验证。
```

也可以只执行一个任务：

```text
用 $sdlc-test 只读检查当前 diff，找出具体缺陷和验证缺口。
用 $ai-native-sdlc audit 只读检查当前项目的流程与证据。
用 $ai-native-sdlc resume 继续 <change-id>。
```

完整流程在目标 Git 仓库维护 `.sdlc/changes/<change-id>/`。按风险创建 3、6 或 9 份 Markdown 工件。审计不初始化目录。专项 Skills 不自动启动完整流程。

## 安装与维护

完整的 SSH 安装、更新和开发命令见 [仓库说明](../../README.md)。

- 本仓库的插件 ID 为 `ai-native-sdlc@personal`。
- 修改源码后运行验证并更新版本，再发布到 GitHub。
- 每台机器分别刷新 marketplace、安装插件，并新建任务读取新版。
- 当前机器的安装不会自动同步到远程主机或其他 AI 应用。

## 验证与边界

```text
python3 skills/ai-native-sdlc/scripts/test_sdlc.py
python3 skills/ai-native-sdlc/scripts/sdlc.py --repo <repo> inspect
```

- 脚本使用 Python 标准库和 Git。
- `evals/scenarios.json` 提供 12 个行为评估案例，供后续模型或 Skill 更新时使用。它们没有自动调用模型或创建定时任务。
- 本地校验检查记录、阶段条件与审批范围变化；真实测试结果仍需核对工具输出。
- 生产访问控制通过实际 CI、仓库保护和部署权限执行。Skills 和本地审批记录无法替代这些平台控制。
- 使用现有项目工具，无附带 MCP 服务、远程账号、后台监控或全局 Shell Hook。

概念来源与独立实现说明见 [SOURCE.md](SOURCE.md)。
