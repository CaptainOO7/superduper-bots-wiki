# 服务、用量与恢复

适用版本：SuperDuper Bots 0.2.0-rc.1 候选版。

从已审查的产品检出运行 `scripts/superduper-bots --root PATH COMMAND`。将 PATH 替换为你的 release 根目录。先练习只读检查，再进行会改变服务状态的操作。

| 命令 | 用途 |
| --- | --- |
| `status` / `doctor` | 检查安装、依赖、授权、loaded 与逐项 health |
| `logs` | 查看保留日志计数及健康摘要 |
| `web` | 打开本机认证 Dashboard；保护认证链接 |
| `start` / `stop` / `restart` | 控制该实例，保持同一 Bot 的消费独占 |
| `verify COMMIT` | 校验不可变发布文件 |
| `backup` | 停服后生成私有 SQLite 快照、注册和持久数据副本 |
| `restore DIRECTORY` | 验证同一部署、版本、账本和交付记录 |
| `upgrade COMMIT --repo PATH` / `rollback COMMIT` | 选择已验证且与现有状态相容的发布 |

## 模型资源

Enforced 按累计额度和预留控制调用。Monitor 记录使用并显示阈值。Unlimited 不设累计上限，仍记录用量并执行有限的每 Ticket 和 Assignment 请求上限。未知结果保持预留，直至核对有效提供方凭证。Dashboard 的 modelGovernance 报告当前模式和阈值。管理命令的 modelResources 报告记账用量及待核对请求。

经授权的管理员在停服后使用私有证据文件运行 `config --reconcile-usage PATH`。独立策略变更使用 `config --resource-policy PATH`，要求静止状态和新授权；已消耗用量仍保留。

## 执行额度阻塞

只有明确因请求上限停下，且无候选结果、未决交付、未决用量或 Worker 租约的初始 Assignment 可走一次性恢复。停止独立服务，审查原审批、已记账用量与新授权，通过 `config --recover-execution PATH` 提交私有许可。运行时在同一 Ticket 上创建新一代 Assignment，保留旧用量及历史。普通中断与含糊交付须单独核对。

## 升级与回退

升级前保留已验证 release、私有配置、SQLite 快照、受信测试和外部回执。凭据与供应方证据分别私下备份。只有缺失的 DSH 持久目录可通过停服后的 `restore DIRECTORY --recover-persistence` 直接补回。若业务数据库与用量或交付回执存在差异，先由管理员逐项对账。使用当前审查通过的 CLI 进行版本选择；包含执行恢复许可的状态不能回退到缺少该能力的版本。

切换目标前先结束当前工作、处理未决回执并退役活跃话题。使用 `config --switch-target PATH` 提交新授权，原仓库审批保持历史绑定，账本沿用。
