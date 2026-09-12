# Source and implementation boundary

Conceptual reference: X (Twitter) thread by [@laowangbabababa](https://x.com/laowangbabababa), "我用 MinimaxH3 也复刻出来白模的舞蹈视频了" and the long-form article《Libtv 靠白模精准复刻动作大片，附保姆级教学》, published 2026-09-05, consulted 2026-09-12.

The source describes a white-model (depth motion capture) workflow: strip a reference video down to a depth skeleton, generate character turnaround sheets and an empty scene, then render the final clip with MiniMax H3 via Libtv or 优云智算 (compshare). This plugin is an independent packaging of that workflow for Benjamin's Codex environment. Its step structure, prompt templates, platform notes and evaluation scenarios are local design choices.

No third-party service is bundled, no automated generation is triggered, and no credential is stored. Platform names, pricing and model capabilities are time-sensitive and should be re-verified before use.
