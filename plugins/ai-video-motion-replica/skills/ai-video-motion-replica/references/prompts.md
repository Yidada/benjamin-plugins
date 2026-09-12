# 提示词模板

## 1. 角色三视图（角色设定图）

通用结构：`三视图布局 + 主体设定 + 服装逐项 + 各视角姿态 + 一致性 + 画质 + NEGATIVE`

示例（可爱写实少女·哪吒）：

```text
Professional character design turnaround sheet, three views only on clean white studio background.
Horizontal layout: front view, left side profile, back view — three full-body standing poses side by side,
complete heads visible in every view, empty hands at sides, NO weapon, NO spear, NO staff in any view.
Subject: cute beautiful real young Chinese girl as feminine Nezha, photorealistic semi-realistic style
(NOT flat anime, NOT cartoon). Black hair in two ox-horn buns, red headband with long flowing red ribbons,
large expressive eyes, cute youthful face with fair smooth skin, determined sweet expression.
Outfit: sleeveless red high-collar top with gold lotus chest embroidery, gold-red arm gauntlets,
wide red waist sash with gold lotus buckle, layered red skirt panels with gold flame trim over red pants,
red boots with gold lotus shin guards. Side view: standing naturally in profile, hands relaxed at sides,
red ribbon flowing. Back view: full back visible, headscarf ribbons trailing.
Consistent character identity across all three views. High detail costume texture, soft studio lighting,
character reference sheet quality.
NEGATIVE: weapon, spear, fire-tipped spear, staff, sword, jian, gun, holding object, anime cartoon flat style,
chibi, deformed body, missing head, cropped head, extra limbs, wrong number of fingers, blurry face,
inconsistent costume between views, multiple characters, text, watermark, logo, background scene, outdoor,
shadow clutter, low quality, plastic doll skin
```

要点：
- 强制 `front / left side / back` 三视图，全身、头完整、空手无武器。
- 服装逐件描述（领口/刺绣/护腕/腰带/裙摆/靴），保证多视角一致。
- 负面词显式排除武器、动漫扁平风、多余肢体、视角间服装不一致。

## 2. 场景图（空场景）

```text
Empty ancient Chinese martial arts performance stage interior, no people, no characters.
Wide cinematic 16:9 composition with open center floor space for a dancer.
Dark polished wooden floor with subtle warm reflections. Two vermilion red lacquered pillars on left and right,
ornate carved wooden screens beside them. Back wall draped with large ink-wash landscape painting curtain
in muted gray-blue tones. Traditional Chinese hall architecture, wooden beams and rafters visible overhead.
Warm amber lantern side lighting from both sides plus soft top spotlight on center stage.
Thin natural white mist and volumetric light beams drifting low across the floor.
Rich red-gold theatrical color palette, dramatic stage lighting, photorealistic, cinematic atmosphere,
high detail, empty stage ready for performance.
NEGATIVE: people, character, dancer, mannequin, crowd, modern interior, concrete floor, neon lights,
outdoor scene, daylight sky, text, subtitle, watermark, logo, low quality, blurry, oversaturated,
cluttered props, weapons rack, furniture blocking center stage, western architecture, sci-fi elements
```

要点：
- 首句必须 `empty / no people`，中央留出活动空间给舞者。
- 明确画幅（16:9）、光源方向、色调、氛围。
- 负面词排除人物/杂物/现代元素/水印。

## 3. 视频生成提示词（白模 + 角色图 + 场景图）

只写模型需要补的信息，动作/走位/机位交给白模。模板：

```text
[角色名/主体]，[服装风格]，
在[场景描述]，[色调与打光]，
[镜头运动：推/拉/环绕/俯拍/跟拍]，与参考白模的动作和走位保持一致，
[需补的细节：衣摆飘动、刀刃火星、地面雾气、头发甩动、表情微变]，
[风格：写实/水墨/电影感]，[画质：4K, cinematic, high detail]
NEGATIVE: [变形、多手多脚、人物融合、糊、动作漂移、风格偏离、文字水印]
```

单挑/打斗示例要点：
- 明确「弹反、踩刀、处决」等关键帧动作由白模保留，提示词只补「刀刃火星、衣摆、下压机位」。
- 强调两人从头到尾不糊在一起。

多人舞蹈示例要点：
- 用 `A` `B` `C` `D` 命名引用每个人；说明主角是谁、前后站位。
- 描述 10s 节奏：主角起手 → 队伍展开 → 齐舞卡点 → 定格收势。
- 强调「人数不减少、队形不乱、卡点对齐」。

## 4. 负面词速查

- 人物：`deformed body, extra limbs, wrong number of fingers, missing head, cropped head, blurry face, multiple characters, character fusion`
- 风格：`anime cartoon flat style, chibi, plastic doll skin, inconsistent costume`
- 画面：`text, watermark, logo, low quality, blurry, oversaturated`
- 场景：`people, mannequin, crowd, cluttered props, furniture blocking center stage`
