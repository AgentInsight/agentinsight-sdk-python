---
alwaysApply: false
globs: agentinsight-python/**/*.*
---
# AgentInsight Python SDK — 智能体执行规则

> 本文档是AI智能体（AI Agent）执行本项目开发任务的规则依据。智能体在执行任何任务前，必须先完整阅读本文档，并严格按照本文档定义的规则执行。

---

## 1. 项目基本信息

### 1.1 技术栈

| 类别 | 技术选型 |
|------|---------|
| 语言/框架 | Python >= 3.10, < 4.0 |
| 包管理 | uv 0.11.2（锁定依赖 + 构建后端） |
| 类型检查 | mypy >= 1.0（严格模式，`disallow_untyped_defs = true`） |
| 代码风格 | ruff >= 0.15.2（Google docstring 约定） |
| HTTP 客户端 | httpx >= 0.15.4 |
| 数据模型 | Pydantic >= 2 |
| 可观测性 | OpenTelemetry API + SDK >= 1.33.1（TracerProvider + OTLP HTTP Exporter） |
| API 客户端 | Fern 自动生成（`agentinsight/api/`，不可手改） |
| 测试 | pytest >= 7.4 + pytest-xdist + pytest-asyncio + pytest-httpserver |
| 重试/退避 | backoff + tenacity |
| 猴子补丁 | wrapt（OpenAI 集成） |
| 构建 | uv build --no-sources |
| 文档 | pdoc >= 15.0.4（Google 格式） |
| 部署 | PyPI 发布（GitHub Actions 自动触发） |

### 1.2 项目关键特征

- **OpenTelemetry 原生**：SDK 完全构建在 OpenTelemetry 标准之上，不作私有 tracing 协议。Span 通过 `OTLPSpanExporter` 发送到 AgentInsight OTLP 端点。
- **单例资源管理**：`AgentInsightResourceManager` 按 `public_key` 管理单例，每个 API key 维护独立的 `TracerProvider`、`AgentInsightSpanProcessor` 和后台线程。
- **多项目安全隔离**：通过 `ContextVar` 实现多项目场景下的客户端隔离，防止 trace 数据跨项目泄漏。
- **三级集成方式**：直接 SDK（`AgentInsight` 客户端）、`@observe` 装饰器、OpenAI 直插替换（`agentinsight.openai`）、LangChain 回调处理器。
- **后台任务线程**：`MediaUploadConsumer`（媒体上传）+ `ScoreIngestionConsumer`（评分摄入），通过 sentinel 对象实现优雅关闭。
- **自动生成 API 客户端**：`agentinsight/api/` 由 Fern 根据 OpenAPI 规范自动生成，覆盖 ingestion、prompts、datasets、scores、media 等全部端点。

### 1.3 项目目录结构

| 目录 | 说明 |
|------|------|
| `agentinsight/__init__.py` | 公共 API 入口，`__all__` 导出全部公开符号 |
| `agentinsight/_client/` | 核心 SDK：客户端、装饰器、资源管理器、Span 处理器、Span 过滤器、属性传播、数据集 |
| `agentinsight/_task_manager/` | 后台消费者：媒体上传队列与管理、评分摄入 |
| `agentinsight/_utils/` | 内部工具：HTTP 客户端、序列化器、提示缓存、错误日志、环境变量 |
| `agentinsight/api/` | **Fern 自动生成**的 API 客户端，**禁止手改** |
| `agentinsight/openai.py` | OpenAI SDK 直插式集成（wrapt 猴子补丁） |
| `agentinsight/langchain/` | LangChain 回调处理器集成 |
| `tests/unit/` | 单元测试：不需要 AgentInsight 服务器，使用 `InMemorySpanExporter` |
| `tests/e2e/` | 端到端测试：需要真实 AgentInsight 服务器，使用带轮询重试的 API wrapper |
| `tests/live_provider/` | 供应商测试：需要真实 OpenAI/LangChain API 调用 |
| `tests/support/` | e2e 共享辅助工具（API wrapper、重试、轮询） |
| `scripts/select_e2e_shard.py` | CI 分片选择器：历史权重 + 贪心装箱算法 |
| `scripts/codex/` | Codex 云/工作树引导和共享快速检查 |

