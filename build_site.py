import json

with open(r'C:\Users\Administrator/AccioWork/2026-07-04-16-44-08/catalog_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cats = data['categories']
cat_order = sorted(cats.keys(), key=lambda k: -len(cats[k]))

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

pages = []

# ===== index.html =====
index = []
index.append('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yinxiyangjia Tools — Power Tools & Hardware Wholesale Catalog</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0a0e14;
  --surface: #131820;
  --surface2: #1a212e;
  --border: #252d3a;
  --text: #e2e6ed;
  --text2: #8b95a5;
  --text3: #5c6675;
  --accent: #3b82f6;
  --accent2: #1d4ed8;
  --red: #ef4444;
  --green: #22c55e;
  --amber: #f59e0b;
  --card-radius: 12px;
  --max-w: 1280px;
}
* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior: smooth; }
body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
a { color: inherit; text-decoration: none; }

/* Top Bar */
.topbar { position: fixed; top:0; left:0; right:0; z-index:100; background: rgba(10,14,20,0.92); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); }
.topbar-inner { max-width: var(--max-w); margin:0 auto; display:flex; align-items:center; justify-content:space-between; padding:0 24px; height:56px; }
.logo { font-weight:800; font-size:18px; letter-spacing: -0.5px; }
.logo span { color: var(--accent); }
.topbar-links { display:flex; gap:6px; align-items:center; }
.topbar-links a { padding:6px 14px; border-radius:8px; font-size:13px; font-weight:500; color: var(--text2); transition: all 0.15s; }
.topbar-links a:hover { color: var(--text); background: var(--surface2); }
.topbar-links .btn-store { background: var(--accent); color: #fff; }
.topbar-links .btn-store:hover { background: var(--accent2); }

/* Hero */
.hero { padding: 120px 24px 80px; text-align:center; max-width:800px; margin:0 auto; }
.hero .badge { display:inline-block; background: rgba(59,130,246,0.12); color:var(--accent); padding:4px 14px; border-radius:20px; font-size:12px; font-weight:600; letter-spacing:0.5px; margin-bottom:24px; }
.hero h1 { font-size:clamp(32px,5vw,56px); font-weight:800; letter-spacing:-1.5px; line-height:1.1; margin-bottom:20px; }
.hero h1 span { background: linear-gradient(135deg, var(--accent), #8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero p { font-size:17px; color:var(--text2); max-width:560px; margin:0 auto 32px; }
.hero-stats { display:flex; gap:40px; justify-content:center; flex-wrap:wrap; }
.hero-stats .stat { text-align:center; }
.hero-stats .stat .num { font-size:36px; font-weight:700; letter-spacing:-1px; }
.hero-stats .stat .lbl { font-size:13px; color:var(--text2); margin-top:2px; }

/* Section */
.section { max-width: var(--max-w); margin:0 auto; padding:0 24px; }
.section-title { font-size:24px; font-weight:700; margin-bottom:6px; letter-spacing:-0.5px; }
.section-sub { color:var(--text2); font-size:14px; margin-bottom:32px; }

/* Category Nav */
.cat-nav { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:40px; }
.cat-nav a { padding:8px 18px; border-radius:20px; font-size:13px; font-weight:500; background:var(--surface2); color:var(--text2); border:1px solid transparent; transition:all 0.15s; }
.cat-nav a:hover, .cat-nav a.active { background:rgba(59,130,246,0.12); color:var(--accent); border-color:rgba(59,130,246,0.3); }

/* Product Grid */
.products-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:20px; }
.product-card { background:var(--surface); border:1px solid var(--border); border-radius:var(--card-radius); overflow:hidden; transition:transform 0.2s, border-color 0.2s, box-shadow 0.2s; }
.product-card:hover { transform:translateY(-4px); border-color:rgba(59,130,246,0.4); box-shadow:0 12px 40px rgba(0,0,0,0.4); }
.product-card .img-wrap { background: var(--surface2); height:220px; display:flex; align-items:center; justify-content:center; padding:16px; }
.product-card img { max-width:100%; max-height:100%; object-fit:contain; }
.product-card .info { padding:16px 18px 18px; }
.product-card .info .title { font-size:13px; font-weight:600; line-height:1.4; height:36px; overflow:hidden; margin-bottom:10px; color:var(--text); }
.product-card .meta { display:flex; justify-content:space-between; align-items:center; }
.product-card .price { font-size:18px; font-weight:700; color:var(--accent); }
.product-card .moq { font-size:11px; color:var(--text3); }
.product-card .cta { display:inline-flex; align-items:center; gap:4px; margin-top:12px; font-size:12px; font-weight:600; color:var(--accent); transition:gap 0.15s; }
.product-card .cta:hover { gap:8px; }

/* Category Section */
.cat-section { margin-bottom:60px; padding-top: 80px; margin-top:-80px; }

/* Footer */
.contact { max-width:var(--max-w); margin:60px auto 0; padding:0 24px; }
.contact-inner { background: var(--surface); border:1px solid var(--border); border-radius:16px; padding:48px; display:grid; grid-template-columns: 1fr 1fr; gap:32px; }
.contact-title { font-size:22px; font-weight:700; margin-bottom:8px; letter-spacing:-0.5px; }
.contact-sub { color:var(--text2); font-size:14px; margin-bottom:32px; }
.contact-card { background: var(--surface2); border-radius:12px; padding:28px; display:flex; align-items:flex-start; gap:18px; border:1px solid var(--border); transition:border-color 0.2s; }
.contact-card:hover { border-color:rgba(59,130,246,0.4); }
.contact-icon { width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; }
.contact-icon.wx { background:rgba(7,193,96,0.15); color:#07c160; }
.contact-icon.wa { background:rgba(37,211,102,0.15); color:#25d366; }
.contact-info h4 { font-size:15px; font-weight:600; margin-bottom:4px; }
.contact-info p { font-size:14px; color:var(--accent); font-weight:600; letter-spacing:0.5px; margin-bottom:4px; }
.contact-info .hint { font-size:12px; color:var(--text3); line-height:1.5; }
.contact-intro { grid-column:1/-1; }
.contact-intro p { color:var(--text2); font-size:14px; line-height:1.7; }
@media (max-width:640px) {
  .contact-inner { grid-template-columns:1fr; padding:28px; }
}
.footer { border-top:1px solid var(--border); margin-top:80px; padding:40px 24px; text-align:center; }
.footer p { color:var(--text3); font-size:13px; }
.footer p + p { margin-top:8px; }

/* Responsive */
@media (max-width:640px) {
  .hero { padding:100px 20px 50px; }
  .hero-stats { gap:20px; }
  .hero-stats .stat .num { font-size:28px; }
  .products-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap:12px; }
  .product-card .img-wrap { height:150px; }
  .topbar-links a { font-size:12px; padding:5px 10px; }
}
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-inner">
    <a href="#" class="logo">Yinxiyangjia <span>Tools</span></a>
    <div class="topbar-links">
      <a href="#products">Products</a>
      <a href="#categories">Categories</a>
      <a href="#contact">Contact</a>
      <a href="https://xj520520.en.alibaba.com" target="_blank" class="btn-store">Visit Store</a>
    </div>
  </div>
</div>

<div class="hero">
  <div class="badge">INDUSTRIAL &amp; DIY POWER TOOLS</div>
  <h1>Professional <span>Power Tools</span> &amp; Hardware Catalog</h1>
  <p>Fuqing Yinxiyangjia Department Store — Factory-direct wholesale supplier of electric drills, angle grinders, saws, garden tools, and hand tools. OEM/ODM supported.</p>
  <div class="hero-stats">
    <div class="stat"><div class="num">''' + str(data['total']) + '''</div><div class="lbl">Products</div></div>
    <div class="stat"><div class="num">''' + str(len(cat_order)) + '''</div><div class="lbl">Categories</div></div>
    <div class="stat"><div class="num">13+</div><div class="lbl">Years Export</div></div>
  </div>
</div>

<div class="section" id="categories">
  <div class="section-title">Browse by Category</div>
  <div class="section-sub">Click a category to jump to its products</div>
  <div class="cat-nav">
''')

for cat in cat_order:
    cnt = len(cats[cat])
    anchor = cat.lower().replace(' ', '-').replace('/', '-').replace('&', '').replace(',', '')
    index.append(f'    <a href="#{anchor}">{cat} <span style="font-size:11px;opacity:0.6">({cnt})</span></a>')

index.append('  </div>')
index.append('</div>')

index.append('<div class="section" id="products">')
index.append('  <div class="section-title">All Products</div>')
index.append('  <div class="section-sub">191 power tools and hardware products, factory-direct prices</div>')

# Product sections
for cat in cat_order:
    items = cats[cat]
    anchor = cat.lower().replace(' ', '-').replace('/', '-').replace('&', '').replace(',', '')
    index.append(f'<div class="cat-section" id="{anchor}">')
    index.append(f'  <div class="section-title" style="font-size:20px;margin-bottom:4px;">{cat}</div>')
    index.append(f'  <div class="section-sub">{len(items)} products</div>')
    index.append('  <div class="products-grid">')

    for p in items:
        title = p.get('title','')
        if len(title) > 65:
            title = title[:62] + '...'
        title = esc(title)
        img = p.get('imgUrl','')
        price = p.get('price','N/A')
        moq = p.get('moq','N/A').replace('\u6700\u4f4e\u8d77\u8ba2\u91cf\uff1a ', '')
        url = p.get('url','#')

        index.append(f'''    <a href="{url}" target="_blank" class="product-card">
      <div class="img-wrap"><img src="{img}" alt="" loading="lazy" onerror="this.parentElement.innerHTML='<div style=color:var(--text3);font-size:13px>Image loading...</div>'"></div>
      <div class="info">
        <div class="title">{title}</div>
        <div class="meta"><span class="price">{price}</span><span class="moq">MOQ: {moq}</span></div>
        <div class="cta">View Details <span>&rarr;</span></div>
      </div>
    </a>''')

    index.append('  </div>')
    index.append('</div>')

index.append('</div>')  # close section

# Contact section
index.append('''
<div class="contact" id="contact">
  <div class="section-title">Contact Us</div>
  <div class="section-sub">Reach out for OEM/ODM inquiries, bulk pricing, and partnership opportunities</div>
  <div class="contact-inner">
    <div class="contact-intro">
      <p>Fuqing Yinxiyangjia Department Store is a factory-direct supplier of industrial and DIY power tools, garden tools, and hardware. With 13+ years of export experience, we serve wholesalers and distributors worldwide. Custom branding, packaging, and specifications are available.</p>
    </div>
    <div class="contact-card">
      <div class="contact-icon wx">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 01.213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 00.167-.054l1.903-1.114a.864.864 0 01.717-.098 10.16 10.16 0 002.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 01-1.162 1.178A1.17 1.17 0 014.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 01-1.162 1.178 1.17 1.17 0 01-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 01.598.082l1.584.926a.272.272 0 00.14.047c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 01-.023-.156.49.49 0 01.201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.952-7.062-6.122zm-2.18 2.769c.535 0 .969.44.969.982a.976.976 0 01-.969.983.976.976 0 01-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 01-.969.983.976.976 0 01-.969-.983c0-.542.434-.982.97-.982z"/></svg>
      </div>
      <div class="contact-info">
        <h4>WeChat</h4>
        <p>Any-9970</p>
        <div class="hint">Scan QR or search ID to connect. Best for product inquiries, custom orders, and real-time communication.</div>
      </div>
    </div>
    <div class="contact-card">
      <div class="contact-icon wa">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
      </div>
      <div class="contact-info">
        <h4>WhatsApp</h4>
        <p>+86 137 8888 9047</p>
        <div class="hint">Available for international buyers. Quick response for pricing, samples, and bulk orders.</div>
      </div>
    </div>
  </div>
</div>
''')

index.append('''
<div class="footer">
  <p style="font-weight:600;color:var(--text2);margin-bottom:8px;">Fuqing Yinxiyangjia Department Store</p>
  <p>Factory-direct Power Tools &amp; Hardware Wholesale | OEM / ODM Supported</p>
  <p><a href="https://xj520520.en.alibaba.com" target="_blank" style="color:var(--accent);">xj520520.en.alibaba.com</a></p>
  <p style="margin-top:16px;">&copy; 2026 Yinxiyangjia Tools. All rights reserved.</p>
  <p style="font-size:11px;color:var(--text3);margin-top:4px;">Auto-sync daily from Alibaba.com store</p>
</div>

</body>
</html>''')

output = '\n'.join(index)
out_path = r'C:\Users\Administrator/AccioWork/2026-07-04-16-44-08/index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(output)

print(f'Site built: {out_path}')
print(f'Products: {data["total"]}')
