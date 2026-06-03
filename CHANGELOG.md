# 更新日志 / Changelog

AgentInsight Python SDK 的所有重要变更将记录在此文件中。

All notable changes to the AgentInsight Python SDK will be documented in this file.

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，本项目遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-02

### 新增 / Added

- AgentInsight Python SDK 初始版本发布 / Initial release of AgentInsight Python SDK
- AgentInsight 可观测性平台的 Python 客户端 / Python client for the AgentInsight observability platform
- `@observe` 装饰器，自动追踪函数调用 / `@observe` decorator for automatic function tracing
- 通过 `agentinsight.openai` 的 OpenAI 集成（猴子补丁方式）/ OpenAI integration via `agentinsight.openai` (monkey-patching)
- 通过 `CallbackHandler` 的 LangChain 集成 / LangChain integration via `CallbackHandler`
- 9 种观察类型：span、generation、agent、tool、chain、embedding、evaluator、retriever、guardrail / 9 observation types: span, generation, agent, tool, chain, embedding, evaluator, retriever, guardrail
- 评分系统，支持 NUMERIC、BOOLEAN 和 CATEGORICAL 类型 / Scoring system supporting NUMERIC, BOOLEAN, and CATEGORICAL types
- 通过 `propagate_attributes` 和 OpenTelemetry Baggage 的上下文传播 / Context propagation via `propagate_attributes` and OpenTelemetry Baggage
- Prompt 管理，支持版本控制和模板编译 / Prompt management with version control and template compilation
- 数据集管理和实验/评估框架 / Dataset management and experiment/evaluation framework
- 通过 `ContextVar` 的多项目隔离 / Multi-project isolation via `ContextVar`
- 批量 span 导出，可配置刷新设置 / Batch span export with configurable flush settings
- 媒体上传和评分摄入的后台线程 / Background threads for media upload and score ingestion
- `AGENTINSIGHT_*` 环境变量配置 / `AGENTINSIGHT_*` environment variable configuration
- 通过 pdoc 生成的 SDK 参考文档 / SDK reference documentation generated via pdoc
- 示例目录及使用示例 / Examples directory with usage samples
- SECURITY.md 安全策略 / SECURITY.md security policy
- CODE_OF_CONDUCT.md

### 致谢 / Acknowledgements

本项目基于 [Langfuse Python SDK](https://github.com/langfuse/langfuse-python) 构建并演化而来。

This project is built upon and evolved from the [Langfuse Python SDK](https://github.com/langfuse/langfuse-python).

Langfuse Python SDK 本身基于 [PostHog Python SDK](https://github.com/PostHog/posthog-python) 构建。

The Langfuse Python SDK itself is built upon the [PostHog Python SDK](https://github.com/PostHog/posthog-python).