---

## 2. 智能体行为规则

### 2.1 角色模拟规则

智能体在同一时刻仅扮演一个角色。角色列表：

| 角色 | 职责描述 |
|------|---------|
| **SDK 架构师** | 负责 SDK 架构设计、OpenTelemetry 集成方案评审、资源管理器生命周期管理；指导高效 Python 编程实践，确保代码质量和系统稳定性 |
| **SDK 开发工程师** | 负责核心 SDK 功能开发、集成层实现（OpenAI/LangChain）、序列化/HTTP 层维护；编写和维护所负责模块的单元测试 |
| **API 集成工程师** | 负责 Fern API 客户端重新生成与集成、公共 API 契约维护、序列化/反序列化测试 |
| **测试工程师** | 负责测试策略制定、测试用例设计、三级测试（单元/E2E/供应商）执行、覆盖率追踪 |
| **CI/发布工程师** | 负责 CI 流水线维护、e2e 分片配置、PyPI 发布流程、依赖可用性检查 |

### 2.2 自动化分级

| 级别 | 含义 |
|------|------|
| **自主执行** | 智能体可独立完成，无需人工介入 |
| **需人工确认** | 智能体完成工作后必须暂停，等待人工确认 |

### 2.3 人工介入触发条件

智能体**必须暂停**请求人工介入的场景：
1. 需求矛盾/缺失、架构方案需权衡、评审意见无法裁决
2. OpenTelemetry 版本升级导致不兼容变更
3. 连续3次修复后测试仍失败
4. 涉及：`agentinsight/api/` 重新生成（Fern 上游变更）、公共 API 签名变更（breaking change）、环境变量新增/重命名、`_version.py` 版本号策略变更
5. 发现硬编码的密钥/密码/连接字符串
6. 调试中需要注入真实 `AGENTINSIGHT_SECRET_KEY` 进行服务端验证

### 2.4 错误处理策略

通用策略：**分析原因 → 逐层排查（代码→配置→环境）→ 无法解决则请求人工介入**。

| 场景 | 排查路径 |
|------|---------|
| 单元测试失败 | `InMemorySpanExporter` 收集的 span → span 属性/名称/父子关系 → 业务逻辑 |
| E2E 测试失败 | API wrapper 轮询超时 → AgentInsight 服务器健康检查 → docker compose 日志 → 网络连接 |
| 类型检查不通过 | mypy 错误行 → 类型注解 → `pyproject.toml` 的 `tool.mypy.overrides` 配置 |
| 序列化异常 | `EventSerializer` 自定义编码逻辑 → 对象类型 → JSON 兼容性 |
| 后台线程泄漏 | `ResourceManager.shutdown()` → sentinel 注入 → consumer 线程状态 |
| 依赖安装失败 | uv 锁定版本 → `pyproject.toml` 依赖约束 → 上游包兼容性 |

---

## 3. 文件操作规则

- **所有代码改动必须在 `agentinsight-python/` 目录及其子目录下**
- **所有文档保存在 `agentinsight-python/documents/`**，命名规范：`<类型>-<名称>-v<版本号>.md`
- **所有测试文件必须在 `tests/` 目录下对应层级**
- 各类型新增位置：

| 类型 | 目录 | 说明 |
|------|------|------|
| 核心 SDK | `agentinsight/_client/` | 客户端、装饰器、资源管理、Span 处理、属性传播 |
| 后台任务 | `agentinsight/_task_manager/` | 媒体上传、评分摄入消费者 |
| 工具函数 | `agentinsight/_utils/` | HTTP 客户端、序列化器、缓存、错误处理 |
| 集成层 | `agentinsight/openai.py` 或 `agentinsight/langchain/` | OpenAI/LangChain 集成 |
| API 客户端 | `agentinsight/api/` | **仅限 Fern 重新生成，不可手改** |
| 公共 API | `agentinsight/__init__.py` | 导出 `__all__` 列表 |
| 环境变量 | `agentinsight/_client/environment_variables.py` | `AGENTINSIGHT_*` 常量定义 |
| 单元测试 | `tests/unit/test_*.py` | 命名 `test_{module}.py` |
| E2E 测试 | `tests/e2e/test_*.py` | 命名 `test_{feature}.py` |
| 供应商测试 | `tests/live_provider/test_*.py` | 命名 `test_{provider}.py` |
| 测试辅助 | `tests/support/` | API wrapper、重试、轮询工具 |

