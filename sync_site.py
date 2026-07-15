#!/usr/bin/env python3
"""
Auto-sync script: scrape Alibaba.com store, categorize products, rebuild website.
Runs via GitHub Actions or locally.
"""
import json, re, os, sys, time
from datetime import datetime
from playwright.sync_api import sync_playwright

STORE_URL = "https://xj520520.en.alibaba.com/productlist.html"
DATA_FILE = "catalog_data.json"
HTML_FILE = "index.html"
SYNC_LOG = "sync_log.json"

CATEGORY_KEYWORDS = {
    "Angle Grinders / 角磨机": ["angle grinder", "角磨机", "grinder machine"],
    "Electric Hammer Drills / 电锤钻": ["hammer drill", "电锤", "impact drill", "旋转锤", "冲击钻", "rotary hammer", "demolition hammer"],
    "Electric Saws / 电锯": ["saw", "电锯", "chain saw", "circular saw", "圆锯", "切割机", "chainsaw", "jigsaw"],
    "Garden & Outdoor Tools / 园林工具": ["garden", "园林", "prun", "修剪", "lawn mower", "割草", "grass", "hedge", "sprayer"],
    "Socket & Wrench Tools / 套筒扳手": ["socket", "套筒", "wrench", "扳手", "ratchet", "棘轮"],
    "Cordless Drill Sets / 无绳电钻套装": ["cordless drill", "无绳电钻", "drill set", "电钻套装"],
    "Tool Kits & Sets / 工具套装": ["tool set", "工具套装", "tool kit", "工具箱", "combination tool"],
    "Power Tool Accessories / 电动工具配件": ["battery", "电池", "charger", "充电器", "blade", "drill bit", "钻头"],
    "Screwdrivers & Hand Tools / 螺丝刀手工具": ["screwdriver", "螺丝刀", "plier", "hand tool"],
    "Other Power Tools / 其他电动工具": ["polisher", "抛光", "sander", "砂光", "blower", "mixer", "搅拌", "nail", "rivet", "铆钉"],
}

def categorize(title):
    tl = title.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in tl:
                return cat
    return "Other / 其他"

def scrape_store():
    """Scrape all products from the Alibaba.com store using headless browser."""
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page_num = 1
        while True:
            url = f"{STORE_URL}?page={page_num}" if page_num > 1 else STORE_URL
            print(f"  Fetching page {page_num}: {url}")
            try:
                page.goto(url, timeout=30000, wait_until="networkidle")
                page.wait_for_timeout(3000)
                # Extract products via JS
                items = page.evaluate("""() => {
                    const products = [];
                    const links = document.querySelectorAll('a[href*="/product-detail/"]');
                    const seen = new Set();
                    links.forEach(a => {
                        const href = a.href;
                        if (seen.has(href)) return;
                        seen.add(href);
                        const card = a.closest('.product-item, .m-gallery-product-item, [data-role="product-item"]') || a.parentElement;
                        const img = card?.querySelector('img');
                        const titleEl = card?.querySelector('.title, .product-title');
                        const priceEl = card?.querySelector('.price, .product-price');
                        const moqEl = card?.querySelector('.moq, .min-order');
                        if (titleEl || a.innerText) {
                            products.push({
                                title: (titleEl?.innerText || a.innerText || '').trim(),
                                url: href,
                                imgUrl: img?.src || '',
                                price: (priceEl?.innerText || '').trim(),
                                moq: (moqEl?.innerText || '').trim()
                            });
                        }
                    });
                    return products;
                }""")
                if not items:
                    print(f"  No products on page {page_num}, stopping.")
                    break
                products.extend(items)
                print(f"  Found {len(items)} products on page {page_num}")
                page_num += 1
                if page_num > 20:  # safety limit
                    break
            except Exception as e:
                print(f"  Error on page {page_num}: {e}")
                break
        browser.close()
    
    # Deduplicate by URL
    seen = {}
    for p in products:
        url = p.get('url', '')
        if url and url not in seen:
            seen[url] = p
    return list(seen.values())

def merge_products(existing, new_products):
    """Merge new products with existing, preserving translations."""
    existing_map = {}
    for cat, items in existing.get('categories', {}).items():
        for p in items:
            existing_map[p['url']] = (cat, p)
    
    categorized = {}
    for p in new_products:
        cat = categorize(p['title'])
        categorized.setdefault(cat, []).append(p)
    
    # Build final structure
    result = {'total': 0, 'categories': {}}
    for cat in CATEGORY_KEYWORDS.keys():
        items = categorized.get(cat, [])
        for p in items:
            url = p.get('url', '')
            if url in existing_map:
                old = existing_map[url][1]
                for key in ['title_en', 'title_fr', 'title_es']:
                    if key in old:
                        p[key] = old[key]
        result['categories'][cat] = items
        result['total'] += len(items)
    # Add "Other" category
    other_items = categorized.get("Other / 其他", [])
    if other_items:
        result['categories']["Other / 其他"] = other_items
        result['total'] += len(other_items)
    
    return result

def main():
    print("=== Auto Sync: Yinxiyangjia Tools ===")
    print(f"Start: {datetime.now().isoformat()}")
    
    # 1. Scrape store
    print("\n[1/4] Scraping store products...")
    new_products = scrape_store()
    print(f"  Total scraped: {len(new_products)} products")
    
    # 2. Load existing data
    print("\n[2/4] Loading existing catalog...")
    existing = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        print(f"  Existing: {existing.get('total', 0)} products")
    else:
        print("  No existing data, starting fresh")
    
    # 3. Merge
    print("\n[3/4] Merging and categorizing...")
    merged = merge_products(existing, new_products)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"  Merged total: {merged['total']} products")
    
    # 4. Log
    log = {
        'last_sync': datetime.now().isoformat(),
        'total_products': merged['total'],
        'new_products': max(0, len(new_products) - existing.get('total', 0))
    }
    with open(SYNC_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2)
    print(f"\n=== Sync complete: {log['total_products']} products ===")
    return log

if __name__ == '__main__':
    main()
