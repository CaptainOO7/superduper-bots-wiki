# GitHub Pages 与产品部署

适用版本：Wiki 初始版本、产品 M1.5-01。

## Wiki 本地开发

安装 Node.js 与 Corepack。从 Wiki 仓库根目录执行：

```sh
corepack pnpm install --frozen-lockfile
corepack pnpm dev
```

## 官网与静态构建

[官方 Wiki](https://captainoo7.github.io/superduper-bots-wiki/) 由 GitHub Actions 构建并发布到 GitHub Pages。Wiki 使用 VitePress 静态输出，无需独立服务器、数据库、DSH 或模型凭据。

运行 `WIKI_BASE=/superduper-bots-wiki/ corepack pnpm build` 可复现官网基础路径的静态构建。输出位于 `docs/.vitepress/dist/`。在本地可使用 `corepack pnpm dev`。静态产物也可放到其他服务器，构建时按实际挂载路径设置 `WIKI_BASE`。仓库中的 Wiki Docker 配置是可选资产，本候选版未验证该构建。产品隔离 Worker 仍需要 Docker。

## 产品安装

适用版本：SuperDuper Bots 0.2.0-rc.1 候选版。受管产品部署支持 macOS，需要 Docker Desktop、Git、Python 3.12 或更高版本、Node 24 和 Corepack。由维护者获取经审查的产品源，业务身份只用于授权目标仓库。准备独立的私有 release 根目录和状态目录。

从已审查的产品检出运行以下命令。将示例目录、服务标签和端口替换为自己的独立参数。

```sh
release_root="$HOME/.local/share/sdb-example-release"
state_dir="$HOME/.local/share/sdb-example-state"
reviewed_commit="$(git rev-parse HEAD)"
mkdir -m 700 "$state_dir"
scripts/superduper-bots --root "$release_root" install "$reviewed_commit" --repo "$PWD" --prepare-worker
scripts/superduper-bots --root "$release_root" verify "$reviewed_commit"
scripts/superduper-bots --root "$release_root" configure --state "$state_dir" --label local.superduper-bots.example --port 3085
scripts/superduper-bots --root "$release_root" activate "$reviewed_commit"
scripts/superduper-bots --root "$release_root" setup
```

流程保持服务停止。也可用 `setup --profile PATH` 导入经审查的主机私有配置。启动前确认同一 Bot 只有一个事件消费者。

## 向导与账号

在飞书开放平台准备能在批准群组读取和回复消息的机器人，并配置消息事件。指定请求者和审批者。在主机私有目录管理 Bot 包装程序和凭据。

向导支持 GitHub 双 App、单 App 分别签发限权令牌、细粒度 PAT、以及匿名读取配合已认证的 App Writer。每个角色使用独立的主机适配器入口。双 App 提供独立的根凭据。单 App 共用根凭据。PAT 实际权限由 GitHub 授予，不能仅靠只读探测断言具备写入权限。匿名 Reader 只适用于公开仓库。使用目标稳定仓库 ID 和默认分支，保持 Source 与 Target 分离。

设置可写路径、登记测试及其 SHA-256、隔离 Worker 镜像及授权记录。选择模型资源模式、每任务及每次 Assignment 的有限调用上限。可选择已验证的 BigModel 部署，或配置经审查的 OpenAI 兼容端点、模型及请求上限。凭据文件留在主机。免凭据端点须显式配置。其他模型端点的兼容验证使用夹具。

遗留受控模式仍要求当前资源证据。独立模式使用对应的授权和账本。启动前确认模型资源与计费边界。