---

## 4. 任务执行流程规则

- **前置条件**：用户提交需求
- **执行动作**：

  **步骤1：影响范围分析** `[自主执行]`
  - 确定需求影响的代码层级：公共 API → 核心 SDK → 后台任务 → 序列化/HTTP 层 → 集成层
  - 判断是否需要 Fern API 重新生成
  - 判断是否为 breaking change

  **步骤2：编写/定位测试** `[自主执行]`
  - Bug 修复：先写一个能复现 bug 的失败测试，确认失败
  - 新功能：根据三层测试体系确定测试层级
  - 运行确认测试失败（红阶段）：
    ```bash
    uv run --frozen pytest tests/unit/test_target.py::test_new_case -v
    ```

  **步骤3：编写功能代码** `[自主执行]`
  - 仅编写使当前失败测试通过的代码
  - 遵循编码规则（参见第5节）

  **步骤4：质量检查** `[自主执行]`
  - 运行代码风格检查：
    ```bash
    uv run --frozen ruff check .
    uv run --frozen ruff format .
    ```
  - 运行类型检查：
    ```bash
    uv run --frozen mypy agentinsight --no-error-summary
    ```

  **步骤5：运行测试** `[自主执行]`
  - 最小验证矩阵（参见第7节）
  - 确认所有相关测试通过

  **步骤6：自审** `[自主执行]`
  - 对照 `code_review.md` 检查清单自审
  - 检查 diff 中无意外修改、无生成文件的手动编辑
  - 确认 `.env.template` 与新环境变量保持同步

  **步骤7：交付** `[自主执行]`
  - 输出变更摘要、验证命令及结果、跳过的检查及原因

- **后置条件**：所有相关测试通过，类型检查通过，代码风格通过，`code_review.md` 检查清单通过

---

## 5. 编码规则

### 5.1 Python 编码铁律

1. **无注释代码**：除非用户明确要求，不在代码中添加注释
2. **ASCII 优先**：仅当文件已使用 Unicode 或明确需要时才使用非 ASCII 字符
3. **异常消息**：不在 `raise` 语句中直接使用 f-string 字面量；先构建消息变量再抛出
4. **类型注解**：所有新函数必须有完整类型注解（配合 `disallow_untyped_defs = true`）
5. **Google docstring**：如有文档字符串，遵循 Google 风格约定
6. **导入排序**：ruff I 规则自动排序（标准库 → 第三方 → 本地）
7. **小改动优先**：保持改动聚焦，避免无关重构
8. **保持向后兼容**：公共 API 默认向后兼容，除非 PR 明确标记为 breaking change

### 5.2 设计原则

1. **基于 OTEL 标准**：所有 trace/span 操作通过 OpenTelemetry API，不使用私有协议
2. **单例资源管理**：`AgentInsightResourceManager` 确保每个 public_key 的唯一实例
3. **线程安全**：后台线程（MediaUploadConsumer、ScoreIngestionConsumer）必须支持优雅关闭
4. **可测试性**：核心逻辑可通过 `InMemorySpanExporter` 在单元测试中验证
5. **防御性编程**：对外部输入进行校验，做好异常处理和错误日志

### 5.3 API 约定

- **环境变量**：优先使用 `AGENTINSIGHT_BASE_URL`；`AGENTINSIGHT_HOST` 已废弃，仅在兼容路径或测试中出现
- **`agentinsight/api/`**：不可手改，必须通过上游 Fern/OpenAPI 重新生成
- **公共 API 变更**：更新 `__all__`、示例代码、README 片段和相关引用文档
- **`.env.template`**：与环境变量变更保持同步

---

## 6. 测试规则

### 6.1 三级测试体系

