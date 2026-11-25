# 产品与系统要求

适用版本：M1.5-01。

SuperDuper Bots 是基于 DeepSeek DSH 的独立产品。DSH 提供会话、模型接入与 Web 容器。Super Agent 负责在飞书原讨论中澄清需求、冻结 Proposal、等待人工审批，并在隔离环境中实现和测试候选变更。

已验证的运行平台是 macOS，使用 Node.js 24、Docker Desktop、Git、Python 3、launchd 和固定版本的 DSH Harness。运行环境需要经管理员授权的飞书机器人与目标群、GitHub 身份和可用模型额度。仓库权限与任务审批是独立的检查。

Product source is the runtime distribution. The business target is the repository whose files a particular approved task may change. Repository identity is a stable provider ID.
