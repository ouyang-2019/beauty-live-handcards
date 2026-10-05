# 安装

## WorkBuddy

1. 打开[Release](https://github.com/ouyang-2019/beauty-live-handcards/releases/tag/v0.1.0)，下载 `beauty-live-handcards-workbuddy-0.1.0.zip`。
2. 在客户端“专家·技能·连接器 → 技能 → 添加技能 → 上传技能”中导入ZIP。
3. 启用“美妆直播手卡”，新建任务并选择当前产品资料目录，在对话中选择技能。
4. 图片工具或模型尚未配置时，先完成文案与提示词准备，再按宿主支持的方法配置工具。

WorkBuddy包把SKILL.md放在ZIP根目录，并提供其要求的中英文描述、作者和版本字段。不要把GitHub仓库整体下载ZIP当作这个技能安装包。

## Codex

将 `skills/beauty-live-handcards` 复制到用户技能目录，例如 `~/.codex/skills/beauty-live-handcards`。在新会话中用 `$beauty-live-handcards` 或明确的技能名称调用。
已有同名版本时保留备份，再按需要更新。

## 其他Agent Skills宿主

按宿主说明，将完整 `beauty-live-handcards` 目录放入其技能目录。通用包使用Agent Skills标准元数据；模型、读图和图片工具由宿主提供。

## 输入目录

包装图、配方、价格和报告放在本次项目工作目录。技能目录存规则和脚本，成品、生产记录与客户资料放在项目工作目录。

## 官方参考

- [WorkBuddy本地上传技能](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [WorkBuddy字段与结构](https://open.workbuddy.cn/en/docs/skill)
- [Agent Skills规范](https://agentskills.io/specification)
