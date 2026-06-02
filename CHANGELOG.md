[English](#english) | [中文](#中文)

---

<a id="english"></a>

# Changelog

All notable changes to the AgentInsight Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-02

### Added

- Initial release of AgentInsight Python SDK
- Python client for the AgentInsight observability platform
- `@observe` decorator for automatic function tracing
- OpenAI integration via `agentinsight.openai` (monkey-patching)
- LangChain integration via `AgentInsightCallbackHandler`
- 9 observation types: span, generation, agent, tool, chain, embedding, evaluator, retriever, guardrail
- Scoring system supporting NUMERIC, BOOLEAN, and CATEGORICAL types
- Context propagation via `propagate_attributes` and OpenTelemetry Baggage
- Prompt management with version control and template compilation
- Dataset management and experiment/evaluation framework
- Multi-project isolation via `ContextVar`
- Batch span export with configurable flush settings
- Background threads for media upload and score ingestion
- `AGENTINSIGHT_*` environment variable configuration
- SDK reference documentation generated via pdoc
- Examples directory with usage samples
- SECURITY.md security policy
- CODE_OF_CONDUCT.md

### Acknowledgements

This project is built upon and evolved from the [Langfuse Python SDK](https://github.com/langfuse/langfuse-python).
The Langfuse Python SDK itself is built upon the [PostHog Python SDK](https://github.com/PostHog/posthog-python).

---

<a id="中文"></a>

# 更新日志

AgentInsight Python SDK 的所有重要变更将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

## [0.1.0] - 2026-06-02

### 新增

- AgentInsight Python SDK 初始版本发布
- AgentInsight 可观测性平台的 Python 客户端
- `@observe` 装饰器，自动追踪函数调用
- 通过 `agentinsight.openai` 的 OpenAI 集成（猴子补丁方式）
- 通过 `AgentInsightCallbackHandler` 的 LangChain 集成
- 9 种观察类型：span、generation、agent、tool、chain、embedding、evaluator、retriever、guardrail
- 评分系统，支持 NUMERIC、BOOLEAN 和 CATEGORICAL 类型
- 通过 `propagate_attributes` 和 OpenTelemetry Baggage 的上下文传播
- Prompt 管理，支持版本控制和模板编译
- 数据集管理和实验/评估框架
- 通过 `ContextVar` 的多项目隔离
- 批量 span 导出，可配置刷新设置
- 媒体上传和评分摄入的后台线程
- `AGENTINSIGHT_*` 环境变量配置
- 通过 pdoc 生成的 SDK 参考文档
- 示例目录及使用示例
- SECURITY.md 安全策略
- CODE_OF_CONDUCT.md

### 致谢

本项目基于 [Langfuse Python SDK](https://github.com/langfuse/langfuse-python) 构建并演化而来。
Langfuse Python SDK 本身基于 [PostHog Python SDK](https://github.com/PostHog/posthog-python) 构建。
