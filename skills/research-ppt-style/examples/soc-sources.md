# SOC示例的来源、映射与演练依据（不口播）

论文：Limin Yang et al., *True Attacks, Attack Attempts, or Benign Triggers? An Empirical Measurement of Network Alerts in a Security Operations Center*, USENIX Security 2024, pp.1525–1542。

[官方论文页面](https://www.usenix.org/conference/usenixsecurity24/presentation/yang-limin)。本例依据用户提供的官方PDF内容核验，SHA256为5370116654815a819ab35bff01573234087733b07b0c2d7b75c2ee35dfab797d。图表/原PDF未随包再分发。本例为新写的中文转述，不代表作者原始演讲。

| 口播页 | 来源 | 必须保留的口径 |
| --- | --- | --- |
| 1–4 | 首页、§1–3、Figure 1 | SOC流程与测量设计不同；RQ承担问题与困难；目录只导航；英文图按实际标签/分支定位 |
| 5 | §3、§5、Table 3 | 两段日志而非连续4年；227已知事件，11重叠；网络源下界 |
| 6 | Table 1、§6.2/6.4、Appendix C | 良性触发不同于一般FP；保守判定；unknown非安全 |
| 7 | §4、Figure 2 | 1,101为案例相关网络记录；初始阶段无网络告警；一例不外推 |
| 8 | Table 3、§6.1、Figure 8 | 两时期日均；后期BHR44.9%；13,764为记录余量非工时 |
| 9 | Tables 4/7、§6.2/6.4 | 分母14,429,534；0.01%为告警条数占比；来源可重叠 |
| 10 | §6.3、Figures 9–12 | 573为累计活动日；66.22%为合格连接子集启发式，非独立真值 |
| 11 | §7.1、Table 8 | ID4/6日志缺失；ID1无关；7/4渠道不当召回率；Total含相关记录 |
| 12 | §7.2、Figure 13 | (a)10，(b)10/11，(c)9/10/11；3案例探索，无检测性能验证 |
| 13 | §5、Table 2、§7.3、§8.2、Appendices A/B | 107人力记录，28历时记录；53.2天非工时；建议与落地/收益分开 |
| 14 | §3、§8.3及对应子分析 | 单SOC、网络范围、旧时段、不完备及观察性边界 |
| 15 | 汇报者归纳，依据§3、6–8 | 方法迁移是归纳，不声称作者跨场景实验 |
| 16 | 前述已介绍证据 | 不在结尾新增结果或扩大结论 |

第4段用用户确认的PPT问题全句作一种措辞参考，所有子问和程度/关联或指示/真实成功范围完整。当前统一规则先全文连贯与讲懂，允许为理解调整页内讲序和自然句式；在内容相近处尽可能贴近清楚顺口原话，不要求所有任务按此顺序或字字相同。原义、合法重排与删漏反例见 [rq-fidelity.md](rq-fidelity.md)。技能内例子没有写入用户PPT或演讲稿MD。

## 第9页八行直接映射

| 展示行 | Table 7原项 | 条数 |
| --- | --- | ---: |
| 外部渗透测试/合规审计 | External Pen-test / Various alerts | 2,694,851 |
| Zeek日志记录故障 | Non-Attack / Logging failure | 2,553,794 |
| 外部域名指向本地IP | DNS / External domain w/ local IP | 1,407,151 |
| 内部合法扫描 | Internal Scan / Legitimate scan | 194,518 |
| 新增IP地址空间 | Non-Attack / New IP address space | 138,630 |
| SSL弱密钥 | SSL / Weak key | 30,570 |
| 外部DNS服务器 | DNS / External DNS server | 28,698 |
| 例外服务 | Services w/ Exceptions / Various alerts | 260 |

这八项是选列原表细项，不是Table 7的完整列表或互斥分类。新主机3条另列未画，其他DNS/SSL项未画。良性触发并集7,057,012不能由选列项求和推导。原型的138,893混合了138,630、3与另列260，无法据此认定并集，示例移除该聚合。最小条可只标数值，不设置人为最短条长。

Table 4与Remark 6的unknown百分比存在原文差异，本例依Table 4的23.72%及计数。稀有度正文与图轴的聚合命名差异仍保留为审校疑点，不补造平均分母。连接阈值的原文表达差异也未在口播中硬定。

## 作者与伦理备查（不逐项口播）

作者来自UIUC、NCSA和IBM Research；姓名/贡献及组织按论文首页核对。作者履历和导师关系不由机构名推断，本例不依赖这些信息。论文的数据合作、标注/归因/关联工作解释了研究价值，口播第2段只保留相关的一小部分。

伦理与公开性依据§3/§8.3：论文报告伦理审查，公开项目代码和一份Postgres案例月份的脱敏样本；不是全部两段日志和私有报告的开放数据。此处备查，避免把IRB/匿名化/代码细节全部堆进短作者页口播。

## 英文图定位核验

第4段按实际Figure 1和参考渲染核对：左侧Inputs中Network、Endpoints/Hosts、Honeypot、Blocklists/Threat Intel；网络分支经Black Hole Router (BHR)到SIEM (Splunk)，其他来源汇聚；向右是Threat triage, Detection, Response和Post-attack Forensics；上下反馈分别为New Insights/New insights。不是所有输入的单一直线pipeline。

第8段定位Date、# of Alerts in Millions、All/Blocked。第10段定位Number of Active Days/CDF of Attacker IPs和Number of Victim IPs/Cumulated % of Alerts。第12段按(a)(b)(c)定位Entropy of Daily Alert Volume、Entropy of Alert Sequence、Alert Rareness Per Host Per Day、CDF of Hosts及实际图例/案例ID。与参考图的字面标签和位置核对后才加入正文；稀有度正文/轴命名的原文差异仍按上面的边界处理。

## 时长参数与验收状态

本案例的听众和时间配置见 [task-profile.json](task-profile.json)：包括入门学生与专业评审，全场18分钟以内；建议正文计划16分钟、留2分钟缓冲，第2页局部目标不超过40秒。这些是本案要求/建议，不是全部用户默认值。16段教学稿按早期页号组织，不替代用户最新MD/PPT，也不能凭此称当前实际汇报已完成时长验收。

文本字符估算见 [timing.json](timing.json)，去掉标题和Markdown加粗标记，假设每分钟260–320个中文及其他非空白字符，另加1.5–3分钟给指图、英文/数字和停顿。英文标签增加的定位价值与朗读耗时一起考虑，不机械换算为中文读音。粗估上界超过本案总时长时明确标记尚未满足，不取中点假称通过；先精简重复文字/次要支线，图表和必要限定仍保留，再实际演练。

第2段的文字粗估和额外停顿也单列在timing.json，不是实测40秒。当前只做连续文本审读，未进行真人计时演练、听众理解测试或PowerPoint/WPS现场显示验收。当前案例角色及唯一写入者配置只是参数示范，不强迫新任务建立相同session。最新MD手改及图表保护按实际工程另验收，本轮没有修改该工程。
