#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AgentInsight Python SDK 基础追踪示例

本示例展示：
- 初始化 AgentInsight 客户端
- 使用 @observe 装饰器追踪函数
- 创建 Span 和 Generation
- 添加评分
- 刷新数据

运行前请设置环境变量：
    export AGENTINSIGHT_PUBLIC_KEY="pk-xxx"
    export AGENTINSIGHT_SECRET_KEY="sk-xxx"
    export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
"""

import agentinsight
from agentinsight import AgentInsight, observe


def demo_basic_tracing() -> None:
    # 初始化客户端（也可通过环境变量 AGENTINSIGHT_PUBLIC_KEY / AGENTINSIGHT_SECRET_KEY / AGENTINSIGHT_BASE_URL 自动读取）
    client = AgentInsight()

    # 方式一：使用 start_as_current_observation 上下文管理器创建 Span
    with client.start_as_current_observation(
        name="user-workflow",
        as_type="chain",
        input={"user_query": "什么是 AgentInsight?"},
        metadata={"environment": "demo"},
    ) as root_span:
        # 在根 Span 内创建子 Span
        with client.start_as_current_observation(
            name="search-docs",
            as_type="span",
            input={"query": "AgentInsight 文档"},
        ) as search_span:
            result = "AgentInsight 是一个基于 OpenTelemetry 的智能体可观测性平台"
            search_span.update(output=result)

        # 创建 Generation 类型观察（用于记录 LLM 调用）
        with client.start_as_current_observation(
            name="generate-answer",
            as_type="generation",
            input={"messages": [{"role": "user", "content": "什么是 AgentInsight?"}]},
            model="deepseek-r1:1.5b",
            model_parameters={"temperature": 0.7, "max_tokens": 1024},
        ) as generation:
            answer = "AgentInsight 是一个基于 OpenTelemetry 标准的智能体可观测性 SDK"
            generation.update(
                output=answer,
                usage_details={"input": 15, "output": 20, "total": 35},
            )

        root_span.update(output={"answer": answer})

        # 为当前 Span 添加评分
        client.score_current_span(
            name="relevance",
            value=0.95,
            comment="回答高度相关",
        )

        # 为整个 Trace 添加评分
        client.score_current_trace(
            name="overall-quality",
            value=0.9,
            comment="整体质量良好",
        )

    # 刷新确保数据发送到服务端
    client.flush()
    print("基础追踪示例完成")


@observe(name="process-request", as_type="chain")
def process_request(user_query: str) -> str:
    # 使用 @observe 装饰器自动追踪函数
    # 装饰器会自动创建 Span 并捕获输入输出
    search_result = search_knowledge_base(user_query)
    answer = generate_answer(search_result)
    return answer


@observe(name="search-kb", as_type="tool")
def search_knowledge_base(query: str) -> str:
    return f"关于 '{query}' 的搜索结果"


@observe(name="generate-answer", as_type="generation")
def generate_answer(context: str) -> str:
    return f"基于以下内容生成回答: {context}"


def demo_decorator_tracing() -> None:
    # 使用 @observe 装饰器追踪
    # 装饰器自动建立父子关系：process_request 是父 Span，内部调用自动成为子 Span
    result = process_request("如何使用 AgentInsight?")
    print(f"装饰器追踪结果: {result}")

    # 获取客户端并刷新
    client = agentinsight.get_client()
    client.flush()
    print("装饰器追踪示例完成")


def demo_manual_span_management() -> None:
    # 方式三：手动创建和管理 Span（不使用上下文管理器）
    client = AgentInsight()

    span = client.start_observation(
        name="manual-workflow",
        as_type="chain",
        input={"task": "手动 Span 管理"},
    )

    generation = span.start_observation(
        name="manual-generation",
        as_type="generation",
        input={"prompt": "手动创建的 Generation"},
        model="deepseek-r1:1.5b",
    )

    generation.update(
        output="手动管理的 Generation 输出",
        usage_details={"input": 10, "output": 15, "total": 25},
    )
    generation.end()

    span.update(output="手动管理的 Span 输出")
    span.end()

    client.flush()
    print("手动 Span 管理示例完成")


if __name__ == "__main__":
    demo_basic_tracing()
    demo_decorator_tracing()
    demo_manual_span_management()
