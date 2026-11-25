# 服务、用量与恢复

适用版本：M1.5-01。

- 使用 `superduper-bots status` 检查运行状态。预期历史回填暂停的环境中，实时 Feishu 状态仍应报告就绪。
- 使用 `superduper-bots restart` 重启受管实例。确认只有一个实例消费同一机器人的事件。
- Dashboard 由 DSH 认证。会话到期时通过管理员提供的本机认证流程重新登录。将登录链接视为凭据。
- 模型额度以持久化账本为准。用量未知的请求保留预留额度，额度不足时停止调用。
- 升级前先保存经完整性校验的 SQLite 在线备份、私有配置、DSH 持久数据和上一版本的发布清单。
- 在恢复旧状态前，核对快照之后发生的外部投递、审批和用量。恢复不能归还已消耗额度，也不能重放已完成投递。

Backup and recovery require reconciling the usage ledger and external receipts before resuming service.
