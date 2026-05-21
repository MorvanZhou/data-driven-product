# Google Analytics & Search Console 网站改进技能

[English](README.md)

一个 AI 代理技能，执行目标驱动的网站分析 — 从 Google Search Console 和 GA4 采集数据，审计 SEO/GEO 就绪度，生成带数据可视化的优先级改进方案。

## 功能概述

给你的 AI 代理一个网站 URL，它会：

1. **理解网站目标** — 访问网站，定义预期用户旅程
2. **采集搜索和分析数据** — 通过 GSC 和 GA4 API（或手动导出 CSV）
3. **分析用户偏离点** — 将搜索关键词和用户行为与目标对照
4. **审计线上站点** — SEO 元数据、GEO（AI 搜索）就绪度、性能、安全
5. **生成优先级报告** — P0-P3 行动项，附图表和执行路线图

### 核心理念

**目标 → 数据 → 差距 → 行动**

所有分析都从网站期望用户做什么出发。技能找到现实偏离预期的地方，告诉你该修什么。

## 安装

```bash
npx skills add morvanzhou/data-driven-product
```

## 快速开始

告诉你的 AI 代理：

> 使用 data-driven-product 技能分析 example.com

代理会引导你完成配置，并自动执行完整分析。

### 数据采集模式

| 模式 | 配置 | 适用场景 |
|------|------|----------|
| **API 自动采集**（推荐）| Google Cloud Service Account（首次约 10 分钟）| 完整分析，数据最全 |
| **手动导出 CSV** | 无需配置 | 用导出数据快速分析 |
| **仅浏览器审计** | 无需配置 | 不需要分析数据的技术 SEO/GEO 审计 |

### API 配置（模式 A）

1. 创建 Google Cloud 项目，启用 **Search Console API**、**Analytics Data API** 和 **PageSpeed Insights API**
2. 创建 Service Account，下载 JSON 密钥
3. 授权访问：在 GSC 和 GA4 中添加 SA 邮箱为查看者
4. 告诉代理你的密钥文件路径、GSC 网站地址和 GA4 Property ID

> **提示**：GSC 有两种资源类型 — 网域（`sc-domain:example.com`）和网址前缀（`https://example.com`）。填错格式会导致 403 错误。

详细配置步骤见 [references/gsc-api-guide.md](skills/data-driven-product/references/gsc-api-guide.md)。

## 分析工作流

```
Phase 0  →  网站画像 & 目标定义
Phase 1  →  数据采集（API / CSV / 仅浏览器）
Phase 2  →  搜索表现分析（GSC）
Phase 3  →  用户行为分析（GA4）
Phase 3b →  漏斗探索（可选，自定义事件）
Phase 4  →  线上站点审计（性能、SEO、安全）
Phase 5  →  源代码审查（可选）
Phase 5b →  SEO & GEO 优化清单
Phase 6  →  目标对齐的改进报告 + 图表
```

## 输出

技能在 `.skills-data/data-driven-product/` 下生成完整的分析产出：

- **`analysis/improvement-report.md`** — 最终报告，含执行摘要、目标达成状态、P0-P3 优先行动项、执行路线图
- **`analysis/`** — 各阶段详细报告（搜索分析、行为分析、漏斗分析、站点审计、SEO/GEO 清单）
- **`charts/`** — 数据可视化图表（PNG），嵌入到报告中

## 协作技能

| 技能 | 用途 |
|------|------|
| `seo-geo` | 实施报告中的 SEO/GEO 优化建议 |
| `agent-browser` | 浏览器自动化，用于网站审计 |
| `frontend-design` | 实施前端/UX 改进 |

## 许可证

MIT
