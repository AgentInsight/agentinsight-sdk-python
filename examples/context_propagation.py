#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AgentInsight Python SDK 上下文传播示例

本示例展示：
- 使用 propagate_attributes 传播上下文
- 跨服务传播（as_baggage=True）
- 在下游服务中接收上下文

运行前请设置环境变量：
    export AGENTINSIGHT_PUBLIC_KEY="pk-xxx"
    export AGENTINSIGHT_SECRET_KEY="sk-xxx"
    export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
"""

from agentinsight import AgentInsight, observe, propagate_attributes


def demo_basic_propagation() -> None:
    # 使用 propagate_attributes 在整个 Trace 中传播属性
    # 所有在上下文中创建的 Span 都会自动继承这些属性
    client = AgentInsight()

    with client.start_as_current_observation(
        name="user-request",
        as_type="chain",
    ) as root_span:
        # 在 Trace 早期设置传播属性
        # 这些属性会自动传播到所有子 Span
        with propagate_attributes(
            user_id="user_123",
            session_id="session_abc",
            metadata={"environment": "production", "region": "cn-east"},
            tags=["v2", "premium"],
        ):
            # 子 Span 自动继承 user_id, session_id, metadata, tags
            with client.start_as_current_observation(
                name="process-query",
                as_type="span",
            ) as child_span:
                child_span.update(output="查询处理完成")

            # Generation 也自动继承
            with client.start_as_current_observation(
                name="generate-response",
                as_type="generation",
                model="deepseek-r1:1.5b",
            ) as generation:
                generation.update(output="生成的回答")

        root_span.update(output="请求处理完成")

    client.flush()
    print("基础属性传播示例完成")


def demo_propagation_with_observe() -> None:
    # propagate_attributes 与 @observe 装饰器配合使用
    client = AgentInsight()

    @observe(name="main-workflow", as_type="chain")
    def main_workflow() -> str:
        # 在装饰器函数内设置传播属性
        with propagate_attributes(
            user_id="user_456",
            session_id="session_def",
            trace_name="user-workflow-trace",
        ):
            # 所有嵌套的 @observe 函数都会继承属性
            result = sub_task()
            return result

    @observe(name="sub-task", as_type="tool")
    def sub_task() -> str:
        return "子任务完成"

    main_workflow()

    client.flush()
    print("propagate_attributes + @observe 示例完成")


def demo_cross_service_propagation() -> None:
    # 使用 as_baggage=True 实现跨服务传播
    # 属性会通过 OpenTelemetry Baggage 传播到 HTTP 请求头中
    # 下游服务可以自动提取这些属性
    client = AgentInsight()

    with client.start_as_current_observation(
        name="api-gateway",
        as_type="chain",
    ) as gateway_span:
        # 启用跨服务传播
        # 注意：as_baggage=True 会将属性值添加到所有出站 HTTP 请求头中
        # 仅在值可以安全通过 HTTP 头传输时启用
        with propagate_attributes(
            user_id="user_789",
            session_id="session_cross_service",
            metadata={"service": "gateway", "version": "2.0"},
            as_baggage=True,
        ):
            # 模拟调用下游服务
            # 在实际场景中，httpx/requests 会自动在请求头中携带 baggage
            print("跨服务属性已设置，下游服务可通过 Baggage 接收")

            with client.start_as_current_observation(
                name="call-downstream",
                as_type="span",
            ) as call_span:
                call_span.update(output="下游服务调用完成")

        gateway_span.update(output="网关处理完成")

    client.flush()
    print("跨服务传播示例完成")


def demo_downstream_service_context() -> None:
    # 模拟下游服务接收传播的上下文
    # 在实际场景中，OpenTelemetry 会自动从 HTTP 头提取 Baggage
    client = AgentInsight()

    # 下游服务中，propagate_attributes 可以继续添加或覆盖属性
    with client.start_as_current_observation(
        name="downstream-service",
        as_type="chain",
    ) as service_span:
        # 下游服务可以设置自己的传播属性
        # 这些属性会与上游传播的属性合并
        with propagate_attributes(
            user_id="user_789",
            session_id="session_cross_service",
            metadata={"service": "downstream", "version": "1.0"},
        ):
            with client.start_as_current_observation(
                name="process-in-downstream",
                as_type="span",
            ) as process_span:
                process_span.update(output="下游处理完成")

        service_span.update(output="下游服务完成")

    client.flush()
    print("下游服务上下文接收示例完成")


def demo_version_propagation() -> None:
    # 使用 version 参数传播版本信息
    # 适用于追踪不同版本的应用组件
    client = AgentInsight()

    with client.start_as_current_observation(
        name="versioned-workflow",
        as_type="chain",
    ) as root_span:
        with propagate_attributes(
            user_id="user_version_demo",
            version="agent-v2.1.0",
            metadata={"deployment": "blue", "feature_flag": "new_algorithm"},
        ):
            with client.start_as_current_observation(
                name="versioned-operation",
                as_type="span",
            ) as op_span:
                op_span.update(output="版本化操作完成")

        root_span.update(output="版本化工作流完成")

    client.flush()
    print("版本传播示例完成")


if __name__ == "__main__":
    demo_basic_propagation()
    demo_propagation_with_observe()
    demo_cross_service_propagation()
    demo_downstream_service_context()
    demo_version_propagation()
