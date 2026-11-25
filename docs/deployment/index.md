# 部署与自托管

适用版本：Wiki 初始版本、产品 M1.5-01。

## Wiki 本地开发

安装 Node.js 与 Corepack。从 Wiki 仓库根目录执行：

```sh
corepack pnpm install --frozen-lockfile
corepack pnpm dev
```

## 静态部署

运行 `corepack pnpm build`，将 `docs/.vitepress/dist/` 发布到静态 Web 服务器。若服务器使用子路径，构建时设置 `WIKI_BASE=/your-path/`。GitHub Pages 使用项目子路径。

## Docker

运行 `docker compose up --build` 后访问本机 4173 端口。Wiki 无需 DSH、飞书、模型凭据或产品状态。仅对本机开放端口是默认行为。

## 产品安装

M1.5-01 的版本化发布管理需要授权访问产品源和部署运行手册。独立安装器与向导通过验收后，本页会补充对应版本的操作流程。

## 独立部署候选版

以下流程适用于正在验收的 M1.5 候选版，已在隔离的 macOS 目录中使用夹具验证。真实飞书和模型验收仍待完成。

1. 使用维护者身份获取已审查的私有产品版本。业务 Reader 与 Writer 只安装在获批的目标仓库。
2. 创建私有状态目录，使用 `superduper-bots install` 准备不可变 release 和 Worker 镜像。
3. 使用 `configure` 注册独立服务，然后用 `activate` 选择已验证版本。现有实例继续使用自己的端口和状态目录。
4. 使用 `setup` 进入向导，或使用 `setup --profile` 导入经审查的私有 profile。部署维护者可查阅产品版本随附的完整命令参数。
5. 在准备好飞书、GitHub、当前模型证据和单独授权后才启动服务。

## 准备飞书机器人

在飞书开放平台创建或选择经管理员授权的机器人。配置接收消息事件及所需读写权限。将机器人加入批准的群，区分允许提交请求的人和允许审批的人。将凭据保存在主机私有目录。使用独立机器人可避免两个环境同时消费同一事件。

## 配置模型

当前候选版使用 BigModel 的 glm-5.3-flash。向导需要本机私有密钥文件的路径。启动前需要当前资源证据和独立预算授权。服务状态与模型可用额度分别检查。当前验证流程不支持自动充值或续期。
