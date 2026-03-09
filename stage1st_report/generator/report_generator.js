/**
 * Stage1st 战报生成器 v3
 * - 修复移动端响应式布局
 * - 过滤词云噪音词
 * - 图片转为base64嵌入HTML
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const CONFIG = {
    threadId: '2275908',
    outputDir: '/workspace/files',
    dataSource: '/workspace/project/stage1st_project/tools/posts_mar9.json',
    maxImages: 8,          // 最多嵌入的图片数量
    maxImageSize: 500000   // 单张图片最大500KB
};

// 需要过滤的噪音词（论坛标识符、小尾巴等）
const NOISE_WORDS = new Set([
    '图片', '来自', '下载次数', '下载附件', '上传', '鹅球', 'Android', 'iOS',
    'iPhone', 'iPad', '手机', '客户端', '浏览器', '版本', '——', '—来自',
    '本帖', '最后编辑', '发表于', '楼', '楼主', '沙发', '板凳', '地板',
    'QUOTE', 'quot', '引用', '回复', '原帖', '由', '于', '被', '编辑',
    'kb', 'KB', 'Mb', 'MB', '附件', '保存', '分享', '收藏', '举报',
    'sign', 'signature', 'tar', 'gzip', 'png', 'jpg', 'jpeg', 'gif', 'webp'
]);

// 表情包域名（需要排除的）
const SMILEY_DOMAINS = ['smiley', 'emoji', 'emoticon', 'static/image/common'];

// 下载图片并转为base64
async function downloadImageAsBase64(url) {
    return new Promise((resolve, reject) => {
        const client = url.startsWith('https') ? https : http;
        const request = client.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://stage1st.com/'
            },
            timeout: 10000
        }, (response) => {
            if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
                // 跟随重定向
                downloadImageAsBase64(response.headers.location).then(resolve).catch(reject);
                return;
            }

            if (response.statusCode !== 200) {
                reject(new Error(`HTTP ${response.statusCode}`));
                return;
            }

            const chunks = [];
            let size = 0;

            response.on('data', (chunk) => {
                size += chunk.length;
                if (size > CONFIG.maxImageSize) {
                    request.destroy();
                    reject(new Error('Image too large'));
                    return;
                }
                chunks.push(chunk);
            });

            response.on('end', () => {
                const buffer = Buffer.concat(chunks);
                const contentType = response.headers['content-type'] || 'image/png';
                const base64 = buffer.toString('base64');
                resolve(`data:${contentType};base64,${base64}`);
            });

            response.on('error', reject);
        });

        request.on('error', reject);
        request.on('timeout', () => {
            request.destroy();
            reject(new Error('Timeout'));
        });
    });
}

async function extractImages(posts) {
    const images = [];
    const urlRegex = /\[图片:(https?:\/\/[^\s\]]+)\]/g;

    for (const post of posts) {
        if (images.length >= CONFIG.maxImages) break;

        const matches = [...post.content.matchAll(urlRegex)];
        for (const match of matches) {
            if (images.length >= CONFIG.maxImages) break;

            const originalUrl = match[1].split(' ')[0];
            // 排除表情包
            if (SMILEY_DOMAINS.some(d => originalUrl.toLowerCase().includes(d))) {
                continue;
            }

            console.log(`[IMG] 下载图片 ${images.length + 1}/${CONFIG.maxImages}: ${originalUrl.substring(0, 50)}...`);

            try {
                const base64 = await downloadImageAsBase64(originalUrl);
                images.push({
                    base64: base64,
                    originalUrl: originalUrl,
                    author: post.author,
                    floor: post.floor,
                    time: post.time
                });
                console.log(`[IMG] ✓ 成功 (${Math.round(base64.length / 1024)}KB)`);
            } catch (e) {
                console.log(`[IMG] ✗ 失败: ${e.message}`);
            }

            // 延迟避免请求过快
            await new Promise(r => setTimeout(r, 300));
        }
    }

    return images;
}

function cleanContent(content) {
    // 移除图片标记
    let cleaned = content.replace(/\[图片:[^\]]+\]/g, '');
    // 移除论坛小尾巴（—— 来自 xxx）
    cleaned = cleaned.replace(/——\s*来自[^\n]*/g, '');
    cleaned = cleaned.replace(/—来自[^\n]*/g, '');
    // 移除签名档
    cleaned = cleaned.replace(/本帖最后由[^\n]*/g, '');
    return cleaned.trim();
}