| 层级 | 目录 | 标记 | 特征 |
|------|------|------|------|
| **单元测试**| 单元测试 | `tests/unit/` | `@pytest.mark.unit` | 不需要 AgentInsight 服务器，使用 `InMemorySpanExporter` |
| **E2E 测试** | `tests/e2e/` | `@pytest.mark.e2e` | 需要真实 AgentInsight 服务器，使用带轮询重试的 API wrapper |
| **串行 E2E** | `tests/e2e/` | `@pytest.mark.serial_e2e` | 共享状态敏感，不能并发执行 |
| **供应商测试** | `tests/live_provider/` | `@pytest.mark.live_provider` | 需要真实 OpenAI/LangChain API 调用，作为独立 CI 套件 |

### 6.2 测试运行命令

```bash
# 单元测试
uv run --frozen pytest -n auto --dist worksteal tests/unit

# 可并发的 E2E 测试
uv run --frozen pytest -n 4 --dist worksteal tests/e2e -m "not serial_e2e"

# 串行 E2E 测试
uv run --frozen pytest tests/e2e -m "serial_e2e"

# 供应商测试
uv run --frozen pytest -n 4 --dist worksteal tests/live_provider -m "live_provider"

# 单个测试
uv run --frozen pytest tests/unit/test_resource_manager.py::test_pause_signals_score_consumer_shutdown
```

### 6.3 最小验证矩阵

| 变更范围 | 最低验证要求 |
|---------|------------|
| 仅文档或注释 | Python 文件变更时 `uv run --frozen ruff format --check .` |
| 仅 Python 源码 | `uv run --frozen ruff check .` + `uv run --frozen mypy agentinsight --no-error-summary` + 针对性单元测试 |
| 仅单元测试 | 针对性 `uv run --frozen pytest ...` |
| 关闭、刷新、工作线程、OTEL 行为 | 针对性 resource-manager/OTEL 测试 + 相关集成测试 |
| OpenAI 或 LangChain 集成 | 使用 exporter-local 断言的针对性单元测试；仅在单元测试无法覆盖时添加 e2e/live_provider 测试 |
| 生成 API 客户端或公共 API 契约 | 上游 Fern/OpenAPI 重新生成路径 + 针对性序列化/反序列化测试 |
| CI、分片或引导 | 相关脚本测试 + 对照本文档的 CI 契约检查 |

### 6.4 测试拓扑

#### `tests/unit`
- 绝不能需要运行中的 AgentInsight 服务器
- 优先使用内存 exporter（`InMemorySpanExporter`）和本地 fake 代替网络调用
- 若测试 trace 行为，使用 `tests/conftest.py` 中的共享内存 fixtures

#### `tests/e2e`
- 用于需要真实 AgentInsight 服务器的持久化后端行为
- 优先使用 `tests/support/` 中的有界轮询辅助工具，而非裸 `sleep()` 调用
- `serial_e2e` 仅用于共享服务器并发不安全的测试
- 新 e2e 文件必须命名为 `tests/e2e/test_*.py`
- 不要添加 `e2e_core` / `e2e_data` 标记。CI 通过 `scripts/select_e2e_shard.py` 机械分片 `tests/e2e`

#### `tests/live_provider`
- 使用真实供应商调用，始终作为独立 CI 套件运行
- 除非团队明确更改策略，不要把 `tests/live_provider` 拆分为单独的 smoke 和 extended 任务
- 断言聚焦于稳定的供应商行为，而非脆弱的 observation 数量

### 6.5 测试模式

单元测试通用模式：
1. 创建 `AgentInsight` 客户端实例（使用 `agentinsight_memory_client` fixture）
2. 调用被测方法
3. `client.flush()` 确保 span 被导出
4. 从 `memory_exporter.get_finished_spans()` 获取 span 列表
5. 使用 `get_span()` / `find_spans()` 辅助函数断言 span 名称、属性、父子关系

### 6.6 质量度量指标

| 指标 | 目标值 |
|------|--------|
| 类型检查通过率 | 100%（`mypy agentinsight --no-error-summary` 零错误） |
| 代码风格通过率 | 100%（`ruff check .` + `ruff format .` 零错误） |
| 单元测试通过率 | 100%（所有 Python 版本矩阵） |
| E2E 测试通过率 | 100%（2 分片 + 串行子集） |

