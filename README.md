# Benjamin Plugins

Benjamin 的 Codex 插件仓库。包含 **AI-Native SDLC**（完整软件流程与六个专项 Skills）和 **LoopX**（长期任务、证据验收与持续执行），可在不同项目中复用。

这个仓库负责保存版本和分发安装包。插件安装到每台机器的 Codex 后，在该机器的项目中使用。

## 安装

前提：已安装支持 Plugin 的 Codex CLI，GitHub 账号拥有此私有仓库的读取权限，SSH Key 已配置。

```bash
codex plugin marketplace add git@github.com:Yidada/benjamin-plugins.git --ref main
codex plugin add ai-native-sdlc@personal
codex plugin add loopx@personal
```

安装后在 Codex 中新建任务。仓库名称为 `benjamin-plugins`，仓库内 marketplace 的标识为 `personal`，安装命令使用后者。

每台电脑需要分别安装；私有仓库仅对获授权的 GitHub 账号开放。如果该机器已配置另一个名为 `personal` 的 marketplace，应先检查 `codex plugin marketplace list` 的结果，解决名称冲突后再添加。

如果此前通过本地 `benjamin-personal` 市场安装过同名插件，请先确认准备使用哪个来源，再迁移安装，避免同时启用重复 Skills。

## 使用

```text
用 $ai-native-sdlc start 实现分页 API，交付本地代码并完成验证。
用 $sdlc-test 只读检查当前 diff，找出缺陷和验证缺口。
用 $ai-native-sdlc audit 只读检查当前项目的流程与证据。
```

| Skill | 用途 |
|---|---|
| `$ai-native-sdlc` | 用户明确调用后，管理完整生命周期、风险和证据 |
| `$sdlc-plan` | 问题定义、验收条件和计划 |
| `$sdlc-design` | 方案、接口、数据和兼容性 |
| `$sdlc-build` | 实现、修复和重构 |
| `$sdlc-test` | 测试、评估和代码审查 |
| `$sdlc-release` | PR、发布和回滚 |
| `$sdlc-maintain` | 故障诊断和维护 |

专项 Skills 可按当前任务选用。项目自己的 `AGENTS.md`、技术栈和命令继续生效。详细行为及边界见 [插件说明](plugins/ai-native-sdlc/README.md)。

### LoopX 长期任务

```text
用 $loopx start 重构这个模块，保持 API 兼容并通过测试。
用 $loopx status 查看当前目标、证据、阻塞与下一步。
用 $loopx resume 接着上次的工作继续。
```

LoopX 复用官方内核，执行机器需要 Python 3.11+。跨会话推进需要持久项目及实际宿主调度器；插件创建本身不会启动后台任务。详见 [LoopX 插件说明](plugins/loopx/README.md)。

## 更新已安装的版本

完成上面的 Git marketplace 安装后，运行：

```bash
codex plugin marketplace upgrade personal
codex plugin add ai-native-sdlc@personal
codex plugin add loopx@personal
```

然后新建 Codex 任务以使用更新内容。更新仓库会刷新可安装版本；已打开任务的上下文不会随之改写。

## 修改和验证

建议使用独立 Git checkout 维护源码：

```bash
git clone git@github.com:Yidada/benjamin-plugins.git
cd benjamin-plugins
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python plugins/ai-native-sdlc/skills/ai-native-sdlc/scripts/test_sdlc.py
.venv/bin/python plugins/loopx/skills/loopx/scripts/test_preflight.py
```

- `scripts/validate.py` 检查 marketplace、插件目录、Skills、YAML、相对链接和评估案例格式。
- `test_sdlc.py` 在临时目录中运行 28 个 CLI 测试，覆盖路径边界、审批记录、阶段条件与变更恢复。
- GitHub Actions 在 push、pull request 和手动触发时执行上述检查。
- AI-Native SDLC 自带 12 个行为评估案例，LoopX 自带 10 个；此 CI 仅验证案例结构，模型评估需另外执行。
- 更新插件内容时同时更新 manifest 的 `version`，以便客户端获取新版本。使用 Codex 的 `plugin-creator` 维护本地版本时，按该 Skill 的 cachebuster helper 流程执行。

## 文件结构

```text
.agents/plugins/marketplace.json    安装目录
.github/workflows/validate.yml      持续校验
plugins/ai-native-sdlc/             插件源码
plugins/loopx/                      长期任务插件
scripts/validate.py                仓库结构校验
```

概念来源及独立实现说明见 [SOURCE.md](plugins/ai-native-sdlc/SOURCE.md)。当前插件为私人使用，manifest 标记为 `UNLICENSED`。