function analyzePosts(posts) {
    const authorCount = {};
    const allText = posts.map(p => cleanContent(p.content)).join(' ');
    posts.forEach(p => authorCount[p.author] = (authorCount[p.author] || 0) + 1);

    // 关键词提取，过滤噪音词
    const keywordRegex = /[\u4e00-\u9fa5]{2,4}/g;
    const keywords = allText.match(keywordRegex) || [];
    const keywordCount = {};
    keywords.forEach(k => {
        // 过滤噪音词
        if (NOISE_WORDS.has(k)) return;
        // 过滤纯数字
        if (/^\d+$/.test(k)) return;
        keywordCount[k] = (keywordCount[k] || 0) + 1;
    });

    return {
        totalPosts: posts.length,
        uniqueAuthors: Object.keys(authorCount).length,
        authorPostCount: authorCount,
        allText,
        keywords: Object.entries(keywordCount)
            .filter(([k, v]) => v > 1)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 30)
    };
}

function generateInvestmentAdvice(posts, analysis) {
    const text = analysis.allText.toLowerCase();
    const advice = [];

    if (text.includes('油价') || text.includes('石油') || text.includes('原油') || text.includes('炼油') || text.includes('霍尔木兹')) {
        advice.push({ category: '石油/能源', trend: '强烈看多', impact: 'positive', content: '中东冲突升级，能源设施成为攻击目标，霍尔木兹海峡风险加剧。建议关注原油期货、能源ETF。' });
    }
    if (text.includes('黄金') || text.includes('避险')) {
        advice.push({ category: '黄金', trend: '看多', impact: 'positive', content: '地缘政治风险升温，黄金避险需求增加。' });
    }
    if (text.includes('尿素') || text.includes('化肥')) {
        advice.push({ category: '化肥/农产品', trend: '看多', impact: 'positive', content: '能源价格上涨推高化肥成本。' });
    }
    if (text.includes('航运') || text.includes('封锁')) {
        advice.push({ category: '航运', trend: '高风险', impact: 'negative', content: '中东航线保险费率飙升。' });
    }
    if (text.includes('导弹') || text.includes('无人机')) {
        advice.push({ category: '军工', trend: '关注', impact: 'positive', content: '军工订单预期增加。' });
    }
    if (advice.length === 0) {
        advice.push({ category: '综合', trend: '观望', impact: 'neutral', content: '建议保持谨慎。' });
    }
    return advice;
}

function escapeHtml(text) {
    return text.replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m]));
}

