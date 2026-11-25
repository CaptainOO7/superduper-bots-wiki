# SuperDuper Bots Wiki

Public user guides and operations reference. Markdown lives under `docs/`.
The Wiki builds independently of the private product source, DSH, Feishu, and model services.

Use `corepack pnpm install --frozen-lockfile`, then `corepack pnpm build`.
See [deployment](docs/deployment/index.md) for local development and self-hosting.

Documentation is licensed under CC BY 4.0. Build, test, and deployment code is MIT licensed.

## Preview publication

The Pages workflow reads open, same-repository Draft PRs from the configured Writer App. It retrieves the FAQ Markdown at the exact head SHA and builds it with trusted `main` code. The preview accepts only the FAQ file and a restricted prose grammar. It uses the production site's theme and navigation, and the candidate cannot supply scripts, links, HTML, Vue expressions, frontmatter, or workflow code.

Each successful publication reconstructs all eligible previews and the production site together. Closing a PR removes its preview on the next deployment. The `previews/pr-N/candidate.json` marker records the commit; a mismatch means the online preview is stale. The preview mechanism stays disabled until a repository administrator sets `WIKI_PREVIEW_WRITER` to the authorized App identity.
