[English](#english) | [中文](#中文)

---

<a id="english"></a>

# AgentInsight Python SDK Examples

This directory contains usage examples for the AgentInsight Python SDK to help you get started with various features.

## Prerequisites

Install the AgentInsight Python SDK:

```bash
pip install agentinsight-sdk
```

## Environment Variables

Before running the examples, set the following environment variables:

```bash
export AGENTINSIGHT_PUBLIC_KEY="pk-xxx"
export AGENTINSIGHT_SECRET_KEY="sk-xxx"
export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
```

Some examples require additional dependencies:

```bash
# OpenAI integration examples
pip install openai

# LangChain integration examples
pip install langchain langchain-openai
```

## Example List

| File | Description |
|------|-------------|
| `basic_usage.py` | Basic tracing: client initialization, @observe decorator, Span/Generation creation, scoring |
| `openai_integration.py` | OpenAI integration: automatic ChatCompletion tracing, streaming responses, prompt association |
| `langchain_integration.py` | LangChain integration: CallbackHandler configuration, Chain/Agent tracing, trace attribute propagation |
| `prompt_management.py` | Prompt management: get/create prompts, compile templates, version control, cache configuration |
| `evaluation.py` | Evaluation system: define evaluation functions, run experiments, multi-metric evaluation, run-level evaluation |
| `context_propagation.py` | Context propagation: propagate_attributes usage, cross-service propagation, Baggage mechanism |

## Running Examples

```bash
# Run a single example
python examples/basic_usage.py

# Run OpenAI integration example (requires OPENAI_API_KEY or Ollama)
python examples/openai_integration.py

# Run LangChain integration example (requires LangChain dependencies)
python examples/langchain_integration.py
```

## Core Concepts

### Three Integration Methods

1. **Direct SDK**: Use the `AgentInsight` client and `start_as_current_observation` / `start_observation` to manually create Spans
2. **@observe Decorator**: Use the `@observe()` decorator to automatically trace functions, supporting nested calls with automatic parent-child relationships
3. **Framework Integration**: Automatically trace third-party framework calls via `agentinsight.openai` or `agentinsight.langchain`

### Observation Types

| Type | Description | Use Case |
|------|-------------|----------|
| `span` | General Span | Any operation tracing |
| `generation` | LLM generation | Record model calls, supports model/usage/cost |
| `agent` | Agent | Agent decision-making and execution |
| `tool` | Tool call | Tool function tracing |
| `chain` | Chain call | Multi-step workflows |
| `retriever` | Retriever | RAG retrieval operations |
| `embedding` | Embedding | Vectorization operations |
| `evaluator` | Evaluator | Evaluation function tracing |
| `guardrail` | Guardrail | Safety check tracing |

---

<a id="中文"></a>

# AgentInsight Python SDK 示例

本目录包含 AgentInsight Python SDK 的使用示例，帮助你快速上手各种功能。

## 前置条件

安装 AgentInsight Python SDK：

```bash
pip install agentinsight-sdk
```

## 环境变量

运行示例前，请设置以下环境变量：

```bash
export AGENTINSIGHT_PUBLIC_KEY="pk-xxx"
export AGENTINSIGHT_SECRET_KEY="sk-xxx"
export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
```

部分示例需要额外依赖：

```bash
# OpenAI 集成示例
pip install openai

# LangChain 集成示例
pip install langchain langchain-openai
```

## 示例列表

| 文件 | 说明 |
|------|------|
| `basic_usage.py` | 基础追踪：客户端初始化、@observe 装饰器、Span/Generation 创建、评分 |
| `openai_integration.py` | OpenAI 集成：自动追踪 ChatCompletion、流式响应、Prompt 关联 |
| `langchain_integration.py` | LangChain 集成：CallbackHandler 配置、Chain/Agent 追踪、trace 属性传递 |
| `prompt_management.py` | Prompt 管理：获取/创建 Prompt、编译模板、版本控制、缓存配置 |
| `evaluation.py` | 评估系统：定义评估函数、运行实验、多指标评估、运行级别评估 |
| `context_propagation.py` | 上下文传播：propagate_attributes 用法、跨服务传播、Baggage 机制 |

## 运行示例

```bash
# 运行单个示例
python examples/basic_usage.py

# 运行 OpenAI 集成示例（需要 OPENAI_API_KEY 或 Ollama）
python examples/openai_integration.py

# 运行 LangChain 集成示例（需要 LangChain 依赖）
python examples/langchain_integration.py
```

## 核心概念

### 三级集成方式

1. **直接 SDK**：使用 `AgentInsight` 客户端和 `start_as_current_observation` / `start_observation` 手动创建 Span
2. **@observe 装饰器**：使用 `@observe()` 装饰器自动追踪函数，支持嵌套调用自动建立父子关系
3. **框架集成**：通过 `agentinsight.openai` 或 `agentinsight.langchain` 自动追踪第三方框架调用

### 观察类型

| 类型 | 说明 | 使用场景 |
|------|------|---------|
| `span` | 通用 Span | 任意操作追踪 |
| `generation` | LLM 生成 | 记录模型调用，支持 model/usage/cost |
| `agent` | 智能体 | Agent 决策和执行 |
| `tool` | 工具调用 | 工具函数追踪 |
| `chain` | 链式调用 | 多步骤流程 |
| `retriever` | 检索器 | RAG 检索操作 |
| `embedding` | 嵌入 | 向量化操作 |
| `evaluator` | 评估器 | 评估函数追踪 |
| `guardrail` | 护栏 | 安全检查追踪 |
