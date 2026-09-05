# LoopX

把长期任务交给官方 LoopX 管理：目标、待办、边界、证据、配额和交接保存在执行机器上，每轮根据最新状态决定如何继续。

## 安装与使用

在已经配置本仓库 marketplace 的机器上安装：

```bash
codex plugin marketplace upgrade personal
codex plugin add loopx@personal
```

插件负责工作流；执行机器还需要 Python 3.11+ 和官方 LoopX CLI。首次要求接入时，Skill 会检查并处理缺失依赖，默认使用独立环境。源码契约按 LoopX 0.5.4 核对，已有安装会读取实际版本的帮助与执行契约。

```text
用 $loopx start 重构这个模块，保持 API 兼容，通过现有测试。
用 $loopx status 查看当前目标、已验证的进展、阻塞和下一步。
用 $loopx resume 接着上次的工作继续。
用 $loopx replan 先支持 SQLite，保留之前完成的工作与证据。
用 $loopx report 给我当前任务的审查包。
用 $loopx pause 暂停这个目标的后续调度。
```

`start/status/resume/replan/report/pause` 是 Skill 的对话入口，实际操作调用官方支持的命令。

## 行为

| 能力 | 实现 |
| --- | --- |
| 开工 | 精确目标、验收条件、范围和有序待办；预览之后验证真实写入 |
| 每轮推进 | fresh guard → claim → 执行与验证 → 接受回执 → 记账 |
| 中断恢复 | 检查未闭合回执、认领与外部结果，保留失败记录 |
| 改计划 | 使用官方变更流程，保留历史和任务来源 |
| 完成验收 | 核验验收缺口、后继任务、监控及评审义务，读取内核闭合结论 |
| 持续运行 | 使用实际宿主的 Goal 或调度器，按 scheduler_hint 退避并验证更新 |

查询状态不会自动创建目标。LoopX 的 slot 代表逻辑配额，不能据此推断模型调用费用为零。全文解读与官方实现的对应说明见 [SOURCE.md](SOURCE.md)。

## 执行边界

- 当前插件提供一个 Skill、环境检查脚本和执行参考，没有远程 MCP 服务。
- 持续运行需要能访问同一项目及其持久状态的宿主调度器。仅安装插件或手机聊天无法证明后台已经启动。
- 本版本没有 Multica API/调度桥接；将来可由执行机器上的 Runtime 接入。
- 可引用 AI-Native SDLC 的验收与证据文件，LoopX 负责长期任务状态和后续执行。
- 不会创建用户任务、启动定时器或安装额外全局 Skills，直到用户提出对应工作请求。

## 验证

```bash
python3 scripts/validate.py
python3 plugins/loopx/skills/loopx/scripts/test_preflight.py
```

从仓库根目录执行。环境检查测试覆盖只读查询、保留已有状态、损坏/缺失状态和命令注入输入。`evals/scenarios.json` 包含 10 个行为场景；结构校验不会运行模型评估。
