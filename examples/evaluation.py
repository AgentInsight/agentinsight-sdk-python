#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AgentInsight Python SDK 评估系统示例

本示例展示：
- 定义评估函数
- 运行实验
- 使用批量评估

运行前请设置环境变量：
    export AGENTINSIGHT_PUBLIC_KEY="pk-xxx"
    export AGENTINSIGHT_SECRET_KEY="sk-xxx"
    export AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
"""

from agentinsight import AgentInsight, Evaluation, observe


def accuracy_evaluator(
    *, input: str, output: str, expected_output: str | None = None, **kwargs: object
) -> Evaluation:
    # 精确匹配评估器：检查输出是否与期望输出完全匹配
    if expected_output is None:
        return Evaluation(
            name="accuracy",
            value=0,
            comment="缺少期望输出，无法评估",
        )

    is_correct = output.strip().lower() == expected_output.strip().lower()
    return Evaluation(
        name="accuracy",
        value=1.0 if is_correct else 0.0,
        comment="回答正确" if is_correct else "回答错误",
    )


def length_evaluator(
    *, input: str, output: str, expected_output: str | None = None, **kwargs: object
) -> Evaluation:
    # 输出长度评估器：评估输出是否在合理长度范围内
    output_len = len(output)
    is_reasonable = 10 <= output_len <= 500

    return Evaluation(
        name="length_quality",
        value=1.0 if is_reasonable else 0.5,
        comment=f"输出长度: {output_len} 字符",
        metadata={"length": output_len},
    )


def multi_metric_evaluator(
    *, input: str, output: str, expected_output: str | None = None, **kwargs: object
) -> list[Evaluation]:
    # 多指标评估器：一次返回多个评估结果
    evaluations: list[Evaluation] = []

    # 包含性检查
    has_content = len(output.strip()) > 0
    evaluations.append(
        Evaluation(
            name="has_content",
            value=has_content,
            comment="输出非空" if has_content else "输出为空",
            data_type="BOOLEAN",
        )
    )

    # 关键词匹配
    if expected_output:
        keywords = expected_output.lower().split()
        matched = sum(1 for kw in keywords if kw in output.lower())
        keyword_ratio = matched / len(keywords) if keywords else 0
        evaluations.append(
            Evaluation(
                name="keyword_match",
                value=round(keyword_ratio, 3),
                comment=f"关键词匹配率: {keyword_ratio:.1%}",
            )
        )

    return evaluations


def demo_basic_experiment() -> None:
    # 运行基础实验
    client = AgentInsight()

    # 定义任务函数
    @observe(as_type="chain")
    def answer_question(*, item: dict, **kwargs: object) -> str:
        question = item["input"]
        return f"关于 '{question}' 的回答"

    # 准备实验数据
    experiment_data = [
        {
            "input": "什么是 Python?",
            "expected_output": "Python 是一种编程语言",
            "metadata": {"category": "programming"},
        },
        {
            "input": "什么是 AgentInsight?",
            "expected_output": "AgentInsight 是可观测性平台",
            "metadata": {"category": "observability"},
        },
        {
            "input": "什么是 OpenTelemetry?",
            "expected_output": "OpenTelemetry 是可观测性标准",
            "metadata": {"category": "observability"},
        },
    ]

    # 运行实验
    result = client.run_experiment(
        name="基础问答评估",
        description="评估问答系统的准确性",
        data=experiment_data,
        task=answer_question,
        evaluators=[accuracy_evaluator, length_evaluator],
    )

    # 打印格式化结果
    print(result.format())

    client.flush()
    print("基础实验示例完成")


def demo_experiment_with_multi_metrics() -> None:
    # 使用多指标评估器运行实验
    client = AgentInsight()

    def process_item(*, item: dict, **kwargs: object) -> str:
        return f"处理结果: {item['input']}"

    data = [
        {"input": "测试问题 1", "expected_output": "测试答案 1"},
        {"input": "测试问题 2", "expected_output": "测试答案 2"},
    ]

    result = client.run_experiment(
        name="多指标评估实验",
        data=data,
        task=process_item,
        evaluators=[multi_metric_evaluator],
    )

    # 打印包含详细条目的结果
    print(result.format(include_item_results=True))

    client.flush()
    print("多指标评估实验完成")


def demo_run_level_evaluator() -> None:
    # 使用运行级别评估器（评估整个实验的聚合指标）
    client = AgentInsight()

    def simple_task(*, item: dict, **kwargs: object) -> str:
        return item["input"]

    def avg_accuracy_evaluator(*, item_results: list, **kwargs: object) -> Evaluation:
        # 计算所有条目的平均准确率
        if not item_results:
            return Evaluation(name="avg_accuracy", value=0.0, comment="无结果")

        accuracy_values = []
        for item_result in item_results:
            for evaluation in item_result.evaluations:
                if evaluation.name == "accuracy" and isinstance(
                    evaluation.value, (int, float)
                ):
                    accuracy_values.append(evaluation.value)

        avg = sum(accuracy_values) / len(accuracy_values) if accuracy_values else 0
        return Evaluation(
            name="avg_accuracy",
            value=round(avg, 3),
            comment=f"平均准确率: {avg:.1%} ({len(accuracy_values)} 个条目)",
        )

    data = [
        {"input": "问题 1", "expected_output": "问题 1"},
        {"input": "问题 2", "expected_output": "不同答案"},
    ]

    result = client.run_experiment(
        name="运行级别评估实验",
        data=data,
        task=simple_task,
        evaluators=[accuracy_evaluator],
        run_evaluators=[avg_accuracy_evaluator],
    )

    print(result.format())

    client.flush()
    print("运行级别评估实验完成")


def demo_categorical_evaluation() -> None:
    # 使用分类评估（CATEGORICAL 类型）
    client = AgentInsight()

    def sentiment_evaluator(
        *, input: str, output: str, expected_output: str | None = None, **kwargs: object
    ) -> Evaluation:
        # 简单的情感分析评估器
        positive_words = ["好", "棒", "优秀", "喜欢", "满意"]
        negative_words = ["差", "糟糕", "讨厌", "不满", "失望"]

        output_lower = output.lower()
        if any(w in output_lower for w in positive_words):
            sentiment = "positive"
        elif any(w in output_lower for w in negative_words):
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return Evaluation(
            name="sentiment",
            value=sentiment,
            comment=f"检测到情感: {sentiment}",
            data_type="CATEGORICAL",
        )

    def generate_response(*, item: dict, **kwargs: object) -> str:
        return item["input"]

    data = [
        {"input": "这个产品很好用"},
        {"input": "服务太差了"},
        {"input": "今天天气一般"},
    ]

    result = client.run_experiment(
        name="情感分析评估",
        data=data,
        task=generate_response,
        evaluators=[sentiment_evaluator],
    )

    print(result.format(include_item_results=True))

    client.flush()
    print("分类评估实验完成")


if __name__ == "__main__":
    demo_basic_experiment()
    demo_experiment_with_multi_metrics()
    demo_run_level_evaluator()
    demo_categorical_evaluation()
