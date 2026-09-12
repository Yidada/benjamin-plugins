# AI Video Motion Replica

用「白模」把参考视频的动作、走位和机位提取出来，再用人物三视图和空场景图渲染成成片，解决口述提示词无法还原复杂舞蹈、武术和打斗动作的问题。

- 插件名：`ai-video-motion-replica`
- Skill：`$ai-video-motion-replica`
- 适用：舞蹈 / 武术 / 打斗动作视频的复刻与换角、换风格

## 安装

```bash
codex plugin add ai-video-motion-replica@personal
```

## 使用

```text
用 $ai-video-motion-replica 把这段参考视频的动作复刻成我的角色。
用 $ai-video-motion-replica 做一段多人齐舞，主角是 A，后排在 B/C/D。
```

## 工作流

1. 参考视频 → 深度动作捕捉 → 白模（只保留位置、轨迹、机位）。
2. 生成人物三视图 + 空场景图。
3. 白模 + 人物图 + 场景图 → 视频模型（MiniMax H3 / Libtv / 优云智算），提示词只补细节。
4. 多人时命名 `A`/`B`/`C`/`D` 按名字引用；长片拆成 5s 分段生成。

详细步骤见 [SKILL.md](skills/ai-video-motion-replica/SKILL.md)，提示词模板见 [references/prompts.md](skills/ai-video-motion-replica/references/prompts.md)。

概念来源见 [SOURCE.md](SOURCE.md)。
