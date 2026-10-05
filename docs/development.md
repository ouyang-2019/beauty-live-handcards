# 构建与检查

Python 3.9+，仅使用标准库。

```text
python tools/validate_repo.py
python tools/build_release.py
```

通用技能源只维护在 `skills/beauty-live-handcards`。
构建器为WorkBuddy添加宿主所需顶层元数据，生成通用ZIP、WorkBuddy ZIP、产品案例ZIP与SHA256SUMS。
构建输出位于 `dist/`，作为GitHub Release附件发布。

检查范围：技能元数据、内部链接、发布文件范围、案例原图哈希与尺寸、文件大小、打包ZIP及质检脚本帮助命令。
案例图片来自既有成稿；这组检查不证明重新完成了视觉审核或WorkBuddy实际生图。

验证真实行为时先用三张试稿，记录实际模型、工具、输出尺寸和问题，再据此修订。不要把README里的展示案例数据复制到新的产品。
