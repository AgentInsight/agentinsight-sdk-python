# AgentInsight Python SDK

[![MIT License](https://img.shields.io/badge/License-MIT-red.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![CI test status](https://img.shields.io/github/actions/workflow/status/AgentInsight/agentinsight-sdk-python/ci.yml?style=flat-square&label=All%20tests)](https://github.com/AgentInsight/agentinsight-sdk-python/actions/workflows/ci.yml?query=branch%3Amain)
[![PyPI Version](https://img.shields.io/pypi/v/agentinsight-sdk.svg?style=flat-square&label=pypi+agentinsight-sdk)](https://pypi.python.org/pypi/agentinsight-sdk)
[![Python Version](https://img.shields.io/pypi/pyversions/agentinsight-sdk.svg?style=flat-square&label=python)](https://pypi.python.org/pypi/agentinsight-sdk)
[![GitHub Repo stars](https://img.shields.io/github/stars/AgentInsight/agentinsight-sdk-python?style=flat-square&logo=GitHub&label=AgentInsight%2Fagentinsight-sdk-python)](https://github.com/AgentInsight/agentinsight-sdk-python)

AgentInsight Python SDK — 用于将 AI 应用可观测性数据发送到 [AgentInsight](https://agentinsight.goldebridge.com/platform) 平台的官方 Python 客户端库。

The official Python client library for sending AI application observability data to the [AgentInsight](https://agentinsight.goldebridge.com/platform) platform.

基于 OpenTelemetry 协议，支持自动追踪 AI 模型调用、评分评估、Prompt 管理等功能。提供三种集成方式：直接 SDK 调用、`@observe` 装饰器、以及 OpenAI / LangChain 开箱即用的集成。

Built on the OpenTelemetry protocol, supporting automatic AI model call tracing, scoring & evaluation, prompt management, and more. Offers three integration methods: direct SDK calls, the `@observe` decorator, and out-of-the-box OpenAI / LangChain integrations.

## 特性 / Features

- 🔍 **自动追踪 / Automatic Tracing** — 使用 `@observe` 装饰器自动追踪函数调用，捕获输入/输出、耗时和错误 / Use the `@observe` decorator to automatically trace function calls, capturing inputs/outputs, latency, and errors
- 🤖 **LLM 集成 / LLM Integrations** — 开箱即用的 OpenAI 和 LangChain 集成，仅需修改一行 import / Out-of-the-box OpenAI and LangChain integrations, requiring only a single import change
- 📊 **评分与评估 / Scoring & Evaluation** — 内置评估框架和批量评估系统，支持 NUMERIC / BOOLEAN / CATEGORICAL 评分 / Built-in evaluation framework and batch evaluation system, supporting NUMERIC / BOOLEAN / CATEGORICAL scores
- 🔄 **上下文传播 / Context Propagation** — 基于 OpenTelemetry Baggage 的跨服务上下文传播 / Cross-service context propagation based on OpenTelemetry Baggage
- 📝 **Prompt 管理 / Prompt Management** — 版本控制的 Prompt 管理和模板编译 / Version-controlled prompt management and template compilation
- 📁 **数据集与实验 / Datasets & Experiments** — 数据集管理和 A/B 实验框架 / Dataset management and A/B experiment framework
- 🛡️ **多项目隔离 / Multi-Project Isolation** — 通过 `ContextVar` 实现多项目场景下的客户端隔离，防止 trace 数据跨项目泄漏 / Client isolation across projects via `ContextVar`, preventing trace data leakage between projects
- ⚡ **高性能 / High Performance** — 批量发送 span、后台线程处理媒体上传和评分摄入 / Batch span export, background threads for media upload and score ingestion

## 安装 / Installation

```bash
pip install agentinsight-sdk
```

OpenAI 集成需要额外安装 OpenAI 包 / For OpenAI integration, install the OpenAI package additionally:

```bash
pip install agentinsight-sdk openai
```

LangChain 集成需要额外安装 LangChain 包 / For LangChain integration, install the LangChain packages additionally:

```bash
pip install agentinsight-sdk langchain langchain-openai
```

## 快速开始 / Quick Start

### 1. 初始化客户端 / Initialize the Client

```python
import agentinsight

agentinsight.init(
    public_key="pk-...",
    secret_key="sk-...",
    base_url="https://agent.goldebridge.com",
)
```

或者通过环境变量配置 / Or configure via environment variables:

```bash
export AGENTINSIGHT_PUBLIC_KEY="pk-..."
export AGENTINSIGHT_SECRET_KEY="sk-..."
export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
```

```python
from agentinsight import AgentInsight

client = AgentInsight()
```

### 2. 使用 @observe 装饰器 / Use the @observe Decorator

`@observe` 装饰器是最简单的追踪方式，自动捕获函数的输入、输出和耗时 / The `@observe` decorator is the simplest way to add tracing, automatically capturing function inputs, outputs, and latency:

```python
from agentinsight import observe

@observe(name="my-function")
def my_function(query: str) -> str:
    return f"Processed: {query}"

result = my_function("Hello, AgentInsight!")
```

装饰器支持嵌套调用，自动建立父子关系 / The decorator supports nested calls and automatically establishes parent-child relationships:

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

### 3. 追踪 LLM 调用 / Trace LLM Calls

使用 `as_type="generation"` 标记 LLM 调用，记录模型参数和 token 用量 / Use `as_type="generation"` to mark LLM calls, recording model parameters and token usage:

```python
from agentinsight import observe

@observe(as_type="generation")
def call_llm(prompt: str) -> str:
    # Your LLM call here
    return "LLM response"

result = call_llm("What is AI?")
```

也可以使用低级 API 手动管理 span / You can also use the low-level API to manually manage spans:

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

### 4. 添加评分 / Add Scores

为任何 span 添加评分，支持 NUMERIC、BOOLEAN 和 CATEGORICAL 类型 / Add scores to any span, supporting NUMERIC, BOOLEAN, and CATEGORICAL types:

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

## OpenAI 集成 / OpenAI Integration

只需修改一行 import，即可自动追踪所有 OpenAI API 调用 / Automatically trace all OpenAI API calls by changing a single import line:

```diff
- import openai
+ from agentinsight.openai import openai
```

完整示例 / Full example:

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

AgentInsight 自动追踪 / AgentInsight automatically traces:
- 所有 prompts 和 completions（支持 streaming、async 和 function calling）/ All prompts and completions (supports streaming, async, and function calling)
- 请求延迟 / Request latency
- API 错误 / API errors
- Token 用量和成本 / Token usage and costs

## LangChain 集成 / LangChain Integration

使用 `AgentInsightCallbackHandler` 追踪 LangChain 链的执行 / Use `AgentInsightCallbackHandler` to trace LangChain chain execution:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agentinsight.langchain import AgentInsightCallbackHandler

handler = AgentInsightCallbackHandler()

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

## 上下文传播 / Context Propagation

使用 `propagate_attributes` 在 trace 内设置用户级、会话级属性，自动传播到所有子 span / Use `propagate_attributes` to set user-level and session-level attributes within a trace, automatically propagating them to all child spans:

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

跨服务传播（通过 HTTP 头部）/ Cross-service propagation (via HTTP headers):

```python
from agentinsight import propagate_attributes

with propagate_attributes(
    user_id="user_123",
    session_id="session_abc",
    as_baggage=True,
):
    pass
```

## 评估系统 / Evaluation System

AgentInsight 提供内置的实验和评估框架 / AgentInsight provides a built-in experiment and evaluation framework:

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

## 观察类型 / Observation Types

SDK 支持 9 种观察类型，对应不同的 span 语义 / The SDK supports 9 observation types, each corresponding to different span semantics:

| 类型 / Type | 类名 / Class | 用途 / Usage |
|------|-------|-------|
| `span` | `AgentInsightSpan` | 通用工作流步骤 / General workflow step |
| `generation` | `AgentInsightGeneration` | LLM 调用 / LLM call |
| `agent` | `AgentInsightAgent` | Agent 执行 / Agent execution |
| `tool` | `AgentInsightTool` | 工具调用 / Tool call |
| `chain` | `AgentInsightChain` | 链式调用 / Chain call |
| `embedding` | `AgentInsightEmbedding` | 向量嵌入 / Vector embedding |
| `evaluator` | `AgentInsightEvaluator` | 评估器 / Evaluator |
| `retriever` | `AgentInsightRetriever` | 检索器 / Retriever |
| `guardrail` | `AgentInsightGuardrail` | 安全护栏 / Safety guardrail |

## 配置 / Configuration

### 环境变量 / Environment Variables

| 变量 / Variable | 说明 / Description | 默认值 / Default |
|----------|-------------|---------|
| `AGENTINSIGHT_PUBLIC_KEY` | 项目公钥（必填）/ Project public key (required) | — |
| `AGENTINSIGHT_SECRET_KEY` | 项目私钥（必填）/ Project secret key (required) | — |
| `AGENTINSIGHT_BASE_URL` | AgentInsight 服务地址 / AgentInsight server URL | `https://agent.goldebridge.com` |
| `AGENTINSIGHT_TRACING_ENABLED` | 是否启用 tracing / Enable tracing | `True` |
| `AGENTINSIGHT_TRACING_ENVIRONMENT` | 环境标识 / Environment identifier | `default` |
| `AGENTINSIGHT_RELEASE` | 发布版本标识 / Release version identifier | — |
| `AGENTINSIGHT_FLUSH_AT` | 批量发送 span 的阈值 / Batch span export threshold | `512` |
| `AGENTINSIGHT_FLUSH_INTERVAL` | 批量发送间隔（秒）/ Batch export interval (seconds) | `5` |
| `AGENTINSIGHT_SAMPLE_RATE` | 采样率（0.0 - 1.0）/ Sample rate (0.0 - 1.0) | `1.0` |
| `AGENTINSIGHT_TIMEOUT` | HTTP 请求超时（秒）/ HTTP request timeout (seconds) | `5` |
| `AGENTINSIGHT_DEBUG` | 调试模式 / Debug mode | `False` |
| `AGENTINSIGHT_MEDIA_UPLOAD_ENABLED` | 是否启用媒体上传 / Enable media upload | `True` |
| `AGENTINSIGHT_MEDIA_UPLOAD_THREAD_COUNT` | 媒体上传线程数 / Media upload thread count | `1` |
| `AGENTINSIGHT_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED` | 装饰器 I/O 捕获开关 / Decorator I/O capture switch | `True` |
| `AGENTINSIGHT_PROMPT_CACHE_DEFAULT_TTL_SECONDS` | Prompt 缓存 TTL（秒）/ Prompt cache TTL (seconds) | `60` |

### 构造函数参数 / Constructor Parameters

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

## 系统要求 / Requirements

- Python >= 3.10, < 4.0

## 文档 / Documentation

完整文档请参阅 [AgentInsight 官方文档](https://agentinsight.goldebridge.com/platform/docs/sdk/python)。

For full documentation, please refer to the [AgentInsight Official Documentation](https://agentinsight.goldebridge.com/platform/docs/sdk/python).

- [快速开始指南 / Quick Start Guide](https://agentinsight.goldebridge.com/platform/docs/observability/sdk/python/sdk-v3)
- [OpenAI 集成 / OpenAI Integration](https://agentinsight.goldebridge.com/platform/docs/integrations/openai)
- [LangChain 集成 / LangChain Integration](https://agentinsight.goldebridge.com/platform/docs/integrations/langchain)
- [评估系统 / Evaluation System](https://agentinsight.goldebridge.com/platform/docs/evaluations)
- [Prompt 管理 / Prompt Management](https://agentinsight.goldebridge.com/platform/docs/prompts)

## 贡献 / Contributing

请参阅 [CONTRIBUTING.md](https://github.com/AgentInsight/agentinsight-sdk-python/blob/main/CONTRIBUTING.md) 了解贡献指南。

Please refer to [CONTRIBUTING.md](https://github.com/AgentInsight/agentinsight-sdk-python/blob/main/CONTRIBUTING.md) for contribution guidelines.

## 安全 / Security

请参阅 [SECURITY.md](https://github.com/AgentInsight/agentinsight-sdk-python/blob/main/SECURITY.md) 了解安全策略和漏洞报告方式。

Please refer to [SECURITY.md](https://github.com/AgentInsight/agentinsight-sdk-python/blob/main/SECURITY.md) for security policy and vulnerability reporting.

## 致谢 / Acknowledgements

本项目基于 [Langfuse Python SDK](https://github.com/langfuse/langfuse-python) 构建并演化而来，感谢 Langfuse 团队的出色工作。Langfuse Python SDK 采用 MIT 许可证发布。

This project is built upon and evolved from the [Langfuse Python SDK](https://github.com/langfuse/langfuse-python). We thank the Langfuse team for their excellent work. The Langfuse Python SDK is released under the MIT License.

## 许可证 / License

[MIT License](https://opensource.org/licenses/MIT)