### 6.7 测试用户及数据验证
- 使用以下的API Key进行测试
AGENTINSIGHT_SECRET_KEY="sk-lf-8675a592-3d7b-4f2e-bf93-fde30299327e"
AGENTINSIGHT_PUBLIC_KEY="pk-lf-f757665b-53d5-42b1-a759-dfa34eae8386"
AGENTINSIGHT_BASE_URL="https://agent.goldebridge.com"
- 连接Clickhouse数据库（agentinsight.goldebridge.com:8123, clickhouse/AgentIS2026)，验证数据入库及数据准确性
- 如果需要连接LLM，连接本地的Ollama的本地模型deepseek-r1:1.5b
---

## 7. CI 契约

### 7.1 CI 工作流组成

主 CI 工作流 (`ci.yml`) 当前运行：
- **linting**：Python 3.13，`ruff check .`
- **type-checking**：Python 3.13，`mypy agentinsight --no-error-summary`
- **unit-tests**：Python 3.10 - 3.14 矩阵，`pytest -n auto --dist worksteal tests/unit`
- **e2e-tests**：2 个机械分片 + 每分片内串行子集 + live_provider 独立套件
- **PR title validation**：Conventional Commits 格式校验

### 7.2 CI 关键约束

- CI 使用 `AGENTINSIGHT_INIT_*` 环境变量启动 AgentInsight 服务器，除非有充分理由不得更改此路径
- 保持 `cancel-in-progress: true`
- 如需更改 e2e 分片：
  - 更新 `scripts/select_e2e_shard.py`，**不是** `tests/conftest.py` 中的标记路由
  - 确保新的 `tests/e2e/test_*.py` 文件被自动覆盖
  - 保持 `serial_e2e` 为唯一的调度专用 pytest 标记

---

## 8. 安全规则

### 8.1 敏感数据清单

| 场景 | 字段 | 保护方式 |
|------|------|---------|
| 环境变量 | `AGENTINSIGHT_SECRET_KEY` | 仅通过 env var 传入，永不在代码中硬编码 |
| 环境变量 | `AGENTINSIGHT_PUBLIC_KEY` | 同上 |
| CI secrets | `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`HUGGINGFACEHUB_API_TOKEN` | GitHub Secrets 注入 |
| 日志输出 | 密钥/密码 | `EventSerializer` 和错误日志不得序列化或输出密钥原文 |

### 8.2 安全编码铁律

- **禁止**：硬编码密钥/密码/连接字符串 · 在日志中输出密钥 · 提交 `.env` 文件
- **必须**：敏感配置走环境变量 · API 请求使用 HTTPS · Basic Auth 走 httpx 标准认证方式

---

## 9. 提交与 PR 规则

- 提交消息和 PR 标题必须遵循 **Conventional Commits**：`type(scope): description` 或 `type: description`
- 允许的常见类型：`feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`build`、`ci`、`chore`、`revert`、`security`
- 保持提交聚焦且原子化
- 打开 PR 前，自审 diff 并对照 `code_review.md` 中的检查清单
- PR 描述中列出运行过的主要验证命令，并标注跳过的检查及原因

---

## 10. 禁止事项清单

以下事项智能体**严禁执行**，如需执行必须先请求人工介入：

1. ❌ 在代码中硬编码密钥、密码、连接字符串
2. ❌ 手改 `agentinsight/api/` 目录下的任何文件（必须通过 Fern 重新生成）
3. ❌ 删除或减弱现有测试断言来"让测试变绿"
4. ❌ 修改 `_version.py` 中的版本号获取逻辑
5. ❌ 在 CI 工作流中删除 `cancel-in-progress: true`
6. ❌ 更改 `AGENTINSIGHT_INIT_*` 环境变量启动路径（除非有充分理由）
7. ❌ 修改 `pyproject.toml` 中的 `module-root` 或 `build-backend` 配置（除非团队明确决定）
8. ❌ 将 `.env` 或含真实密钥的文件提交到仓库
9. ❌ 使用破坏性 git 命令（如 `git reset --hard`），除非用户明确要求
10. ❌ 撤销无关的工作树修改
11. ❌ 提交 secrets 或 credentials
12. ❌ 修改 `scripts/select_e2e_shard.py` 的分片算法而不相应更新 CI 工作流

