# 来源与适配范围

阅读日期：2026-09-05。

- Bruce Lee：[LoopX：比 Goal 更懂长期任务](https://x.com/Bruce_Lee1207/status/2096067575323177252)。已阅读网页完整正文；文章作为需求与概念来源。
- 官方项目：[huangruiteng/loopx](https://github.com/huangruiteng/loopx)。
- 核对版本：`0.5.4`，源码 revision `d0d729a0a89dda9de3d3d4e3c2407b2a8b8c6434`。
- [Getting started](https://github.com/huangruiteng/loopx/blob/d0d729a0a89dda9de3d3d4e3c2407b2a8b8c6434/docs/guides/getting-started.md) 与 CLI 帮助用于核对安装、guided start、host、quota、heartbeat 和 review-packet。

本插件独立编写 Skill、文档与环境检查脚本，通过 CLI 使用官方内核，不分发或复制其内核源码。官方项目当前许可见其 LICENSE/NOTICE；本私人插件沿用仓库的 UNLICENSED 标记。

## 实现中保留的区别

1. `start-goal --guided` 返回只读事务预览，后续真实写入和读回完成后才能确认创建成功。
2. 文章的 run/ask/wait/repair/quiet 用于解释决策类别，实际执行读取当前版本的 interaction_contract。
3. should-run 的基础判断与带 turn/receipt/cache 参数的调用具有不同写入语义，查询模式不附加记账参数。
4. 未扣 slot 与模型服务的实际账单分别统计。插件不承诺等待或失败期间零费用。
5. 验证回执和持久状态依赖官方内核及实际证据；插件文字本身不会提供机械保证。
6. 唤醒由可访问持久项目的宿主完成。调度失败不写成功 ACK，也不声称后台已运行。