function generateHtmlReport(posts, analysis, investmentAdvice, images, outputFile) {
    const today = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
    const dateStr = new Date().toISOString().split('T')[0];
    const timeStr = new Date().toLocaleString('zh-CN');

    const newsItems = posts
        .map(p => ({ ...p, cleanedContent: cleanContent(p.content) }))
        .filter(p => p.cleanedContent.length > 50 && /伊朗|以色列|美国|俄罗斯|导弹|袭击|油价|核/.test(p.cleanedContent))
        .slice(0, 10);
    const hotComments = posts
        .map(p => ({ ...p, cleanedContent: cleanContent(p.content) }))
        .filter(p => p.cleanedContent.length > 30 && p.cleanedContent.length < 200)
        .slice(0, 8);
    const topAuthors = Object.entries(analysis.authorPostCount).sort((a, b) => b[1] - a[1]).slice(0, 10);
    const keywords = analysis.keywords.slice(0, 20);

    const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>S1 战报 | ${today}</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root { --primary-red: #8B0000; --gold: #D4AF37; --dark-bg: #1a1a1a; --light-bg: #f5f5f0; --text-dark: #1a1a1a; --border-color: #ddd; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { overflow-x: hidden; }
        body { font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--light-bg); color: var(--text-dark); line-height: 1.7; overflow-x: hidden; width: 100%; }
        .newspaper { max-width: 1200px; margin: 0 auto; background: #fff; box-shadow: 0 0 30px rgba(0,0,0,0.12); }
        .masthead { background: linear-gradient(135deg, var(--dark-bg) 0%, #2d2d2d 50%, var(--dark-bg) 100%); color: #fff; text-align: center; padding: 25px 15px; }
        .masthead h1 { font-size: clamp(32px, 10vw, 72px); font-weight: 900; letter-spacing: clamp(5px, 3vw, 20px); font-family: 'Noto Serif SC', serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .masthead .subtitle { font-size: clamp(10px, 3vw, 14px); letter-spacing: clamp(3px, 2vw, 8px); margin-top: 10px; color: var(--gold); }
        .masthead .date-line { margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); font-size: clamp(10px, 2.5vw, 13px); letter-spacing: 2px; }
        .nav-bar { background: var(--primary-red); padding: 10px 15px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
        .nav-bar span { color: #fff; font-size: clamp(10px, 2.5vw, 12px); }
        .nav-bar .highlight { color: var(--gold); font-weight: bold; }
        .headline-section { padding: 25px 15px; text-align: center; background: linear-gradient(180deg, #fff 0%, #fafafa 100%); border-bottom: 3px double var(--primary-red); }
        .headline-section h2 { font-size: clamp(24px, 6vw, 42px); color: var(--primary-red); margin-bottom: 12px; font-family: 'Noto Serif SC', serif; }
        .headline-section .lead { font-size: clamp(13px, 3vw, 16px); max-width: 900px; margin: 0 auto; text-align: justify; padding: 0 10px; }
        .stats-bar { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); background: var(--dark-bg); }
        .stat-item { padding: 15px 10px; text-align: center; border-right: 1px solid rgba(255,255,255,0.1); }
        .stat-item:last-child { border-right: none; }
        .stat-number { font-size: clamp(20px, 5vw, 32px); font-weight: bold; color: var(--gold); font-family: 'Noto Serif SC', serif; }
        .stat-label { font-size: clamp(9px, 2vw, 11px); color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 1px; margin-top: 3px; }
        .content-grid { display: grid; grid-template-columns: 1fr; }
        @media (min-width: 900px) { .content-grid { grid-template-columns: 2fr 1fr; } }
        .main-content { padding: 20px 15px; border-bottom: 1px solid var(--border-color); }
        @media (min-width: 900px) { .main-content { border-bottom: none; border-right: 1px solid var(--border-color); padding: 30px; } }
        .sidebar { padding: 20px 15px; background: #fafafa; }
        @media (min-width: 900px) { .sidebar { padding: 25px; } }
        .section-header { font-size: clamp(18px, 4vw, 22px); color: var(--primary-red); padding-bottom: 10px; border-bottom: 3px double var(--primary-red); margin-bottom: 20px; font-family: 'Noto Serif SC', serif; }
        .news-item { margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px dotted #ccc; word-wrap: break-word; overflow-wrap: break-word; }
        .news-item:last-child { border-bottom: none; margin-bottom: 0; }
        .news-item h3 { font-size: clamp(14px, 3vw, 16px); margin-bottom: 8px; line-height: 1.4; }
        .news-item .tag { background: var(--primary-red); color: #fff; font-size: 9px; padding: 2px 6px; margin-right: 8px; display: inline-block; }
        .news-item p { font-size: clamp(13px, 3vw, 14px); text-align: justify; line-height: 1.8; word-wrap: break-word; overflow-wrap: break-word; }
        .news-item .source { font-size: 11px; color: #999; font-style: italic; margin-top: 8px; }
        .images-section { margin-bottom: 25px; }
        .images-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; margin-top: 15px; }
        .image-item { position: relative; border-radius: 8px; overflow: hidden; background: #f0f0f0; }
        .image-item img { width: 100%; height: 120px; object-fit: cover; display: block; cursor: pointer; transition: transform 0.3s; }
        .image-item img:hover { transform: scale(1.05); }
        .image-item .image-info { font-size: 10px; color: #666; padding: 5px; background: #f9f9f9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .investment-box { background: linear-gradient(135deg, #0d1f2d 0%, #1a3a4a 100%); color: #fff; padding: 18px; margin-bottom: 20px; border-radius: 5px; }
        .investment-box h3 { color: var(--gold); font-size: clamp(14px, 3vw, 18px); margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid var(--gold); }
        .investment-item { margin-bottom: 12px; padding: 10px 12px; background: rgba(255,255,255,0.05); border-left: 3px solid var(--gold); }
        .investment-item .category { font-size: clamp(10px, 2vw, 12px); color: var(--gold); letter-spacing: 1px; margin-bottom: 4px; }
        .investment-item p { font-size: clamp(12px, 2.5vw, 13px); color: rgba(255,255,255,0.9); }
        .investment-item .impact { font-size: 10px; padding: 2px 8px; background: #c00; color: #fff; display: inline-block; margin-top: 6px; border-radius: 3px; }
        .investment-item .impact.positive { background: linear-gradient(135deg, #2e7d32, #43a047); }
        .investment-item .impact.negative { background: linear-gradient(135deg, #c62828, #e53935); }
        .comment { padding: 12px; background: #f9f9f9; margin-bottom: 12px; border-left: 3px solid #ccc; word-wrap: break-word; overflow-wrap: break-word; }
        .comment.highlighted { border-left-color: var(--primary-red); background: #fff8f0; }
        .comment .author { font-size: 11px; color: var(--primary-red); font-weight: bold; }
        .comment .content { font-size: clamp(12px, 2.5vw, 13px); margin-top: 6px; line-height: 1.6; }
        .keywords { margin-top: 20px; padding: 12px; background: #f0f0f0; border-radius: 5px; }
        .keywords h4 { font-size: 12px; color: var(--primary-red); margin-bottom: 10px; }
        .keywords .tag-cloud { display: flex; flex-wrap: wrap; gap: 6px; }
        .keywords .tag { background: var(--dark-bg); color: #fff; padding: 3px 10px; font-size: 10px; border-radius: 3px; }
        .keywords .tag.hot { background: var(--primary-red); }
        .footer { background: var(--dark-bg); color: #fff; padding: 25px 15px; text-align: center; }
        .footer h3 { font-size: clamp(18px, 4vw, 24px); letter-spacing: 5px; margin-bottom: 8px; color: var(--gold); }
        .footer .disclaimer { font-size: 10px; color: rgba(255,255,255,0.4); margin-top: 15px; line-height: 1.6; padding: 0 10px; }
        .author-table { width: 100%; font-size: 11px; border-collapse: collapse; }
        .author-table th, .author-table td { padding: 5px; text-align: left; }
        .author-table th { background: #f5f5f5; }
        .author-table tr:nth-child(even) { background: #fafafa; }
    </style>
</head>
<body>
    <div class="newspaper">
        <header class="masthead">
            <h1>S1 战报</h1>
            <div class="subtitle">S1 OBSERVER | 中东局势深度观察</div>
            <div class="date-line">${today} | 帖子: #${CONFIG.threadId} | ${analysis.totalPosts}条回复</div>
        </header>
        <nav class="nav-bar">
            <span>参与: <span class="highlight">${analysis.uniqueAuthors}</span>人</span>
            <span>${dateStr}</span>
            <span>Stage1st 论坛</span>
        </nav>
        <section class="headline-section">
            <h2>中东局势战报</h2>
            <p class="lead">基于Stage1st论坛专楼实时数据，涵盖最新战况、论坛热评及金融投资建议。${analysis.totalPosts}条回复，${analysis.uniqueAuthors}位用户参与。生成时间: ${timeStr}</p>
        </section>
        <div class="stats-bar">
            <div class="stat-item"><div class="stat-number">${analysis.totalPosts}</div><div class="stat-label">回复</div></div>
            <div class="stat-item"><div class="stat-number">${analysis.uniqueAuthors}</div><div class="stat-label">用户</div></div>
            <div class="stat-item"><div class="stat-number">${keywords.length}</div><div class="stat-label">关键词</div></div>
            <div class="stat-item"><div class="stat-number">${images.length}</div><div class="stat-label">图片</div></div>
            <div class="stat-item"><div class="stat-number">${investmentAdvice.length}</div><div class="stat-label">建议</div></div>
        </div>
        <div class="content-grid">
            <main class="main-content">
                <h2 class="section-header">📊 最新动态</h2>
                ${newsItems.map(item => `<article class="news-item"><h3><span class="tag">动态</span>${escapeHtml(item.cleanedContent.substring(0, 45))}...</h3><p>${escapeHtml(item.cleanedContent.substring(0, 280))}${item.cleanedContent.length > 280 ? '...' : ''}</p><div class="source">—— ${escapeHtml(item.author)} (${item.floor || '?'}楼)</div></article>`).join('')}

                ${images.length > 0 ? `
                <h2 class="section-header">🖼️ 论坛图片</h2>
                <div class="images-grid">
                    ${images.map(img => `<div class="image-item"><a href="${escapeHtml(img.originalUrl)}" target="_blank" rel="noopener noreferrer"><img src="${img.base64}" alt="论坛图片" loading="lazy"></a><div class="image-info">${escapeHtml(img.author)} (${img.floor || '?'}楼)</div></div>`).join('')}
                </div>
                <p style="font-size: 11px; color: #999; margin-top: 8px;">点击图片查看原图 | 共 ${images.length} 张</p>
                ` : ''}

                <h2 class="section-header">💬 热门评论</h2>
                ${hotComments.map((c, i) => `<div class="comment ${i < 3 ? 'highlighted' : ''}"><span class="author">${escapeHtml(c.author)} (${c.floor || '?'}楼):</span><p class="content">${escapeHtml(c.cleanedContent)}</p></div>`).join('')}
            </main>
            <aside class="sidebar">
                <div class="investment-box">
                    <h3>💰 投资建议</h3>
                    ${investmentAdvice.map(adv => `<div class="investment-item"><div class="category">${adv.category} - ${adv.trend}</div><p>${adv.content}</p><span class="impact ${adv.impact}">${adv.impact === 'positive' ? '看多' : adv.impact === 'negative' ? '看空' : '中性'}</span></div>`).join('')}
                </div>
                <div class="keywords">
                    <h4>🏷️ 关键词</h4>
                    <div class="tag-cloud">${keywords.map((kw, i) => `<span class="tag ${i < 5 ? 'hot' : ''}">${kw[0]}</span>`).join('')}</div>
                </div>
                <div style="margin-top: 20px; padding: 12px; background: #fff; border-radius: 5px; border: 1px solid var(--border-color);">
                    <h4 style="font-size: 13px; color: var(--primary-red); margin-bottom: 10px; border-bottom: 2px solid var(--primary-red); padding-bottom: 6px;">👥 活跃用户</h4>
                    <table class="author-table">
                        <tr><th>#</th><th>用户</th><th>发言</th></tr>
                        ${topAuthors.map((entry, i) => `<tr><td>${i + 1}</td><td>${escapeHtml(entry[0])}</td><td style="text-align:center">${entry[1]}</td></tr>`).join('')}
                    </table>
                </div>
            </aside>
        </div>
        <footer class="footer">
            <h3>S1 OBSERVER</h3>
            <p style="color: rgba(255,255,255,0.6); font-size: 12px;">中东局势深度观察 | Stage1st 论坛 #${CONFIG.threadId}</p>
            <div class="disclaimer">免责声明：本战报内容整理自网络论坛，仅供信息参考。投资建议仅供参考，不构成决策依据。Generated by Claude Code | ${timeStr}</div>
        </footer>
    </div>
</body>
</html>`;

    fs.mkdirSync(path.dirname(outputFile), { recursive: true });
    fs.writeFileSync(outputFile, html, 'utf-8');
    console.log(`[OK] HTML战报已生成: ${outputFile}`);
    console.log(`[OK] 提取图片: ${images.length}张`);
    console.log(`[OK] 关键词过滤后: ${keywords.length}个`);
    return outputFile;
}

// Main
async function main() {
    console.log('='.repeat(60));
    console.log('Stage1st 战报生成器 v3');
    console.log(`运行时间: ${new Date().toLocaleString('zh-CN')}`);
    console.log('='.repeat(60));

    let posts = [];
    if (fs.existsSync(CONFIG.dataSource)) {
        console.log(`\n[LOAD] 从 ${CONFIG.dataSource} 加载数据...`);
        posts = JSON.parse(fs.readFileSync(CONFIG.dataSource, 'utf-8'));
        console.log(`[OK] 加载了 ${posts.length} 条回复`);
    } else {
        console.log(`[WARN] 数据文件不存在`);
        posts = [{ author: '示例', content: '测试内容', floor: '1', time: '2026-03-09' }];
    }

    // 提取图片（异步下载并转base64）
    console.log('\n[IMG] 下载并转换图片为Base64...');
    const images = await extractImages(posts);
    console.log(`[OK] 成功获取 ${images.length} 张图片`);

    // 分析
    const analysis = analyzePosts(posts);
    console.log(`[STAT] 总回复: ${analysis.totalPosts}, 参与用户: ${analysis.uniqueAuthors}`);
    console.log(`[KEYWORDS] 过滤后关键词: ${analysis.keywords.slice(0, 10).map(k => k[0]).join(', ')}`);

    const investmentAdvice = generateInvestmentAdvice(posts, analysis);
    const outputFile = path.join(CONFIG.outputDir, `Battle_Report_${new Date().toISOString().split('T')[0]}.html`);
    generateHtmlReport(posts, analysis, investmentAdvice, images, outputFile);

    console.log('\n[DONE] 战报生成完成!');
    console.log(`[FILE] ${outputFile}`);
}

main().catch(console.error);
