# 美妆直播手卡 · Beauty Live Handcards

把产品资料变成主播能直接讲、顾客能快速读懂的单页手卡、功效套图和组合卡。

[English](README.en.md) · [下载 v0.1.0 安装包](https://github.com/ouyang-2019/beauty-live-handcards/releases/tag/v0.1.0) · [安装说明](docs/installation.md) · [五套产品案例](examples/README.md)

适用于美妆品牌、直播团队、电商运营和设计人员。围绕使用场景与明星原料组织卖点，用具体的摄影和3D动作解释产品，同时核对中文、包装与报告归属。

## 能做什么

- 单页直播手卡：包装主视觉、场景、一句话卖点、原料讲解、规格价格与用法。
- 整套产品图：主视觉、功效3D、原料、检测报告与使用讲解，按资料和要求选择模块。
- 组合手卡：讲清每个单品的作用和搭配顺序。
- 已有图片改版：更新配方、报告和正文，复核后同步PNG、PDF与ZIP。
- 推广表达：正文突出亮点，数字旁标注指标和必要条件；内部审核备注留在制作资料。

## 快速开始

**WorkBuddy**：从[Release](https://github.com/ouyang-2019/beauty-live-handcards/releases/tag/v0.1.0)下载 `beauty-live-handcards-workbuddy-0.1.0.zip`，在“技能 → 添加技能 → 上传技能”导入并启用。

**Codex及其他支持Agent Skills的宿主**：使用 `skills/beauty-live-handcards` 目录或Release中的Agent Skills安装包。详见[各宿主安装方法](docs/installation.md)。

准备真实包装图、成分/配方、价格表和匹配的功效报告，然后使用：

```text
使用 beauty-live-handcards，读取我提供的两个产品资料。
每个产品制作1张单页直播手卡，再制作1张双品综合手卡，共3张独立PNG。
正文突出使用场景、原料特色和检测亮点，数据采用指标与条件简注。
保留真实包装、Logo、产品名与规格，检查中文和数据。
输出到本次工作目录的“手卡输出”文件夹。
```

更多请求见[提示词示例](docs/usage.md)。

## 五套产品展示

37张成品原图已公开，展示“香莱可人”和“漾皑秀”的不同产品视觉与讲解方式。

### 香莱可人·重组胶原蛋白次抛精华液

甘油与可溶性胶原的水润护理，次抛使用场景，配方原料与对应检测展示。

[查看完整 9 张案例](examples/01-serum/README.md)

![香莱可人·重组胶原蛋白次抛精华液](examples/01-serum/01.png)

### 香莱可人·青春紧致淡纹精华霜

乳木果脂、羟丙基四氢吡喃三醇与神经酰胺NP的原料分工，柔润肤感与日常护理收尾。

[查看完整 7 张案例](examples/02-cream/README.md)

![香莱可人·青春紧致淡纹精华霜](examples/02-cream/01.png)

### 漾皑秀·璀璨奢养玉肌护手礼盒

四支一盒的护手搭配，把香型、原料和洗手后的护理场景连起来。

[查看完整 7 张案例](examples/03-hand-care-gift-set/README.md)

![漾皑秀·璀璨奢养玉肌护手礼盒](examples/03-hand-care-gift-set/01.png)

### 漾皑秀·蓝铜肽雪肌舒缓水光面膜

冰蓝水光视觉，水润贴敷、舒缓与抗皱紧致护理主题，原料矩阵和对应报告展示。

[查看完整 7 张案例](examples/04-blue-copper-mask/README.md)

![漾皑秀·蓝铜肽雪肌舒缓水光面膜](examples/04-blue-copper-mask/01.png)

### 漾皑秀·黑钻赋活光感驻颜面膜

黑金产品视觉，润泽贴敷体验与原料、用法的完整讲解。

[查看完整 7 张案例](examples/05-black-diamond-mask/README.md)

![漾皑秀·黑钻赋活光感驻颜面膜](examples/05-black-diamond-mask/01.png)

## 运行与验证状态

- 图片生成、参考图编辑与视觉读取由使用者的宿主和模型提供，技能本身提供规则与流程。
- 可选质检记录脚本使用Python 3.9+标准库。
- 五套案例来自本项目既有Codex成稿。WorkBuddy技能文件安装与结构已验证，客户端实际出图仍待测试。
- `qa_gate.py`核对审阅记录和文件哈希；中文和视觉结论需要实际读图。
- [构建与检查](docs/development.md)记录如何生成安装包和运行本地检查。

## 版本与反馈

当前版本为**v0.1.0公开预览版**。欢迎通过[Issues](https://github.com/ouyang-2019/beauty-live-handcards/issues)提交输入类型、宿主/模型、问题图片和预期结果，帮助改进原料讲解、包装还原与中文排版。

## 许可

技能规则、脚本、模板和使用文档采用[MIT](LICENSE)许可，任何人可使用和改进。
产品案例图片与品牌标识按[案例图片使用范围](examples/LICENSE.md)展示。完整范围见[NOTICE](NOTICE.md)。

## 发布结构参考

参考[Anthropic Skills](https://github.com/anthropics/skills)的独立skill目录和按需参考资料、[Superpowers](https://github.com/obra/superpowers)的分宿主安装说明，以及[WorkBuddy Skill Atlas](https://github.com/sandbaseai/workbuddy-skill)的版本ZIP和校验文件方式。项目遵循[Agent Skills结构](https://agentskills.io/specification)，WorkBuddy包按其[官方字段要求](https://open.workbuddy.cn/en/docs/skill)构建。
