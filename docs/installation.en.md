# Installation · Beauty Live Handcards

[English README](../README.en.md) · [中文安装说明](installation.md)

## WorkBuddy

1. Open [Release v0.1.0](https://github.com/ouyang-2019/beauty-live-handcards/releases/tag/v0.1.0) and download `beauty-live-handcards-workbuddy-0.1.0.zip`.
2. In the client, open Experts / Skills / Connectors → Skills → Add Skill → Upload Skill. The current Chinese UI labels are “专家·技能·连接器 → 技能 → 添加技能 → 上传技能”.
3. Import the ZIP and enable “美妆直播手卡”. Start a new task, select your product materials directory and choose the skill in the conversation.
4. If the host's image tools/model are not configured, prepare the copy and prompts first, then configure image tools using the host's supported method.

The WorkBuddy archive puts `SKILL.md` at the ZIP root and includes the required author, version and bilingual description fields. Use the WorkBuddy release asset for installation; GitHub's “Download ZIP” downloads the repository rather than this package.

## Codex

Copy the complete `skills/beauty-live-handcards` directory into your user skills directory, for example `~/.codex/skills/beauty-live-handcards`.

Start a new session and invoke `$beauty-live-handcards` or clearly mention the skill name. Back up an existing same-name installation before updating it.

## Other Agent Skills hosts

Install the complete `beauty-live-handcards` directory according to the host's instructions. The generic archive uses Agent Skills metadata. The host supplies the model, visual reading and image generation/editing tools.

## Product inputs and outputs

Keep packaging images, ingredients/formula files, prices and reports in the current project directory. Keep generated artwork and production records there as well. The installed skill directory holds reusable rules, templates and scripts.

The optional `qa_gate.py` script requires Python 3.9+ and uses the standard library. It checks review records and file hashes. Actual artwork still needs to be visually read and reviewed.

## Preview status

The package structure and WorkBuddy file installation have been checked. The five galleries are existing Codex outputs; WorkBuddy image generation remains to be tested.

## Official references

- [WorkBuddy local skill upload](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [WorkBuddy skill fields and structure](https://open.workbuddy.cn/en/docs/skill)
- [Agent Skills specification](https://agentskills.io/specification)

Next: [English prompt examples](usage.en.md).
