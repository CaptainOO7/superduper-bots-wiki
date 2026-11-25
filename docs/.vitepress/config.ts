import { defineConfig } from 'vitepress'

const words = new Intl.Segmenter('zh', { granularity: 'word' })
const tokenize = (text: string) => {
  const separated = [...words.segment(text)].filter(word => word.isWordLike).map(word => word.segment)
  const han = text.match(/\p{Script=Han}{2,}/gu) ?? []
  const pairs = han.flatMap(term => Array.from(term).slice(1).map((char, index) => Array.from(term)[index] + char))
  return [...new Set([...separated, ...pairs])]
}
export default defineConfig({
  title: 'SuperDuper Bots',
  description: 'Super Agent 用户指南与运维知识库',
  lang: 'zh-CN',
  base: process.env.WIKI_BASE || '/',
  cleanUrls: false,
  themeConfig: {
    search: { provider: 'local', options: { miniSearch: {
      options: { tokenize },
      searchOptions: { tokenize },
    } } },
    nav: [{ text: '入门', link: '/getting-started/' }, { text: '常见问题', link: '/faq/' }],
    sidebar: [
      { text: '入门', items: [{ text: '产品与要求', link: '/getting-started/' }, { text: '安装与自托管', link: '/deployment/' }] },
      { text: '使用与管理', items: [{ text: '飞书任务', link: '/user-guide/' }, { text: '服务与恢复', link: '/administration/' }] },
      { text: '参考', items: [{ text: '常见问题', link: '/faq/' }, { text: '故障排查', link: '/troubleshooting/' }, { text: '术语', link: '/glossary' }, { text: '已知限制', link: '/known-limitations' }] },
    ],
  },
})
