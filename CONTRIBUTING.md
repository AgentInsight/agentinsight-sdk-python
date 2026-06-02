[English](#english) | [中文](#中文)

---

<a id="english"></a>

# Contributing Guide

## Development

### Install Dependencies

```bash
uv sync --locked
```

### Add Pre-commit Hooks

```bash
uv run pre-commit install
```

### Quality Checks

```bash
uv run --frozen ruff check .
uv run --frozen ruff format .
uv run --frozen mypy agentinsight --no-error-summary
```

### Testing

Unit tests do not require a running AgentInsight server:

```bash
uv run --frozen pytest -n auto --dist worksteal tests/unit
```

E2E tests require a running AgentInsight server and environment variables configured per `.env.template`:

```bash
uv run --frozen pytest -n 4 --dist worksteal tests/e2e -m "not serial_e2e"
uv run --frozen pytest tests/e2e -m "serial_e2e"
```

Provider tests require real provider API calls and corresponding API keys:

```bash
uv run --frozen pytest -n 4 --dist worksteal tests/live_provider -m "live_provider"
```

Run a single test:

```bash
uv run --frozen pytest tests/unit/test_resource_manager.py::test_pause_signals_score_consumer_shutdown
```

## Pull Requests

PR titles and commit messages must follow the Conventional Commits specification:

```text
type(scope): description
type: description
```

Common types include `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`, and `security`.

Before submitting a PR:

- Self-review your diff and check against the repository checklist.
- Keep changes focused and avoid unrelated refactoring.
- Add or update tests for behavioral changes.
- List the verification commands you ran in the PR description.

### Updating the OpenAPI Specification

The auto-generated API client in `agentinsight/api/` must not be manually edited. It must be regenerated from the upstream Fern/OpenAPI source.

### Releasing a Version

Version releases are automated through GitHub Actions using PyPI Trusted Publishing (OIDC).

To create a release:

1. Go to [Actions > Release Python SDK](https://github.com/AgentInsight/agentinsight-sdk-python/actions/workflows/release.yml)
2. Click "Run workflow"
3. Select the version increment type:
   - `patch` - Bug fixes (1.0.0 → 1.0.1)
   - `minor` - New features (1.0.0 → 1.1.0)
   - `major` - Breaking changes (1.0.0 → 2.0.0)
   - `prepatch`, `preminor`, or `premajor` - Pre-release versions (e.g., 1.0.0 → 1.0.1a1)
4. For pre-release versions, select the type: `alpha`, `beta`, or `rc`
5. Click "Run workflow"

The workflow will automatically:
- Increment the version number in `pyproject.toml`
- Build the package
- Publish to PyPI
- Create a git tag and GitHub release with auto-generated release notes

### SDK Reference Documentation

Note: The auto-generated SDK reference documentation is still being improved.

SDK reference documentation is generated via pdoc. The docs dependency group is installed on demand when running documentation commands.

To update the reference documentation, run:

```sh
uv run --group docs pdoc -o docs/ --docformat google --logo "https://agent.goldebridge.com/agentinsight_logo.svg" agentinsight
```

To run the reference documentation locally:

```sh
uv run --group docs pdoc --docformat google --logo "https://agent.goldebridge.com/agentinsight_logo.svg" agentinsight
```

## Acknowledgements

This project is built upon and evolved from the [Langfuse Python SDK](https://github.com/langfuse/langfuse-python). We thank the Langfuse team for their excellent work. The Langfuse Python SDK is released under the MIT License.

The Langfuse Python SDK itself is built upon the [PostHog Python SDK](https://github.com/PostHog/posthog-python). We thank the PostHog team for their contributions.

---

<a id="中文"></a>

# 贡献指南

## 开发

### 安装依赖

```bash
uv sync --locked
```

### 添加 pre-commit

```bash
uv run pre-commit install
```

### 质量检查

```bash
uv run --frozen ruff check .
uv run --frozen ruff format .
uv run --frozen mypy agentinsight --no-error-summary
```

### 测试

单元测试不需要运行中的 AgentInsight 服务端：

```bash
uv run --frozen pytest -n auto --dist worksteal tests/unit
```

E2E 测试需要运行中的 AgentInsight 服务端，并根据 `.env.template` 配置环境变量：

```bash
uv run --frozen pytest -n 4 --dist worksteal tests/e2e -m "not serial_e2e"
uv run --frozen pytest tests/e2e -m "serial_e2e"
```

供应商测试需要真实的供应商 API 调用及对应的 API 密钥：

```bash
uv run --frozen pytest -n 4 --dist worksteal tests/live_provider -m "live_provider"
```

运行单个测试：

```bash
uv run --frozen pytest tests/unit/test_resource_manager.py::test_pause_signals_score_consumer_shutdown
```

## Pull Request

PR 标题和提交消息必须遵循 Conventional Commits 规范：

```text
type(scope): description
type: description
```

常见类型包括 `feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`build`、`ci`、`chore`、`revert` 和 `security`。

提交 PR 前：

- 自审 diff 并对照仓库检查清单。
- 保持改动聚焦，避免无关重构。
- 为行为变更添加或更新测试。
- 在 PR 描述中列出运行过的验证命令。

### 更新 OpenAPI 规范

`agentinsight/api/` 中的自动生成 API 客户端禁止手动编辑，必须通过上游 Fern/OpenAPI 源重新生成。

### 发布版本

版本发布通过 GitHub Actions 使用 PyPI Trusted Publishing (OIDC) 自动化完成。

创建发布：

1. 前往 [Actions > Release Python SDK](https://github.com/AgentInsight/agentinsight-sdk-python/actions/workflows/release.yml)
2. 点击 "Run workflow"
3. 选择版本号递增类型：
   - `patch` - 缺陷修复 (1.0.0 → 1.0.1)
   - `minor` - 新功能 (1.0.0 → 1.1.0)
   - `major` - 破坏性变更 (1.0.0 → 2.0.0)
   - `prepatch`、`preminor` 或 `premajor` - 预发布版本（例如 1.0.0 → 1.0.1a1）
4. 对于预发布版本，选择类型：`alpha`、`beta` 或 `rc`
5. 点击 "Run workflow"

工作流将自动执行以下操作：
- 在 `pyproject.toml` 中递增版本号
- 构建包
- 发布到 PyPI
- 创建 git 标签和 GitHub release，并自动生成发布说明

### SDK 参考文档

注意：自动生成的 SDK 参考文档目前仍在完善中。

SDK 参考文档通过 pdoc 生成。docs 依赖组在运行文档命令时按需安装。

更新参考文档，运行以下命令：

```sh
uv run --group docs pdoc -o docs/ --docformat google --logo "https://agent.goldebridge.com/agentinsight_logo.svg" agentinsight
```

在本地运行参考文档，可以使用以下命令：

```sh
uv run --group docs pdoc --docformat google --logo "https://agent.goldebridge.com/agentinsight_logo.svg" agentinsight
```

## 致谢

本项目基于 [Langfuse Python SDK](https://github.com/langfuse/langfuse-python) 构建并演化而来，感谢 Langfuse 团队的出色工作。Langfuse Python SDK 采用 MIT 许可证发布。

Langfuse Python SDK 本身基于 [PostHog Python SDK](https://github.com/PostHog/posthog-python) 构建，感谢 PostHog 团队的贡献。
