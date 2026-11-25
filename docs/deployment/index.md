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
