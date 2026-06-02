#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AgentInsight Python SDK LangChain 集成示例

本示例展示：
- 配置 LangChain CallbackHandler
- 追踪 Chain 调用
- 追踪 Agent 执行
- 传递 trace 属性（user_id, session_id, tags）

运行前请设置环境变量：
    export AGENTINSIGHT_PUBLIC_KEY="pk-xxx"
    export AGENTINSIGHT_SECRET_KEY="sk-xxx"
    export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"

需要安装 LangChain 依赖：
    pip install langchain langchain-openai
"""

from agentinsight import AgentInsight
from agentinsight.langchain import CallbackHandler


def demo_basic_chain_tracing() -> None:
    # 初始化 AgentInsight 客户端
    client = AgentInsight()

    # 创建 LangChain CallbackHandler
    # Handler 会自动追踪所有 LangChain 的 Chain、LLM、Tool 调用
    handler = CallbackHandler(client=client)

    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model="deepseek-r1:1.5b",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            temperature=0.7,
        )

        prompt = ChatPromptTemplate.from_template("用一句话解释: {topic}")
        chain = prompt | llm | StrOutputParser()

        # 传入 handler 追踪整个 Chain 执行
        result = chain.invoke(
            {"topic": "什么是可观测性?"},
            config={"callbacks": [handler]},
        )

        print(f"Chain 结果: {result}")
    except ImportError:
        print("请安装 langchain-openai: pip install langchain langchain-openai")
    except Exception as e:
        print(f"Chain 示例跳过: {e}")

    client.flush()
    print("基础 Chain 追踪示例完成")


def demo_chain_with_trace_attributes() -> None:
    # 通过 metadata 传递 trace 属性
    # 支持: agentinsight_user_id, agentinsight_session_id, agentinsight_tags
    client = AgentInsight()
    handler = CallbackHandler(client=client)

    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model="deepseek-r1:1.5b",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

        prompt = ChatPromptTemplate.from_template("翻译为英文: {text}")
        chain = prompt | llm | StrOutputParser()

        # 在 metadata 中传递 AgentInsight trace 属性
        result = chain.invoke(
            {"text": "今天天气很好"},
            config={
                "callbacks": [handler],
                "metadata": {
                    "agentinsight_user_id": "user_456",
                    "agentinsight_session_id": "session_translate",
                    "agentinsight_tags": ["translation", "demo"],
                },
                "tags": ["langchain-demo"],
            },
        )

        print(f"翻译结果: {result}")
    except ImportError:
        print("请安装 langchain-openai: pip install langchain langchain-openai")
    except Exception as e:
        print(f"Trace 属性示例跳过: {e}")

    client.flush()
    print("Trace 属性示例完成")


def demo_agent_tracing() -> None:
    # 追踪 LangChain Agent 执行
    # Agent 的工具调用、决策过程都会被自动记录
    client = AgentInsight()
    handler = CallbackHandler(client=client)

    try:
        from langchain.agents import AgentExecutor, create_tool_calling_agent
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.tools import tool
        from langchain_openai import ChatOpenAI

        @tool
        def get_weather(city: str) -> str:
            """获取指定城市的天气信息"""
            return f"{city}今天晴天，温度 25°C"

        @tool
        def calculate(expression: str) -> str:
            """计算数学表达式"""
            try:
                return str(eval(expression))
            except Exception:
                return "计算错误"

        llm = ChatOpenAI(
            model="deepseek-r1:1.5b",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            temperature=0,
        )

        tools = [get_weather, calculate]
        llm_with_tools = llm.bind_tools(tools)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "你是一个有帮助的助手，可以使用工具来回答问题。"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        agent = create_tool_calling_agent(llm_with_tools, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # 追踪 Agent 执行
        result = agent_executor.invoke(
            {"input": "北京今天天气怎么样?"},
            config={
                "callbacks": [handler],
                "metadata": {
                    "agentinsight_user_id": "user_789",
                    "agentinsight_session_id": "session_agent",
                },
            },
        )

        print(f"Agent 结果: {result}")
    except ImportError:
        print("请安装 langchain-openai: pip install langchain langchain-openai")
    except Exception as e:
        print(f"Agent 示例跳过: {e}")

    client.flush()
    print("Agent 追踪示例完成")


def demo_custom_trace_context() -> None:
    # 使用 trace_context 参数将 LangChain 追踪关联到已有 Trace
    # 适用于分布式追踪场景
    client = AgentInsight()

    # 创建一个已有的 Trace
    with client.start_as_current_observation(
        name="api-request",
        as_type="chain",
    ) as root_span:
        trace_id = root_span.trace_id
        root_span.update(output="上游处理完成")

        # 将 LangChain 追踪关联到同一 Trace
        _handler = CallbackHandler(
            client=client,
            trace_context={"trace_id": trace_id},
        )

        print(f"Trace ID: {trace_id}")
        print("LangChain 追踪已关联到同一 Trace")

    client.flush()
    print("自定义 Trace 上下文示例完成")


if __name__ == "__main__":
    demo_basic_chain_tracing()
    demo_chain_with_trace_attributes()
    demo_agent_tracing()
    demo_custom_trace_context()
