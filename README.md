[English](#english) | [中文](#中文)

---

<a id="english"></a>

![AgentInsight GitHub Banner](https://agent.goldebridge.com/agentinsight_logo.svg)

# AgentInsight Python SDK

[![MIT License](https://img.shields.io/badge/License-MIT-red.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![CI test status](https://img.shields.io/github/actions/workflow/status/AgentInsight/agentinsight-python/ci.yml?style=flat-square&label=All%20tests)](https://github.com/AgentInsight/agentinsight-python/actions/workflows/ci.yml?query=branch%3Amain)
[![PyPI Version](https://img.shields.io/pypi/v/agentinsight.svg?style=flat-square&label=pypi+agentinsight)](https://pypi.python.org/pypi/agentinsight)
[![Python Version](https://img.shields.io/pypi/pyversions/agentinsight.svg?style=flat-square&label=python)](https://pypi.python.org/pypi/agentinsight)
[![GitHub Repo stars](https://img.shields.io/github/stars/AgentInsight/agentinsight?style=flat-square&logo=GitHub&label=AgentInsight%2Fagentinsight)](https://github.com/AgentInsight/agentinsight)

## Overview

AgentInsight Python SDK provides a Python client for the [AgentInsight](https://agent.goldebridge.com) platform, supporting LLM application observability, tracing, evaluation, and prompt management. The SDK is built entirely on the [OpenTelemetry](https://opentelemetry.io/) standard and offers three integration methods: **out-of-the-box OpenAI / LangChain auto-instrumentation (recommended)**, the `@observe` decorator, and direct SDK calls.

## Features

- 🤖 **LLM Auto-Instrumentation (Recommended)** — Out-of-the-box OpenAI and LangChain integrations; change a single import line to automatically trace every LLM call, including prompts/completions, token usage, and costs — no business-logic changes required
- 🔍 **Automatic Tracing** — Use the `@observe` decorator to automatically trace function calls, capturing inputs/outputs, latency, and errors
- 📊 **Scoring & Evaluation** — Built-in evaluation framework and batch evaluation system, supporting NUMERIC / BOOLEAN / CATEGORICAL scores
- 🔄 **Context Propagation** — Cross-service context propagation based on OpenTelemetry Baggage
- 📝 **Prompt Management** — Version-controlled prompt management and template compilation
- 📁 **Datasets & Experiments** — Dataset management and A/B experiment framework
- 🛡️ **Multi-Project Isolation** — Client isolation across projects via `ContextVar`, preventing trace data leakage between projects
- ⚡ **High Performance** — Batch span export, background threads for media upload and score ingestion

## Installation

```bash
pip install agentinsight
```

For OpenAI integration, install the OpenAI package additionally:

```bash
pip install agentinsight openai
```

For LangChain integration, install the LangChain packages additionally:

```bash
pip install agentinsight langchain langchain-openai
```

## Quick Start

### 1. Initialize the Client

```python
import agentinsight

agentinsight.init(
    public_key="pk-...",
    secret_key="sk-...",
    base_url="https://agent.goldebridge.com",
)
```

Or configure via environment variables:

```bash
export AGENTINSIGHT_PUBLIC_KEY="pk-..."
export AGENTINSIGHT_SECRET_KEY="sk-..."
export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
```

```python
from agentinsight import AgentInsight

client = AgentInsight()
```

### 2. ★ Recommended: Auto-Instrumentation (OpenAI / LangChain)

The fastest way to gain full LLM observability. With a single import change, AgentInsight automatically instruments every API call — capturing prompts/completions, token usage, cost, latency, and errors — without touching your business logic.

**OpenAI** — just swap the import:

```diff
- import openai
+ from agentinsight.openai import openai
```

```python
from agentinsight.openai import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is AI?"},
    ],
)

print(response.choices[0].message.content)
```

**LangChain** — register the callback handler:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agentinsight.langchain import CallbackHandler

handler = CallbackHandler()

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
])

chain = prompt | llm
result = chain.invoke(
    {"input": "What is AI?"},
    config={"callbacks": [handler]},
)

print(result.content)
```

See the [OpenAI Integration](#openai-integration) and [LangChain Integration](#langchain-integration) sections for full details.

### 3. Use the @observe Decorator

The `@observe` decorator is the simplest way to add tracing to your own functions, automatically capturing inputs, outputs, and latency:

```python
from agentinsight import observe

@observe(name="my-function")
def my_function(query: str) -> str:
    return f"Processed: {query}"

result = my_function("Hello, AgentInsight!")
```

The decorator supports nested calls and automatically establishes parent-child relationships:

```python
from agentinsight import observe

@observe(as_type="agent")
def run_agent(query: str) -> str:
    plan = plan_task(query)
    result = execute_task(plan)
    return result

@observe(as_type="chain")
def plan_task(query: str) -> str:
    return f"Plan for: {query}"

@observe(as_type="tool")
def execute_task(plan: str) -> str:
    return f"Executed: {plan}"

run_agent("Build a web app")
```

### 4. Trace LLM Calls

Use `as_type="generation"` to mark LLM calls, recording model parameters and token usage:

```python
from agentinsight import observe

@observe(as_type="generation")
def call_llm(prompt: str) -> str:
    # Your LLM call here
    return "LLM response"

result = call_llm("What is AI?")
```

You can also use the low-level API to manually manage spans:

```python
from agentinsight import AgentInsight

client = AgentInsight()

with client.start_as_current_observation(
    name="process-query",
    as_type="span",
) as span:
    with span.start_as_current_generation(
        name="generate-response",
        model="gpt-4",
        input={"query": "Tell me about AI"},
        model_parameters={"temperature": 0.7, "max_tokens": 500},
    ) as generation:
        response = "AI is a field of computer science..."
        generation.update(
            output=response,
            usage_details={"prompt_tokens": 10, "completion_tokens": 50},
            cost_details={"total_cost": 0.0023},
        )

client.flush()
```

### 5. Add Scores

Add scores to any span, supporting NUMERIC, BOOLEAN, and CATEGORICAL types:

```python
from agentinsight import observe

@observe()
def my_function(query: str) -> str:
    return f"Processed: {query}"

result = my_function("Hello")

from agentinsight import get_client
client = get_client()

with client.start_as_current_observation(name="scored-task", as_type="span") as span:
    span.score(name="relevance", value=0.95, data_type="NUMERIC")
    span.score(name="is_valid", value=True, data_type="BOOLEAN")
    span.score(name="sentiment", value="positive", data_type="CATEGORICAL")

client.flush()
```

## OpenAI Integration

Automatically trace all OpenAI API calls by changing a single import line:

```diff
- import openai
+ from agentinsight.openai import openai
```

Full example:

```python
from agentinsight.openai import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is AI?"},
    ],
)

print(response.choices[0].message.content)
```

AgentInsight automatically traces:
- All prompts and completions (supports streaming, async, and function calling)
- Request latency
- API errors
- Token usage and costs

## LangChain Integration

Use `CallbackHandler` to trace LangChain chain execution:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agentinsight.langchain import CallbackHandler

handler = CallbackHandler()

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
])

chain = prompt | llm
result = chain.invoke(
    {"input": "What is AI?"},
    config={"callbacks": [handler]},
)

print(result.content)
```

## Context Propagation

Use `propagate_attributes` to set user-level and session-level attributes within a trace, automatically propagating them to all child spans:

```python
from agentinsight import AgentInsight, propagate_attributes

client = AgentInsight()

with client.start_as_current_observation(name="user-workflow", as_type="span") as span:
    with propagate_attributes(
        user_id="user_123",
        session_id="session_abc",
        metadata={"environment": "production", "variant": "a"},
        tags=["production", "v2"],
    ):
        with client.start_as_current_observation(name="llm-call", as_type="generation") as gen:
            pass

client.flush()
```

Cross-service propagation (via HTTP headers):

```python
from agentinsight import propagate_attributes

with propagate_attributes(
    user_id="user_123",
    session_id="session_abc",
    as_baggage=True,
):
    pass
```

## Evaluation System

AgentInsight provides a built-in experiment and evaluation framework:

```python
from agentinsight import AgentInsight, Evaluation

client = AgentInsight()

def my_task(*, input, **kwargs):
    return f"Processed: {input}"

def accuracy_evaluator(*, input, output, expected_output=None, **kwargs):
    if not expected_output:
        return Evaluation(name="accuracy", value=0, comment="No expected output")
    is_correct = output.strip().lower() == expected_output.strip().lower()
    return Evaluation(
        name="accuracy",
        value=1.0 if is_correct else 0.0,
        comment="Correct" if is_correct else "Incorrect",
    )

result = client.run_experiment(
    name="my-experiment",
    data=[
        {"input": "What is 2+2?", "expected_output": "4"},
        {"input": "What is 3+3?", "expected_output": "6"},
    ],
    task=my_task,
    evaluators=[accuracy_evaluator],
)

for item_result in result.item_results:
    print(f"Input: {item_result.item}")
    print(f"Output: {item_result.output}")
    for evaluation in item_result.evaluations:
        print(f"  {evaluation.name}: {evaluation.value}")
```

## Observation Types

The SDK supports 9 observation types, each corresponding to different span semantics:

| Type | Class | Usage |
|------|-------|-------|
| `span` | `AgentInsightSpan` | General workflow step |
| `generation` | `AgentInsightGeneration` | LLM call |
| `agent` | `AgentInsightAgent` | Agent execution |
| `tool` | `AgentInsightTool` | Tool call |
| `chain` | `AgentInsightChain` | Chain call |
| `embedding` | `AgentInsightEmbedding` | Vector embedding |
| `evaluator` | `AgentInsightEvaluator` | Evaluator |
| `retriever` | `AgentInsightRetriever` | Retriever |
| `guardrail` | `AgentInsightGuardrail` | Safety guardrail |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AGENTINSIGHT_PUBLIC_KEY` | Project public key (required) | — |
| `AGENTINSIGHT_SECRET_KEY` | Project secret key (required) | — |
| `AGENTINSIGHT_BASE_URL` | AgentInsight server URL | `https://agent.goldebridge.com` |
| `AGENTINSIGHT_TRACING_ENABLED` | Enable tracing | `True` |
| `AGENTINSIGHT_TRACING_ENVIRONMENT` | Environment identifier | `default` |
| `AGENTINSIGHT_RELEASE` | Release version identifier | — |
| `AGENTINSIGHT_FLUSH_AT` | Batch span export threshold | `512` |
| `AGENTINSIGHT_FLUSH_INTERVAL` | Batch export interval (seconds) | `5` |
| `AGENTINSIGHT_SAMPLE_RATE` | Sample rate (0.0 - 1.0) | `1.0` |
| `AGENTINSIGHT_TIMEOUT` | HTTP request timeout (seconds) | `5` |
| `AGENTINSIGHT_DEBUG` | Debug mode | `False` |
| `AGENTINSIGHT_MEDIA_UPLOAD_ENABLED` | Enable media upload | `True` |
| `AGENTINSIGHT_MEDIA_UPLOAD_THREAD_COUNT` | Media upload thread count | `1` |
| `AGENTINSIGHT_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED` | Decorator I/O capture switch | `True` |
| `AGENTINSIGHT_PROMPT_CACHE_DEFAULT_TTL_SECONDS` | Prompt cache TTL (seconds) | `60` |

### Constructor Parameters

```python
from agentinsight import AgentInsight

client = AgentInsight(
    public_key="pk-...",
    secret_key="sk-...",
    base_url="https://agent.goldebridge.com",
    timeout=5,
    debug=False,
    tracing_enabled=True,
    flush_at=512,
    flush_interval=5.0,
    environment="production",
    release="1.0.0",
    sample_rate=1.0,
    media_upload_thread_count=1,
)
```

## Requirements

- Python >= 3.10, < 4.0

## Documentation

For full documentation, please refer to the [AgentInsight Official Documentation](https://agent.goldebridge.com/docs/sdk/python).

- [Quick Start Guide](https://agent.goldebridge.com/docs/observability/sdk/python/sdk-v3)
- [OpenAI Integration](https://agent.goldebridge.com/docs/integrations/openai)
- [LangChain Integration](https://agent.goldebridge.com/docs/integrations/langchain)
- [Evaluation System](https://agent.goldebridge.com/docs/evaluations)
- [Prompt Management](https://agent.goldebridge.com/docs/prompts)

## Contributing

Please refer to [CONTRIBUTING.md](https://github.com/AgentInsight/agentinsight-python/blob/main/CONTRIBUTING.md) for contribution guidelines.

## Security

Please refer to [SECURITY.md](https://github.com/AgentInsight/agentinsight-python/blob/main/SECURITY.md) for security policy and vulnerability reporting.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Acknowledgements

This project is built upon and evolved from the [Langfuse Python SDK](https://github.com/langfuse/langfuse-python). We thank the Langfuse team for their excellent work. The Langfuse Python SDK is released under the MIT License.

---

<a id="中文"></a>

![AgentInsight GitHub Banner](https://agent.goldebridge.com/agentinsight_logo.svg)

# AgentInsight Python SDK

[![MIT License](https://img.shields.io/badge/License-MIT-red.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![CI test status](https://img.shields.io/github/actions/workflow/status/AgentInsight/agentinsight-python/ci.yml?style=flat-square&label=All%20tests)](https://github.com/AgentInsight/agentinsight-python/actions/workflows/ci.yml?query=branch%3Amain)
[![PyPI Version](https://img.shields.io/pypi/v/agentinsight.svg?style=flat-square&label=pypi+agentinsight)](https://pypi.python.org/pypi/agentinsight)
[![Python Version](https://img.shields.io/pypi/pyversions/agentinsight.svg?style=flat-square&label=python)](https://pypi.python.org/pypi/agentinsight)
[![GitHub Repo stars](https://img.shields.io/github/stars/AgentInsight/agentinsight?style=flat-square&logo=GitHub&label=AgentInsight%2Fagentinsight)](https://github.com/AgentInsight/agentinsight)

## 概述

AgentInsight Python SDK 为 [AgentInsight](https://agent.goldebridge.com) 平台提供 Python 客户端，支持 LLM 应用的可观测性、追踪、评估和 Prompt 管理。SDK 完全构建在 [OpenTelemetry](https://opentelemetry.io/) 标准之上，提供三种集成方式：**OpenAI / LangChain 开箱即用的自动埋点（推荐）**、`@observe` 装饰器、以及直接 SDK 调用。

## 功能特性

- 🤖 **LLM 自动埋点（推荐）** — 开箱即用的 OpenAI 和 LangChain 集成，仅需修改一行 import 即可自动追踪所有 LLM 调用，包含 prompts/completions、token 用量和成本，无需改动业务代码
- 🔍 **自动追踪** — 使用 `@observe` 装饰器自动追踪函数调用，捕获输入/输出、耗时和错误
- 📊 **评分与评估** — 内置评估框架和批量评估系统，支持 NUMERIC / BOOLEAN / CATEGORICAL 评分
- 🔄 **上下文传播** — 基于 OpenTelemetry Baggage 的跨服务上下文传播
- 📝 **Prompt 管理** — 版本控制的 Prompt 管理和模板编译
- 📁 **数据集与实验** — 数据集管理和 A/B 实验框架
- 🛡️ **多项目隔离** — 通过 `ContextVar` 实现多项目场景下的客户端隔离，防止 trace 数据跨项目泄漏
- ⚡ **高性能** — 批量发送 span、后台线程处理媒体上传和评分摄入

## 安装

```bash
pip install agentinsight
```

OpenAI 集成需要额外安装 OpenAI 包：

```bash
pip install agentinsight openai
```

LangChain 集成需要额外安装 LangChain 包：

```bash
pip install agentinsight langchain langchain-openai
```

## 快速开始

### 1. 初始化客户端

```python
import agentinsight

agentinsight.init(
    public_key="pk-...",
    secret_key="sk-...",
    base_url="https://agent.goldebridge.com",
)
```

或者通过环境变量配置：

```bash
export AGENTINSIGHT_PUBLIC_KEY="pk-..."
export AGENTINSIGHT_SECRET_KEY="sk-..."
export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
```

```python
from agentinsight import AgentInsight

client = AgentInsight()
```

### 2. ★ 推荐：自动埋点（OpenAI / LangChain）

获得完整 LLM 可观测性的最快方式。只需修改一行 import，AgentInsight 即可自动埋点每一次 API 调用 —— 捕获 prompts/completions、token 用量、成本、延迟和错误 —— 完全无需改动业务代码。

**OpenAI** —— 仅需替换 import：

```diff
- import openai
+ from agentinsight.openai import openai
```

```python
from agentinsight.openai import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is AI?"},
    ],
)

print(response.choices[0].message.content)
```

**LangChain** —— 注册回调处理器：

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agentinsight.langchain import CallbackHandler

handler = CallbackHandler()

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
])

chain = prompt | llm
result = chain.invoke(
    {"input": "What is AI?"},
    config={"callbacks": [handler]},
)

print(result.content)
```

完整细节请参阅 [OpenAI 集成](#openai-集成) 和 [LangChain 集成](#langchain-集成) 小节。

### 3. 使用 @observe 装饰器

`@observe` 装饰器是为自有函数添加追踪的最简方式，自动捕获函数的输入、输出和耗时：

```python
from agentinsight import observe

@observe(name="my-function")
def my_function(query: str) -> str:
    return f"Processed: {query}"

result = my_function("Hello, AgentInsight!")
```

装饰器支持嵌套调用，自动建立父子关系：

```python
from agentinsight import observe

@observe(as_type="agent")
def run_agent(query: str) -> str:
    plan = plan_task(query)
    result = execute_task(plan)
    return result

@observe(as_type="chain")
def plan_task(query: str) -> str:
    return f"Plan for: {query}"

@observe(as_type="tool")
def execute_task(plan: str) -> str:
    return f"Executed: {plan}"

run_agent("Build a web app")
```

### 4. 追踪 LLM 调用

使用 `as_type="generation"` 标记 LLM 调用，记录模型参数和 token 用量：

```python
from agentinsight import observe

@observe(as_type="generation")
def call_llm(prompt: str) -> str:
    # Your LLM call here
    return "LLM response"

result = call_llm("What is AI?")
```

也可以使用低级 API 手动管理 span：

```python
from agentinsight import AgentInsight

client = AgentInsight()

with client.start_as_current_observation(
    name="process-query",
    as_type="span",
) as span:
    with span.start_as_current_generation(
        name="generate-response",
        model="gpt-4",
        input={"query": "Tell me about AI"},
        model_parameters={"temperature": 0.7, "max_tokens": 500},
    ) as generation:
        response = "AI is a field of computer science..."
        generation.update(
            output=response,
            usage_details={"prompt_tokens": 10, "completion_tokens": 50},
            cost_details={"total_cost": 0.0023},
        )

client.flush()
```

### 5. 添加评分

为任何 span 添加评分，支持 NUMERIC、BOOLEAN 和 CATEGORICAL 类型：

```python
from agentinsight import observe

@observe()
def my_function(query: str) -> str:
    return f"Processed: {query}"

result = my_function("Hello")

from agentinsight import get_client
client = get_client()

with client.start_as_current_observation(name="scored-task", as_type="span") as span:
    span.score(name="relevance", value=0.95, data_type="NUMERIC")
    span.score(name="is_valid", value=True, data_type="BOOLEAN")
    span.score(name="sentiment", value="positive", data_type="CATEGORICAL")

client.flush()
```

## OpenAI 集成

只需修改一行 import，即可自动追踪所有 OpenAI API 调用：

```diff
- import openai
+ from agentinsight.openai import openai
```

完整示例：

```python
from agentinsight.openai import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is AI?"},
    ],
)

print(response.choices[0].message.content)
```

AgentInsight 自动追踪：
- 所有 prompts 和 completions（支持 streaming、async 和 function calling）
- 请求延迟
- API 错误
- Token 用量和成本

## LangChain 集成

使用 `CallbackHandler` 追踪 LangChain 链的执行：

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agentinsight.langchain import CallbackHandler

handler = CallbackHandler()

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
])

chain = prompt | llm
result = chain.invoke(
    {"input": "What is AI?"},
    config={"callbacks": [handler]},
)

print(result.content)
```

## 上下文传播

使用 `propagate_attributes` 在 trace 内设置用户级、会话级属性，自动传播到所有子 span：

```python
from agentinsight import AgentInsight, propagate_attributes

client = AgentInsight()

with client.start_as_current_observation(name="user-workflow", as_type="span") as span:
    with propagate_attributes(
        user_id="user_123",
        session_id="session_abc",
        metadata={"environment": "production", "variant": "a"},
        tags=["production", "v2"],
    ):
        with client.start_as_current_observation(name="llm-call", as_type="generation") as gen:
            pass

client.flush()
```

跨服务传播（通过 HTTP 头部）：

```python
from agentinsight import propagate_attributes

with propagate_attributes(
    user_id="user_123",
    session_id="session_abc",
    as_baggage=True,
):
    pass
```

## 评估系统

AgentInsight 提供内置的实验和评估框架：

```python
from agentinsight import AgentInsight, Evaluation

client = AgentInsight()

def my_task(*, input, **kwargs):
    return f"Processed: {input}"

def accuracy_evaluator(*, input, output, expected_output=None, **kwargs):
    if not expected_output:
        return Evaluation(name="accuracy", value=0, comment="No expected output")
    is_correct = output.strip().lower() == expected_output.strip().lower()
    return Evaluation(
        name="accuracy",
        value=1.0 if is_correct else 0.0,
        comment="Correct" if is_correct else "Incorrect",
    )

result = client.run_experiment(
    name="my-experiment",
    data=[
        {"input": "What is 2+2?", "expected_output": "4"},
        {"input": "What is 3+3?", "expected_output": "6"},
    ],
    task=my_task,
    evaluators=[accuracy_evaluator],
)

for item_result in result.item_results:
    print(f"Input: {item_result.item}")
    print(f"Output: {item_result.output}")
    for evaluation in item_result.evaluations:
        print(f"  {evaluation.name}: {evaluation.value}")
```

## 观察类型

SDK 支持 9 种观察类型，对应不同的 span 语义：

| 类型 | 类名 | 用途 |
|------|------|------|
| `span` | `AgentInsightSpan` | 通用工作流步骤 |
| `generation` | `AgentInsightGeneration` | LLM 调用 |
| `agent` | `AgentInsightAgent` | Agent 执行 |
| `tool` | `AgentInsightTool` | 工具调用 |
| `chain` | `AgentInsightChain` | 链式调用 |
| `embedding` | `AgentInsightEmbedding` | 向量嵌入 |
| `evaluator` | `AgentInsightEvaluator` | 评估器 |
| `retriever` | `AgentInsightRetriever` | 检索器 |
| `guardrail` | `AgentInsightGuardrail` | 安全护栏 |

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `AGENTINSIGHT_PUBLIC_KEY` | 项目公钥（必填） | — |
| `AGENTINSIGHT_SECRET_KEY` | 项目私钥（必填） | — |
| `AGENTINSIGHT_BASE_URL` | AgentInsight 服务地址 | `https://agent.goldebridge.com` |
| `AGENTINSIGHT_TRACING_ENABLED` | 是否启用 tracing | `True` |
| `AGENTINSIGHT_TRACING_ENVIRONMENT` | 环境标识 | `default` |
| `AGENTINSIGHT_RELEASE` | 发布版本标识 | — |
| `AGENTINSIGHT_FLUSH_AT` | 批量发送 span 的阈值 | `512` |
| `AGENTINSIGHT_FLUSH_INTERVAL` | 批量发送间隔（秒） | `5` |
| `AGENTINSIGHT_SAMPLE_RATE` | 采样率（0.0 - 1.0） | `1.0` |
| `AGENTINSIGHT_TIMEOUT` | HTTP 请求超时（秒） | `5` |
| `AGENTINSIGHT_DEBUG` | 调试模式 | `False` |
| `AGENTINSIGHT_MEDIA_UPLOAD_ENABLED` | 是否启用媒体上传 | `True` |
| `AGENTINSIGHT_MEDIA_UPLOAD_THREAD_COUNT` | 媒体上传线程数 | `1` |
| `AGENTINSIGHT_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED` | 装饰器 I/O 捕获开关 | `True` |
| `AGENTINSIGHT_PROMPT_CACHE_DEFAULT_TTL_SECONDS` | Prompt 缓存 TTL（秒） | `60` |

### 构造函数参数

```python
from agentinsight import AgentInsight

client = AgentInsight(
    public_key="pk-...",
    secret_key="sk-...",
    base_url="https://agent.goldebridge.com",
    timeout=5,
    debug=False,
    tracing_enabled=True,
    flush_at=512,
    flush_interval=5.0,
    environment="production",
    release="1.0.0",
    sample_rate=1.0,
    media_upload_thread_count=1,
)
```

## 要求

- Python >= 3.10, < 4.0

## 文档

完整文档请参阅 [AgentInsight 官方文档](https://agent.goldebridge.com/docs/sdk/python)。

- [快速开始指南](https://agent.goldebridge.com/docs/observability/sdk/python/sdk-v3)
- [OpenAI 集成](https://agent.goldebridge.com/docs/integrations/openai)
- [LangChain 集成](https://agent.goldebridge.com/docs/integrations/langchain)
- [评估系统](https://agent.goldebridge.com/docs/evaluations)
- [Prompt 管理](https://agent.goldebridge.com/docs/prompts)

## 贡献

请参阅 [CONTRIBUTING.md](https://github.com/AgentInsight/agentinsight-python/blob/main/CONTRIBUTING.md) 了解贡献指南。

## 安全

请参阅 [SECURITY.md](https://github.com/AgentInsight/agentinsight-python/blob/main/SECURITY.md) 了解安全策略和漏洞报告方式。

## 许可证

[MIT License](https://opensource.org/licenses/MIT)

## 致谢

本项目基于 [Langfuse Python SDK](https://github.com/langfuse/langfuse-python) 构建并演化而来，感谢 Langfuse 团队的出色工作。Langfuse Python SDK 采用 MIT 许可证发布。
