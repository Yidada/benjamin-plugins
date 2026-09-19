# AI-Native SDLC · Benjamin 的全局开发工具包

一个 Codex Plugin，包含七个 Skills。整体逻辑对齐 Anthropic 的 [AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)。全局范围是当前用户的 Codex；具体技术栈、命令和代码规范继续由项目提供。

| 序号 | 入口 | 阶段 play | 提交的工件 | 触发 |
|---|---|---|---|---|
| 0 | `$ai-native-sdlc` | 完整循环与证据记录 | `.sdlc/changes/<id>/` 全部工件 | 必须明确调用 |
| 1 | `$sdlc-plan` | 用发起人的原话捕获意图 | intent.md | 可按规划任务自动选用 |
| 2 | `$sdlc-design` | 一次会话完成需求与设计，边写边套用规范 | spec.md | 可按设计任务自动选用 |
| 3 | `$sdlc-build` | 先 plan mode 再写代码，自我验证反馈环 | plan.md、diff 与测试 | 可按编码任务自动选用 |
| 4 | `$sdlc-test` | 持续评估与分级审查 | evidence.md、review.md | 可按验证任务自动选用 |
| 5 | `$sdlc-release` | 双向审查、PR、发布，止步于生产门禁 | PR 与发布记录 | 可按交付任务自动选用 |
| 6 | `$sdlc-maintain` | 由触发器启动诊断，写回新的 intent | 事故记录、新 intent.md | 可按维护任务自动选用 |

## 循环逻辑

- 六个阶段是一个循环。每个阶段结束时提交一份工件，下一个阶段读取它：intent.md → spec.md → plan.md → diff 与测试 → evidence.md → review.md 与 PR → 事故记录 → 新的 intent.md。
- 提交链就是审计记录：谁提出了什么，Agent 产出了什么，谁批准了。
- 人负责判断：接受意图、批准方案、接受计划、Code Owner 合并 PR、授权发布。Agent 负责生成、执行和机械验证，走到生产门禁为止。
- 两层护栏：Skills 和 AGENTS.md 是建议性控制；Hook、CI、分支保护和部署权限是确定性控制。必须始终成立的规则需要确定性控制兜底。
- 风险等级决定记录多少工件和哪些决定需要显式记录。低影响范围的变更按用户请求通过各门禁；R3 记录每一个门禁决定。

## 开始使用

选择菜单中的显示名称按 0–6 编号：0 为总流程，1–6 对应意图、设计、开发、测试、发布和维护。序号帮助识别阶段；调用仍使用原有 `$skill-name`。

安装后，在目标项目中新建 Codex 任务：

```text
用 $ai-native-sdlc start 实现 <需求>，交付本地代码并完成验证。
```

也可以只执行一个 play：

```text
用 $sdlc-plan 整理这个需求的意图。
用 $sdlc-test 只读检查当前 diff，找出具体缺陷和验证缺口。
用 $ai-native-sdlc audit 只读检查当前项目的流程与证据。
用 $ai-native-sdlc resume 继续 <change-id>。
```

完整流程在目标 Git 仓库维护 `.sdlc/changes/<change-id>/`。按风险创建 3、6 或 9 份 Markdown 工件。进入 Build 之前必须有已接受的 plan.md。审计不初始化目录。专项 Skills 不自动启动完整流程。

## 落地顺序

按依赖关系逐步启用，先做没有前置条件的 play：

1. 用 intent 模板记录新需求；保持 AGENTS.md 在一页以内；每个检查一条命令并附健康输出；至少一条确定性 Hook 或 CI 检查；先 plan mode 再改代码。
2. 把必须一致执行的规范写成 Skill；把重复工作交给命名的子代理；为 Agent 配置建立评估集。
3. 一次会话完成需求与设计；PR 审查按固定 pass 执行。
4. CI/CD 集成与审批门禁。
5. 监控触发写回新的 intent，闭合循环。

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
- `evals/scenarios.json` 提供 20 个行为评估案例，覆盖意图捕获、plan mode、计划同步、先写失败测试、配置变更评估、分级审查、事故写回 intent 等行为。它们没有自动调用模型或创建定时任务。
- 本地校验检查记录、阶段条件与审批范围变化；真实测试结果仍需核对工具输出。
- 生产访问控制通过实际 CI、仓库保护、Hook 和部署权限执行。Skills 和本地审批记录无法替代这些平台控制。
- 使用现有项目工具，无附带 MCP 服务、远程账号、后台监控或全局 Shell Hook。
- 各阶段的度量指标见 `skills/ai-native-sdlc/references/measures.md`，只从 Git、CI 和事故记录读取，不虚构基线。

概念来源与独立实现说明见 [SOURCE.md](SOURCE.md)。