---

## 11. 环境设置与质量命令

```bash
uv sync --locked
uv run pre-commit install
uv run --frozen ruff check .
uv run --frozen ruff format .
uv run --frozen mypy agentinsight --no-error-summary
bash scripts/codex/quick-check.sh
```

---

## 12. 发布与文档

```bash
uv build --no-sources
uv run --group docs pdoc -o docs/ --docformat google --logo "https://agent.goldebridge.com/agentinsight_logo.svg" agentinsight
```

发布由 GitHub Actions 处理。不要在仓库说明中构建自定义本地发布流程。

---

## 13. 附录

### 13.1 公共 API 符号速查

| 类别 | 符号 | 说明 |
|------|------|------|
| 主客户端 | `AgentInsight` | 核心 AgentInsight 客户端类 |
| 函数 | `get_client`, `observe`, `propagate_attributes` | 获取客户端 / 装饰器 / 属性传播 |
| Span 类型 | `AgentInsightSpan`, `AgentInsightGeneration`, `AgentInsightEvent`, `AgentInsightAgent`, `AgentInsightTool`, `AgentInsightChain`, `AgentInsightEmbedding`, `AgentInsightEvaluator`, `AgentInsightRetriever`, `AgentInsightGuardrail` | 9 种观察类型 |
| 实验 | `Evaluation`, `RegressionError`, `RunnerContext`, `BatchEvaluationResult`, `BatchEvaluationResumeToken` | 实验与批量评估 |
| Span 过滤 | `is_default_export_span`, `is_langfuse_span`（向后兼容别名）, `is_genai_span`, `is_known_llm_instrumentor` | Span 导出过滤谓词 |
| 属性 | `AgentInsightOtelSpanAttributes` | OTEL Span 属性名常量 |
| 类型 | `ObservationTypeLiteral` | 观察类型字面量 |

### 13.2 核心环境变量

| 变量 | 说明 |
|------|------|
| `AGENTINSIGHT_PUBLIC_KEY` | 项目公钥（必填） |
| `AGENTINSIGHT_SECRET_KEY` | 项目私钥（必填） |
| `AGENTINSIGHT_BASE_URL` | AgentInsight 服务地址（推荐，替代已废弃的 `AGENTINSIGHT_HOST`） |
| `AGENTINSIGHT_FLUSH_AT` | 批量发送 span 的阈值 |
| `AGENTINSIGHT_FLUSH_INTERVAL` | 批量发送间隔（秒） |
| `AGENTINSIGHT_SAMPLE_RATE` | 采样率 |
| `AGENTINSIGHT_TRACING_ENABLED` | 是否启用 tracing |
| `AGENTINSIGHT_TRACING_ENVIRONMENT` | 环境标识 |
| `AGENTINSIGHT_RELEASE` | 发布版本标识 |
| `AGENTINSIGHT_TIMEOUT` | HTTP 请求超时 |
| `AGENTINSIGHT_MEDIA_UPLOAD_ENABLED` | 是否启用媒体上传 |
| `AGENTINSIGHT_MEDIA_UPLOAD_THREAD_COUNT` | 媒体上传线程数 |
| `AGENTINSIGHT_DEBUG` | 调试模式 |
| `AGENTINSIGHT_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED` | 装饰器 I/O 捕获开关 |

### 13.3 E2E 分片权重参考

| 文件 | 历史权重 |
|------|---------|
| `test_core_sdk.py` | 53 |
| `test_batch_evaluation.py` | 41 |
| `test_decorators.py` | 32 |
| `test_prompt.py` | 27 |
| `test_experiments.py` | 17 |
| `test_datasets.py` | 7 |
| `test_media.py` | 1 |

分片算法：贪心装箱，按权重降序分配，每次将文件分配到当前负载最小的分片。

### 13.4 外部文档

- 优先使用官方文档回答产品/API 问题
- OpenAI API 相关问题使用 OpenAI 官方开发者文档
- AgentInsight API 文档：参见 AgentInsight 官方开发者门户
