# Scene Asset Prompt Pack

> Generated from `scene-asset-prompt-pack.yaml`. Do not edit this Markdown manually.

## Rules

- `midjourney_role`: scene_master_only
- `banana_role`: derive_reverse_angle_variant_and_repair
- `scene_pipeline`: scene_master_then_banana_derived_views

## `LOC_KAMIKAZE_ACADEMY_GROUNDS`

### Summary

- `status`: prompted
- `required_outputs`: `scene_master`、`reverse_seed`

### Midjourney

#### scene_master

```text
神风学院操场, 学院公开抽卡仪式、群像嘲讽与男主首次东方神明显圣的白天主场景。, academy courtyard ceremonial draw arena, central draw pool pedestal, surrounding west myth statues, academy facade and open sports ground, crowd ring zone for students, readable hero center lane toward draw pool, PROP_DRAW_POOL_MAIN, CARD_SUMMON_CARD_BASE, PROP_WESTERN_STATUE_SET, VFX_GOLDEN_SKY_ANOMALY, VFX_RAINBOW_LIGHT_PILLAR, day, clear, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, readable wide composition, camera coverage seeds: front wide master, low-angle hero push-in, crowd-side three-quarter angle, statue-line cutaway, not photoreal --ar 16:9 --v 7 --raw
```

#### reverse_seed

```text
same 神风学院操场, reverse-side view of the same space, preserve central draw pool pedestal, surrounding west myth statues, academy facade and open sports ground, crowd ring zone for students, readable hero center lane toward draw pool, preserve layout logic, same day, clear, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still --ar 16:9 --v 7 --raw --oref [KAMIKAZE_ACADEMY_GROUNDS_MASTER] --ow 200
```

### Banana Pro

#### layout_cleanup

```text
保留神风学院操场的空间布局、透视、锚点和光照不变，只清理错误结构与不稳定细节，使它成为后续镜头可复用的稳定母图。
```

## `LOC_PRINCIPAL_OFFICE`

### Summary

- `status`: prompted
- `required_outputs`: `scene_master`

### Midjourney

#### scene_master

```text
校长办公室, 学院权威视角观察异象的室内反应场景。, formal academy office interior, large observation window toward campus, heavy desk and academy crest, dark wood and stone authority materials, readable standing reaction zone near window, VFX_GOLDEN_SKY_ANOMALY, day, indoor, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, readable wide composition, camera coverage seeds: office medium two-shot, principal reaction by window, over-shoulder to campus anomaly, not photoreal --ar 16:9 --v 7 --raw
```

### Banana Pro

#### layout_cleanup

```text
保留校长办公室的空间布局、透视、锚点和光照不变，只清理错误结构与不稳定细节，使它成为后续镜头可复用的稳定母图。
```

## `LOC_ACADEMY_CAFETERIA`

### Summary

- `status`: planned
- `required_outputs`: `scene_master`、`reverse_seed`

### Midjourney

#### scene_master

```text
食堂, 第2集分手羞辱戏的高人流校园室内场景。, academy cafeteria interior, long table rows, noisy student background layer, corner seat isolation zone for Mengjiang, serving counter depth, , day, indoor, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, readable wide composition, camera coverage seeds: corner isolation medium shot, confrontation two-shot, crowd reaction cutaway, not photoreal --ar 16:9 --v 7 --raw
```

#### reverse_seed

```text
same 食堂, reverse-side view of the same space, preserve long table rows, noisy student background layer, corner seat isolation zone for Mengjiang, serving counter depth, preserve layout logic, same day, indoor, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still --ar 16:9 --v 7 --raw --oref [ACADEMY_CAFETERIA_MASTER] --ow 200
```

### Banana Pro

#### layout_cleanup

```text
保留食堂的空间布局、透视、锚点和光照不变，只清理错误结构与不稳定细节，使它成为后续镜头可复用的稳定母图。
```

## `LOC_PUBLIC_DRAW_POOL_NIGHT`

