#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AgentInsight Python SDK OpenAI 集成示例

本示例展示：
- 配置 AgentInsight 的 OpenAI 自动追踪
- 追踪 ChatCompletion 调用
- 追踪流式响应
- 使用 agentinsight_prompt 参数关联 Prompt

运行前请设置环境变量：
    export AGENTINSIGHT_PUBLIC_KEY="pk-xxx"
    export AGENTINSIGHT_SECRET_KEY="sk-xxx"
    export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
    export OPENAI_API_KEY="sk-xxx"  # 或使用 Ollama 等兼容 API

注意：只需将 `import openai` 替换为 `from agentinsight.openai import openai`，
即可自动追踪所有 OpenAI API 调用，无需修改其他代码。
"""

from agentinsight import AgentInsight, observe
from agentinsight.openai import openai


def demo_basic_chat_completion() -> None:
    # 初始化 AgentInsight 客户端
    client = AgentInsight()

    # 使用 agentinsight.openai 替代原始 openai 包
    # 所有 API 调用会被自动追踪，包括输入、输出、token 用量和延迟
    response = openai.chat.completions.create(
        model="deepseek-r1:1.5b",
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": "什么是 AgentInsight?"},
        ],
        temperature=0.7,
        max_tokens=256,
    )

    print(f"回答: {response.choices[0].message.content}")
    print(f"Token 用量: {response.usage}")

    client.flush()
    print("基础 ChatCompletion 示例完成")


def demo_streaming_chat_completion() -> None:
    # 流式响应也会被自动追踪
    # AgentInsight 会在流结束后汇总所有 chunk 并记录完整响应
    client = AgentInsight()

    stream = openai.chat.completions.create(
        model="deepseek-r1:1.5b",
        messages=[
            {"role": "user", "content": "用三句话介绍 Python。"},
        ],
        stream=True,
    )

    print("流式响应: ", end="")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()

    client.flush()
    print("流式响应示例完成")


def demo_with_agentinsight_prompt() -> None:
    # 使用 agentinsight_prompt 参数将 OpenAI 调用与 AgentInsight Prompt 关联
    # 这样在 AgentInsight UI 中可以看到 Prompt 版本和调用关系
    client = AgentInsight()

    # 先获取一个 Prompt（需要在 AgentInsight 平台上已创建）
    # prompt = client.get_prompt("my-chat-prompt", type="chat")

    # 在 OpenAI 调用中传入 agentinsight_prompt 参数
    # 此处使用 fallback 演示，实际使用时替换为真实 Prompt
    try:
        prompt = client.get_prompt(
            "demo-chat-prompt",
            type="chat",
            fallback=[
                {"role": "system", "content": "你是一个专业的技术顾问。"},
                {"role": "user", "content": "{{question}}"},
            ],
        )

        compiled = prompt.compile(question="如何实现分布式追踪?")
        if isinstance(compiled, list):
            messages = compiled
        else:
            messages = [{"role": "user", "content": compiled}]

        response = openai.chat.completions.create(
            model="deepseek-r1:1.5b",
            messages=messages,
            agentinsight_prompt=prompt,
        )

        print(f"回答: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Prompt 关联示例跳过: {e}")

    client.flush()
    print("Prompt 关联示例完成")


@observe(name="openai-workflow", as_type="chain")
def demo_openai_with_observe_decorator() -> str:
    # @observe 装饰器与 OpenAI 集成无缝配合
    # 装饰器创建的 Span 会自动成为 OpenAI Generation 的父级
    user_question = "解释什么是可观测性"

    # OpenAI 调用会自动成为当前 @observe Span 的子 Span
    response = openai.chat.completions.create(
        model="deepseek-r1:1.5b",
        messages=[
            {"role": "system", "content": "用简洁的语言回答问题。"},
            {"role": "user", "content": user_question},
        ],
        temperature=0.5,
    )

    answer = response.choices[0].message.content or ""
    return answer


def demo_with_trace_metadata() -> None:
    # 通过 OpenAI 调用的额外参数传递 trace 元数据
    # 支持: user_id, session_id, trace_id, tags, metadata 等
    client = AgentInsight()

    response = openai.chat.completions.create(
        model="deepseek-r1:1.5b",
        messages=[
            {"role": "user", "content": "你好"},
        ],
        user_id="user_123",
        session_id="session_abc",
        tags=["demo", "openai-integration"],
        metadata={"source": "example", "version": "1.0"},
    )

    print(f"回答: {response.choices[0].message.content}")

    client.flush()
    print("Trace 元数据示例完成")


if __name__ == "__main__":
    demo_basic_chat_completion()
    demo_streaming_chat_completion()
    demo_with_agentinsight_prompt()
    result = demo_openai_with_observe_decorator()
    print(f"装饰器 + OpenAI 结果: {result}")
    demo_with_trace_metadata()
