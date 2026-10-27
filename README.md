# 研究PPT技能：完整匿名参考版

版本0.1.0-rc8-sanitized（2026-10-27）。两项技能包含最新正文/口播偏好、指图讲述、手改保护与公式检查规则。新增16页SOC完整匿名参考及其逐页原备注，保留研究图表和学术来源；汇报者姓名、单位/学院、报告日期与编辑元数据已清理。原RC7的16页空白模板与通用口播另存保留。

## 安装与使用

| 技能 | 内容 |
| --- | --- |
| [research-ppt-style](skills/research-ppt-style/SKILL.md) | 风格、自然口播、图表/手改保护、公式检查；完整匿名参考及原备注 |
| [artifact-template-soc-ppt](skills/artifact-template-soc-ppt/SKILL.md) | 独立可用的匿名参考母版、空白模板与口播 |

在接收者自己的Codex中发送：

```text
请使用 $skill-installer，从GitHub仓库01Elaine/research-ppt-skills安装：
skills/research-ppt-style
skills/artifact-template-soc-ppt
请保留各自完整资源目录；已有同名技能时先说明，不直接覆盖。
```

或下载仓库ZIP，将两个完整技能目录放入当前客户端识别的用户技能目录；不要只复制SKILL.md，实际安装目录按客户端配置确定。安装后若未识别，重新打开会话或重启客户端。不能把一台机器的安装路径直接用于另一台或云端。

调用示例：

```text
请同时使用 $research-ppt-style 和 $artifact-template-soc-ppt，参考SOC母版制作本次研究汇报。内容以我提供的论文为准，替换示例中的研究数字和身份字段，输出可编辑PPT和对应口播稿。
```

## 参考与口播的版本

- [完整匿名PPT](skills/artifact-template-soc-ppt/assets/reference.pptx)：16页，保留研究图表和原备注，用于理解实际版式及图文关系。
- [逐页原备注](skills/artifact-template-soc-ppt/examples/reference-talk.md)：从本次公开的匿名PPT提取，正文与PPT备注一一对应；不是后续19页工作稿。
- [16页空白模板](skills/artifact-template-soc-ppt/assets/blank-template.pptx)及[通用口播](skills/artifact-template-soc-ppt/examples/template-talk.md)：供新论文替换内容，不含原论文图表。
- [SOC教学转述](skills/research-ppt-style/examples/soc-talk.md)：另一个连续讲述示例，与原备注版本不同，不宣称旧参考稿已经落实后来新增的每条表达偏好。

两项技能均可独立安装。技能不内置PPT编辑引擎；制作、渲染与字体由接收者环境提供。不要将整页预览贴成最终PPT，原图可以保留为研究图片，文字、表格与版式继续可编辑。

## 发布范围

只以本仓库目录发布，不上传父目录中的私人原件、审查资料或构建缓存。公开版含经身份清理的参考副本及原备注，不含用户本机原件、个人身份、私人路径、原论文PDF或字体。论文作者与机构名称是学术归属，不是汇报者的身份信息。

[LICENSE.md](LICENSE.md)仍为许可候选说明，未擅自设为生效MIT许可；匿名参考所含论文图表与网页截图另见[THIRD_PARTY.md](THIRD_PARTY.md)，不纳入候选MIT授权范围。隐私处理见[docs/privacy.md](docs/privacy.md)，验证边界见[docs/validation.md](docs/validation.md)。

Python 3.10+可运行 `python tools/check_package.py .` 做文件结构、资源路径、PPT关系及资产哈希检查。该检查不代替研究事实、视觉、素材授权或接收者环境验收。
