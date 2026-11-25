# 服务、用量与恢复

适用版本：M1.5-01。

- 使用 `superduper-bots status` 检查运行状态。预期历史回填暂停的环境中，实时 Feishu 状态仍应报告就绪。
- 使用 `superduper-bots restart` 重启受管实例。确认只有一个实例消费同一机器人的事件。
- Dashboard 由 DSH 认证。会话到期时通过管理员提供的本机认证流程重新登录。将登录链接视为凭据。
- 模型额度以持久化账本为准。用量未知的请求保留预留额度，额度不足时停止调用。
- 升级前先保存经完整性校验的 SQLite 在线备份、私有配置、DSH 持久数据和上一版本的发布清单。
- 在恢复旧状态前，核对快照之后发生的外部投递、审批和用量。恢复不能归还已消耗额度，也不能重放已完成投递。

Backup and recovery require reconciling the usage ledger and external receipts before resuming service.

## 候选版目标切换

暂停迁移工作并停止当前实例。先核查是否存在未决任务、活跃话题或交付回执。用单独授权的新 profile 和两个目标专用 App 运行 `config --switch-target`。核查新仓库的稳定 ID、默认分支和授权版本。原审批仍绑定旧仓库，历史任务保持原记录；预算沿用当前账本。

## 候选版运维流程

使用 `doctor` 检查本机依赖、注册和授权状态。使用 `web` 在当前设备打开认证 Dashboard。使用 `logs` 查看不含原始日志文本的状态摘要。停服后使用 `backup` 备份 SQLite、DSH 持久数据和注册文件。独立的凭据和资源证据由维护者另外备份。

使用 `verify` 校验发布文件，使用 `upgrade` 或 `rollback` 选择兼容版本。使用 `restore` 检查快照归属和账本差异。发现状态差异时先逐条对账，再按该版本恢复手册处理。保持可回退的 release 和外部投递回执。
