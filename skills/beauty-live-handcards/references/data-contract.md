# 事实记录、质检输入与交付

## 产品事实记录
建议保存在生产目录 product-facts.json，每款独立记录：
- product_id、source_folder、category、brand_cn/brand_en、canonical_name、display_name、approved_aliases。
- brand_reference、packaging_reference：原图路径；standard_text：逐字段标准中文/英文/单位/数值及来源。
- retail_price：value、currency、unit、source_file、sheet、cell、as_of。缺值保存null，不能用0或出厂价代替。
- spec、ingredients（精确名、微量身份、来源）、usage（原文与来源）。
- evidence[]：report_id、file、page、sample_name、match_status、test_type、population、duration、metric、value、unit、direction、conditions、claim_supported。
- efficacy_3d_plan[]：benefit、source_evidence、object、visual_action、leader_target、unsupported_implications。
- missing_fields、source_conflicts、status。
- revision_type、supersedes：本轮是资料改版、质检修复还是复核后保留，以及被替换的版本。

test_type明确使用human、in_vitro、consumer_survey、hair_tress、label_only等，不把样品测试与人体混用。
产品对应关系为unverified时不把报告用于该SKU正式宣称。套装不自动继承单品总价或功效之和。
只有原标签核对后才能把历史modules.json中的名称升级为锁稿事实。

## 质检manifest
下例为虚构字段示范；可复制[模板](../templates/product-manifest.example.json)，须替换为当前产品已核事实。
每个产品一份。路径相对--root；source填写可复查的原文件/页码/单元格。关键字段应覆盖各出现区域，包装中文也单列。不能只抽一处标题就代表全页审过。
```json
{
  "product_id": "sample-product",
  "pages": [
    {
      "page_id": "01",
      "file": "01_单页直播手卡.png",
      "critical_text": [
        {
          "id": "brand-cn",
          "expected": "示例品牌",
          "source": "虚构字段示例；使用时替换为当前品牌原标"
        },
        {
          "id": "name-title",
          "expected": "示例保湿精华",
          "source": "虚构字段示例；使用时替换为当前包装全名"
        },
        {
          "id": "spec",
          "expected": "30ml",
          "source": "虚构规格；使用时替换并核实"
        }
      ]
    }
  ]
}
```
文案若采用合法显示简称或符号，先在锁稿中明确写法，manifest记录图上确实应出现的文字；脚本只忽略排版空白，保留大小写、符号和小数精度。OCR读出异体字时回看图，不篡改标准字来迎合识别结果。

## review记录
init自动生成空记录；真实审阅后填写：
- reviewer、带时区reviewed_at（ISO8601）。
- critical_text每项observed（实际逐字读到的内容）、review_method（manual或ocr+visual）、source_verified（true仅表示已实查来源）。
- ocr+visual时另填ocr_evidence（真实工具结果/保存路径）；无OCR填manual。
- visual_checks每项status与具体notes。只有packaging、efficacy_visual可not_applicable且需原因；Logo、名称、文字、证据和构图必审。
- issues每项severity（critical/major/minor）、status（open/resolved）、description、region、resolution（解决后必填复核依据）。
哈希由init产生。改图或改manifest后创建新review，重新查看；不手改哈希逃过新鲜度检查。
script仅验证记录，不能证明审阅实际发生；填写合格结论不得依据脚本生成。

## 状态与恢复
queued → facts_ready → copy_locked → generated → qa_review → needs_repair / qa_passed → delivered。
approval/design_approved单独记录，不等同qa_passed。旧样稿即使用户认可，新增质检上线后仍可需复检。
项目进度表逐款记录：素材位置、缺资料、已生成页、缺页、QA状态、最新目录、下一步。
缺价只阻塞价格字段，先完成其他页；缺同款报告则跳过报告宣称。素材模糊、工具失败时保留清单继续可做产品，不伪造缺失项。

## 输出与同步
产品目录保留有序PNG和整套PDF；QA/提示词/源据放生产资料；报告原件可共享目录。
旧版本保留。改图后同步预览与ZIP，避免交付包仍是旧版本。检查文件存在、可解码、页数正确、没有重复旧版文件、ZIP可完整读取。
交付说明写真实范围、实际尺寸、待补资料与未通过项目；不得声称没做过的自动OCR、逐字/视觉审阅。

最终文件记录建议包括 `file`、`sha256`、`pixels`、`production_method`、`native_source`、`archive_copy`、`reviewed_sha256`、`review_status`、`pdf_page`。文档排版页用 `source_pdf_pages` 记录输入。`native_source` 是工具实际返回的源路径，备份另列；文件校验不能取代人工审图。批量改版与最终打包详见revision-playbook.md。