### Summary

- `status`: prompted
- `required_outputs`: `scene_master`、`reverse_seed`

### Midjourney

#### scene_master

```text
夜间公共抽卡广场, 第3集夜间哪吒异象与第二个压力测试样片主场景。, public draw pool plaza at night, isolated draw pool pedestal, dark open plaza, distant city glow, readable empty space for hero solo shot, PROP_DRAW_POOL_MAIN, CARD_SUMMON_CARD_BASE, VFX_RED_SKY_ANOMALY, VFX_RED_LIGHT_PILLAR, VFX_NEZHA_AVATAR, VFX_NEZHA_WEAPON_SUITE, night, clear night, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, readable wide composition, camera coverage seeds: front night master, low-angle ignition shot, overhead anomaly reveal, not photoreal --ar 16:9 --v 7 --raw
```

#### reverse_seed

```text
same 夜间公共抽卡广场, reverse-side view of the same space, preserve isolated draw pool pedestal, dark open plaza, distant city glow, readable empty space for hero solo shot, preserve layout logic, same night, clear night, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still --ar 16:9 --v 7 --raw --oref [PUBLIC_DRAW_POOL_NIGHT_MASTER] --ow 200
```

### Banana Pro

#### layout_cleanup

```text
保留夜间公共抽卡广场的空间布局、透视、锚点和光照不变，只清理错误结构与不稳定细节，使它成为后续镜头可复用的稳定母图。
```

## `LOC_CITY_REACTION_MONTAGE_NIGHT`

### Summary

- `status`: planned
- `required_outputs`: `scene_master`

### Midjourney

#### scene_master

```text
各处夜景反应蒙太奇, 第3集各方势力抬头观测赤红异象时的拼接场景母板。, city reaction montage night, multiple city reaction windows, skyline under red anomaly, split coverage logic for authority, dorm, and family reactions, VFX_RED_SKY_ANOMALY, night, anomaly-lit night, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, readable wide composition, camera coverage seeds: montage establishing plate, city skyline reaction cutaway, not photoreal --ar 16:9 --v 7 --raw
```

### Banana Pro

#### layout_cleanup

```text
保留各处夜景反应蒙太奇的空间布局、透视、锚点和光照不变，只清理错误结构与不稳定细节，使它成为后续镜头可复用的稳定母图。
```

## `LOC_DORM_WINDOW_NIGHT`

### Summary

- `status`: planned
- `required_outputs`: `scene_master`

### Midjourney

#### scene_master

```text
宿舍窗景, 林倩倩夜间望向异象的高层宿舍窗景。, academy dorm window interior, tall dorm window, female silhouette reaction zone, visible distant red anomaly outside, VFX_RED_SKY_ANOMALY, night, anomaly-lit night, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, readable wide composition, camera coverage seeds: window profile reaction, interior to exterior over-shoulder, not photoreal --ar 16:9 --v 7 --raw
```

### Banana Pro

#### layout_cleanup

```text
保留宿舍窗景的空间布局、透视、锚点和光照不变，只清理错误结构与不稳定细节，使它成为后续镜头可复用的稳定母图。
```

## `LOC_ZHANG_RESIDENCE_TERRACE`

### Summary

- `status`: planned
- `required_outputs`: `scene_master`

### Midjourney

#### scene_master

```text
张家露台, 张贺与张强观测夜间异象的家族露台或外窗场景。, elite residence terrace night, elite residence exterior edge, elevated view toward city sky, father-son reaction position, VFX_RED_SKY_ANOMALY, night, anomaly-lit night, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, readable wide composition, camera coverage seeds: terrace medium two-shot, skyline reaction side view, not photoreal --ar 16:9 --v 7 --raw
```

### Banana Pro

#### layout_cleanup

```text
保留张家露台的空间布局、透视、锚点和光照不变，只清理错误结构与不稳定细节，使它成为后续镜头可复用的稳定母图。
```
