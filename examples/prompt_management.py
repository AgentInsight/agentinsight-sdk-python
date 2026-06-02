#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AgentInsight Python SDK Prompt 管理示例

本示例展示：
- 获取 Prompt
- 编译 Prompt 模板
- 创建 Prompt 版本

运行前请设置环境变量：
    export AGENTINSIGHT_PUBLIC_KEY="pk-xxx"
    export AGENTINSIGHT_SECRET_KEY="sk-xxx"
    export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
"""

from agentinsight import AgentInsight


def demo_get_text_prompt() -> None:
    # 获取文本类型的 Prompt
    # 如果服务端不存在该 Prompt，可以使用 fallback 作为后备
    client = AgentInsight()

    try:
        prompt = client.get_prompt(
            "greeting-template",
            type="text",
            fallback="你好 {{name}}，欢迎使用 {{product}}!",
        )

        print(f"Prompt 名称: {prompt.name}")
        print(f"Prompt 版本: {prompt.version}")
        print(f"Prompt 内容: {prompt.prompt}")
        print(f"模板变量: {prompt.variables}")

        # 编译 Prompt 模板，替换变量
        compiled = prompt.compile(name="张三", product="AgentInsight")
        print(f"编译结果: {compiled}")
    except Exception as e:
        print(f"获取文本 Prompt 示例跳过: {e}")

    client.flush()
    print("获取文本 Prompt 示例完成")


def demo_get_chat_prompt() -> None:
    # 获取对话类型的 Prompt
    # Chat Prompt 包含多条消息（system, user, assistant 等）
    client = AgentInsight()

    try:
        prompt = client.get_prompt(
            "qa-assistant",
            type="chat",
            fallback=[
                {"role": "system", "content": "你是一个专业的 {{domain}} 顾问。"},
                {"role": "user", "content": "{{question}}"},
            ],
        )

        print(f"Chat Prompt 名称: {prompt.name}")
        print(f"Chat Prompt 版本: {prompt.version}")

        # 编译 Chat Prompt
        compiled = prompt.compile(domain="技术", question="如何实现微服务架构?")
        print(f"编译结果: {compiled}")
    except Exception as e:
        print(f"获取 Chat Prompt 示例跳过: {e}")

    client.flush()
    print("获取 Chat Prompt 示例完成")


def demo_get_prompt_with_version() -> None:
    # 通过版本号或标签获取特定版本的 Prompt
    client = AgentInsight()

    try:
        # 通过版本号获取
        prompt_v1 = client.get_prompt(
            "my-prompt",
            type="text",
            version=1,
            fallback="版本 1 的内容: {{content}}",
        )
        print(f"版本 1: {prompt_v1.prompt}")

        # 通过标签获取（如 production、staging）
        prompt_prod = client.get_prompt(
            "my-prompt",
            type="text",
            label="production",
            fallback="生产版本: {{content}}",
        )
        print(f"生产版本: {prompt_prod.prompt}")
    except Exception as e:
        print(f"版本/标签获取示例跳过: {e}")

    client.flush()
    print("版本/标签获取示例完成")


def demo_create_text_prompt() -> None:
    # 创建新的文本 Prompt
    client = AgentInsight()

    try:
        prompt = client.create_prompt(
            name="example-text-prompt",
            prompt="请将以下文本翻译为{{language}}：{{text}}",
            type="text",
            labels=["production"],
            tags=["translation", "example"],
            commit_message="初始版本：翻译模板",
        )

        print(f"创建成功: {prompt.name}, 版本: {prompt.version}")
        compiled = prompt.compile(language="英文", text="今天天气很好")
        print(f"编译结果: {compiled}")
    except Exception as e:
        print(f"创建文本 Prompt 示例跳过: {e}")

    client.flush()
    print("创建文本 Prompt 示例完成")


def demo_create_chat_prompt() -> None:
    # 创建新的对话 Prompt
    client = AgentInsight()

    try:
        prompt = client.create_prompt(
            name="example-chat-prompt",
            prompt=[
                {"role": "system", "content": "你是一个{{style}}风格的助手。"},
                {"role": "user", "content": "{{question}}"},
            ],
            type="chat",
            labels=["staging"],
            tags=["assistant", "example"],
            commit_message="初始版本：通用助手模板",
        )

        print(f"创建成功: {prompt.name}, 版本: {prompt.version}")
        compiled = prompt.compile(style="专业", question="如何学习 Python?")
        print(f"编译结果: {compiled}")
    except Exception as e:
        print(f"创建 Chat Prompt 示例跳过: {e}")

    client.flush()
    print("创建 Chat Prompt 示例完成")


def demo_prompt_with_caching() -> None:
    # Prompt 缓存配置
    # AgentInsight 默认缓存 Prompt 60 秒，可通过 cache_ttl_seconds 调整
    client = AgentInsight()

    try:
        # 设置缓存 TTL 为 300 秒
        prompt = client.get_prompt(
            "cached-prompt",
            type="text",
            cache_ttl_seconds=300,
            fallback="缓存示例: {{value}}",
        )

        print(f"带缓存的 Prompt: {prompt.prompt}")

        # 禁用缓存（每次都从服务端获取最新版本）
        prompt_no_cache = client.get_prompt(
            "cached-prompt",
            type="text",
            cache_ttl_seconds=0,
            fallback="无缓存: {{value}}",
        )

        print(f"无缓存 Prompt: {prompt_no_cache.prompt}")
    except Exception as e:
        print(f"缓存配置示例跳过: {e}")

    client.flush()
    print("Prompt 缓存配置示例完成")


if __name__ == "__main__":
    demo_get_text_prompt()
    demo_get_chat_prompt()
    demo_get_prompt_with_version()
    demo_create_text_prompt()
    demo_create_chat_prompt()
    demo_prompt_with_caching()
