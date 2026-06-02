[English](#english) | [中文](#中文)

---

<a id="english"></a>

# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.x     | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in AgentInsight Python SDK, please report it responsibly.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:

**agentinsightcn@gmail.com**

Please include the following information in your report:

- Type of vulnerability (e.g., buffer overflow, SQL injection, cross-site scripting)
- Full paths of source file(s) related to the vulnerability
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine the affected versions
2. Audit code to find any potential similar problems
3. Prepare fixes for all supported versions
4. Release patches as soon as possible

## Security Best Practices

When using this SDK:

- **Never commit API keys or secrets** to version control. Use environment variables or secret managers.
- **Use HTTPS** for `base_url` to ensure encrypted communication with the AgentInsight server.
- **Keep dependencies updated** to benefit from the latest security patches.
- **Review the permissions** granted to the API keys used with this SDK.

## Comments on This Policy

If you have suggestions on how this process could be improved, please submit a pull request or open an issue.

---

<a id="中文"></a>

# 安全策略

## 支持的版本

| 版本 | 是否支持          |
| ---- | ----------------- |
| 0.x  | :white_check_mark: |
| < 0.1 | :x:              |

## 报告漏洞

我们非常重视安全漏洞。如果您在 AgentInsight Python SDK 中发现安全漏洞，请负责任地报告。

**请勿通过公开的 GitHub Issues 报告安全漏洞。**

请通过以下邮箱报告：

**agentinsightcn@gmail.com**

请在报告中包含以下信息：

- 漏洞类型（例如：缓冲区溢出、SQL 注入、跨站脚本）
- 与漏洞相关的源文件完整路径
- 受影响源代码的位置（标签/分支/提交或直接 URL）
- 复现问题所需的特殊配置
- 复现问题的详细步骤
- 概念验证或利用代码（如可能）
- 问题的影响，包括攻击者可能如何利用

您应在 48 小时内收到回复。如果由于某种原因未收到，请通过邮件跟进，以确保我们收到了您的原始消息。

## 披露策略

当我们收到安全漏洞报告时，我们将：

1. 确认问题并确定受影响的版本
2. 审计代码以查找任何潜在的类似问题
3. 为所有受支持版本准备修复
4. 尽快发布补丁

## 安全最佳实践

使用此 SDK 时：

- **切勿将 API 密钥或机密提交**到版本控制中。请使用环境变量或密钥管理器。
- **使用 HTTPS** 作为 `base_url`，确保与 AgentInsight 服务器的加密通信。
- **保持依赖更新**，以获得最新的安全补丁。
- **审查权限**，检查与此 SDK 一起使用的 API 密钥所授予的权限。

## 关于此策略的意见

如果您对改进此流程有建议，请提交 Pull Request 或开启 Issue。
