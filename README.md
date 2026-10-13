# 研究PPT技能：完整结构公开版

版本0.1.0-rc7-public（2026-10-14）。本包提供完整16页可编辑公开模板：封面、作者页、目录、研究问题、总体方法、证据、启示、局限、方法论借鉴和结语。保留白底蓝灰风格与叙事规范，个人身份和原论文内容使用明确占位。

## 安装与使用

| 技能 | 入口与资源 |
| --- | --- |
| 通用风格与连续口播 | [research-ppt-style](skills/research-ppt-style/SKILL.md)，自带完整模板与通用口播 |
| 可选模板技能 | [artifact-template-soc-ppt](skills/artifact-template-soc-ppt/SKILL.md)，可独立安装 |

把所需skill文件夹整体复制到当前客户端的技能目录，保留assets、references、examples和agents；不只复制SKILL.md。已有同名skill先备份，再按使用者要求更新。Codex通常使用个人目录下的.codex/skills，实际位置也可由CODEX_HOME配置。云端工具需要接收文件附件，不能凭本机路径读取资源。

模板入口：[reference.pptx](skills/artifact-template-soc-ppt/assets/reference.pptx)。匹配16页模板的通用口播：[template-talk.md](skills/research-ppt-style/examples/template-talk.md)。另有 [SOC教学口播](skills/research-ppt-style/examples/soc-talk.md)，它是公开论文的独立转述，不是个人原稿，也不与占位页面的示意数字混为研究事实。

调用示例：
> 使用 $research-ppt-style，阅读我提供的论文，参考完整公开模板制作研究汇报。按本次听众和时长组织问题、总体方法与证据，替换占位内容，输出可编辑PPT与对应口播。完整参考不要求固定16页。

> 使用 $artifact-template-soc-ppt，先检查完整模板，从封面、作者页、目录和研究内容版式中选择需要的页。补齐真实来源、图表、数据与身份信息，再连续通读口播并渲染检查。

## 上传范围

只将本目录作为Git仓库内容，或使用由它生成的RC7-public ZIP；不要上传父目录。此包不含个人原PPT、个人口播、原论文图表、网页截图、原件预览、私人路径、编辑者属性或旧Git历史。所有预览来自当前公开占位模板。

文件内容清理与许可选择是分别记录的事项。自写规则、文档、脚本及占位版式的许可方案见 [LICENSE.md](LICENSE.md)，来源与素材范围见 [THIRD_PARTY.md](THIRD_PARTY.md)。本仓库分发完整结构公开模板，许可证仍保留候选方案，不将待确认的许可写成已经生效。

可选检查：Python 3.10+标准库运行 `python tools/check_package.py .`。两项skill不依赖另一项或制作者本机路径；PPT编辑与外观检查需要使用者自己的工具。模板画廊和客户端安装没有在接收者环境现场验证。字体未嵌入或分发。

清理范围见 [docs/privacy.md](docs/privacy.md)，验证范围见 [docs/validation.md](docs/validation.md)。
