"""
跨境运营数据追踪系统 - 数据生成器

生成空气能热泵跨境销售场景的示例数据
"""

import random
from datetime import datetime, timedelta
from config import CURRENCIES, PLATFORMS, COUNTRIES


def generate_sku_master():
    """
    生成 SKU 主档数据
    
    Returns:
        SKU 列表
    """
    skus = [
        {
            "sku_id": "SKU-HP-005",
            "product_name": "空气能热泵 5HP",
            "product_name_en": "Air Source Heat Pump 5HP",
            "category": "热泵设备",
            "category_en": "Heat Pump Equipment",
            "spec": "5HP/380V/三相电",
            "spec_en": "5HP/380V/3-Phase",
            "supplier": "广东某某电器",
            "supplier_en": "Guangdong XX Electric",
            "cost_price": 12500.00,
            "retail_price": 18800.00,
            "status": "在售",
            "status_en": "Active",
            "created_at": "2026-07-01",
            "updated_at": "2026-07-22"
        },
        {
            "sku_id": "SKU-HP-010",
            "product_name": "空气能热泵 10HP",
            "product_name_en": "Air Source Heat Pump 10HP",
            "category": "热泵设备",
            "category_en": "Heat Pump Equipment",
            "spec": "10HP/380V/三相电",
            "spec_en": "10HP/380V/3-Phase",
            "supplier": "广东某某电器",
            "supplier_en": "Guangdong XX Electric",
            "cost_price": 22000.00,
            "retail_price": 33000.00,
            "status": "在售",
            "status_en": "Active",
            "created_at": "2026-07-01",
            "updated_at": "2026-07-22"
        },
        {
            "sku_id": "SKU-HP-015",
            "product_name": "空气能热泵 15HP",
            "product_name_en": "Air Source Heat Pump 15HP",
            "category": "热泵设备",
            "category_en": "Heat Pump Equipment",
            "spec": "15HP/380V/三相电",
            "spec_en": "15HP/380V/3-Phase",
            "supplier": "广东某某电器",
            "supplier_en": "Guangdong XX Electric",
            "cost_price": 31000.00,
            "retail_price": 46500.00,
            "status": "在售",
            "status_en": "Active",
            "created_at": "2026-07-01",
            "updated_at": "2026-07-22"
        },
        {
            "sku_id": "SKU-AC-012",
            "product_name": "中央空调 12HP",
            "product_name_en": "Central AC 12HP",
            "category": "空调设备",
            "category_en": "AC Equipment",
            "spec": "12HP/380V/三相电",
            "spec_en": "12HP/380V/3-Phase",
            "supplier": "佛山某某制冷",
            "supplier_en": "Foshan XX Refrigeration",
            "cost_price": 18500.00,
            "retail_price": 27800.00,
            "status": "在售",
            "status_en": "Active",
            "created_at": "2026-07-05",
            "updated_at": "2026-07-22"
        },
        {
            "sku_id": "SKU-WS-050",
            "product_name": "空气能热水器 50L",
            "product_name_en": "Air Source Water Heater 50L",
            "category": "热水器",
            "category_en": "Water Heater",
            "spec": "50L/220V/单相电",
            "spec_en": "50L/220V/Single-Phase",
            "supplier": "中山某某卫浴",
            "supplier_en": "Zhongshan XX Sanitary",
            "cost_price": 2800.00,
            "retail_price": 4200.00,
            "status": "清仓",
            "status_en": "Clearance",
            "created_at": "2026-06-15",
            "updated_at": "2026-07-20"
        }
    ]
    return skus


def generate_platform_listings(skus):
    """
    生成平台 Listing 数据
    
    Args:
        skus: SKU 列表
    
    Returns:
        Listing 列表
    """
    listings = []
    
    # 为每个 SKU 生成多个平台的 Listing
    for sku in skus:
        # Amazon US
        listings.append({
            "sku_id": sku["sku_id"],
            "platform": "Amazon US",
            "listing_id": f"B0{''.join(random.choices('0123456789ABCDEF', k=8))}",
            "listed_date": "2026-07-01",
            "status": "Active",
            "price": round(sku["retail_price"] / CURRENCIES["USD"]["rate"] * 1.1, 2),
            "currency": "USD",
            "stock": random.randint(20, 100),
            "last_updated": "2026-07-22"
        })
        
        # Amazon DE (仅热泵设备)
        if "热泵" in sku["category"]:
            listings.append({
                "sku_id": sku["sku_id"],
                "platform": "Amazon DE",
                "listing_id": f"B0{''.join(random.choices('0123456789ABCDEF', k=8))}",
                "listed_date": "2026-07-05",
                "status": "Active",
                "price": round(sku["retail_price"] / CURRENCIES["EUR"]["rate"] * 1.05, 2),
                "currency": "EUR",
                "stock": random.randint(15, 60),
                "last_updated": "2026-07-22"
            })
        
        # eBay (所有产品)
        listings.append({
            "sku_id": sku["sku_id"],
            "platform": "eBay",
            "listing_id": f"EBAY-{sku['sku_id'][-3:]}",
            "listed_date": "2026-07-10",
            "status": "Active" if sku["status"] == "在售" else "Inactive",
            "price": round(sku["retail_price"] / CURRENCIES["USD"]["rate"] * 1.0, 2),
            "currency": "USD",
            "stock": random.randint(10, 50),
            "last_updated": "2026-07-21"
        })
    
    return listings


def generate_daily_sales(skus, days=22):
    """
    生成销售日表数据
    
    Args:
        skus: SKU 列表
        days: 生成天数
    
    Returns:
        销售记录列表
    """
    sales = []
    start_date = datetime(2026, 7, 1)
    
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # 每天生成 3-8 单
        daily_orders = random.randint(3, 8)
        
        for _ in range(daily_orders):
            # 随机选择 SKU
            sku = random.choice(skus)
            
            # 随机选择平台和国家
            platform = random.choice(PLATFORMS)
            country = random.choice(COUNTRIES)
            
            # 根据平台确定币种
            if "US" in platform:
                currency = "USD"
            elif "DE" in platform:
                currency = "EUR"
            elif "UK" in platform:
                currency = "GBP"
            else:
                currency = random.choice(["USD", "EUR", "GBP"])
            
            # 计算价格（在零售价基础上浮动）
            base_price_usd = sku["retail_price"] / CURRENCIES["USD"]["rate"]
            price_multiplier = random.uniform(0.85, 1.15)
            price = round(base_price_usd * price_multiplier, 2)
            
            # 数量
            quantity = random.randint(1, 3)
            
            # 金额
            amount = round(price * quantity, 2)
            
            # 汇率和人民币金额
            exchange_rate = CURRENCIES[currency]["rate"]
            amount_cny = round(amount * exchange_rate, 2)
            
            # 买家
            buyer_names = [
                "John Smith", "Michael Brown", "David Wilson", "James Taylor",
                "Hans Mueller", "Thomas Schmidt", "Peter Fischer",
                "James Johnson", "Robert Williams", "William Brown"
            ]
            buyer = random.choice(buyer_names)
            
            sales.append({
                "date": date_str,
                "sku_id": sku["sku_id"],
                "platform": platform,
                "order_id": f"ORD-{date_str.replace('-', '')}-{random.randint(1000, 9999)}",
                "quantity": quantity,
                "amount": amount,
                "currency": currency,
                "buyer": buyer,
                "country": country["code"],
                "exchange_rate": exchange_rate,
                "amount_cny": amount_cny
            })
    
    return sales


def generate_inventory_data(skus):
    """
    生成库存追踪数据
    
    Args:
        skus: SKU 列表
    
    Returns:
        库存记录列表
    """
    inventory = []
    start_date = datetime(2026, 7, 1)
    
    # 初始库存
    stock_balance = {}
    for sku in skus:
        stock_balance[sku["sku_id"]] = random.randint(50, 200)
    
    # 生成 22 天的库存变动
    for day in range(22):
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        
        for sku in skus:
            sku_id = sku["sku_id"]
            
            # 入库（不定期）
            inbound = 0
            if random.random() < 0.3:  # 30% 概率入库
                inbound = random.randint(10, 50)
                stock_balance[sku_id] += inbound
            
            # 出库（根据销售）
            outbound = random.randint(0, 10)
            if outbound > stock_balance[sku_id]:
                outbound = stock_balance[sku_id]
            stock_balance[sku_id] -= outbound
            
            # 记录
            inventory.append({
                "sku_id": sku_id,
                "date": date_str,
                "inbound": inbound,
                "outbound": outbound,
                "balance": stock_balance[sku_id],
                "warehouse": "深圳主仓" if random.random() < 0.7 else "香港中转仓",
                "remarks": "正常出库" if outbound > 0 else ("入库补货" if inbound > 0 else "")
            })
    
    return inventory


def generate_inquiry_data(skus):
    """
    生成询盘记录数据
    
    Args:
        skus: SKU 列表
    
    Returns:
        询盘记录列表
    """
    inquiries = []
    start_date = datetime(2026, 7, 1)
    
    # 询盘来源
    sources = ["阿里国际站", "环球资源", "展会", "独立站", "LinkedIn", "Google"]
    sources_en = ["Alibaba", "Global Sources", "Exhibition", "Website", "LinkedIn", "Google"]
    
    # 客户名称
    customers = [
        {"name": "ABC Heating Co.", "country": "US"},
        {"name": "German HVAC GmbH", "country": "DE"},
        {"name": "UK Boiler Ltd.", "country": "UK"},
        {"name": "Aussie Solar Pty", "country": "AU"},
        {"name": "Maple Energy Inc.", "country": "CA"},
    ]
    
    # 状态流转
    statuses = ["新询盘", "已报价", "谈判中", "已成交", "已流失"]
    
    # 生成 15-25 条询盘
    inquiry_count = random.randint(15, 25)
    
    for i in range(inquiry_count):
        # 随机日期
        random_day = random.randint(0, 21)
        inquiry_date = start_date + timedelta(days=random_day)
        
        # 随机客户
        customer = random.choice(customers)
        
        # 随机产品
        sku = random.choice(skus)
        
        # 随机来源
        source_idx = random.randint(0, len(sources) - 1)
        
        # 状态（根据日期推断）
        if random_day < 7:
            status = random.choice(["新询盘", "已报价"])
        elif random_day < 14:
            status = random.choice(["已报价", "谈判中"])
        else:
            status = random.choice(["谈判中", "已成交", "已流失"])
        
        # 跟进记录
        follow_ups = [
            "已发送产品目录和报价单",
            "客户要求提供 CE 认证文件",
            "确认交期为 30 天",
            "客户正在比较其他供应商",
            "已安排样品寄送",
            "价格谈判中，客户要求降价 10%",
            "已成交，等待客户付款",
            "客户暂时搁置采购计划",
        ]
        
        # 预计成交日期
        if status in ["已成交", "已流失"]:
            expected_close = ""
        else:
            close_date = inquiry_date + timedelta(days=random.randint(7, 30))
            expected_close = close_date.strftime("%Y-%m-%d")
        
        inquiries.append({
            "date": inquiry_date.strftime("%Y-%m-%d"),
            "customer": customer["name"],
            "product": sku["product_name"],
            "product_en": sku["product_name_en"],
            "source": sources[source_idx],
            "source_en": sources_en[source_idx],
            "status": status,
            "follow_up": random.choice(follow_ups),
            "expected_close": expected_close,
            "country": customer["country"]
        })
    
    return inquiries


def generate_weekly_review(sales):
    """
    生成每周复盘数据
    
    Args:
        sales: 销售记录列表
    
    Returns:
        每周复盘列表
    """
    weekly_data = []
    
    # 按周分组
    weeks = {}
    for sale in sales:
        date = datetime.strptime(sale["date"], "%Y-%m-%d")
        week_num = date.isocalendar()[1]
        
        if week_num not in weeks:
            weeks[week_num] = {
                "start_date": date,
                "end_date": date,
                "sales": []
            }
        
        weeks[week_num]["end_date"] = date
        weeks[week_num]["sales"].append(sale)
    
    # 生成每周复盘
    for week_num, week_data in sorted(weeks.items()):
        week_sales = week_data["sales"]
        
        # 计算指标
        total_revenue = sum(s["amount_cny"] for s in week_sales)
        total_orders = len(week_sales)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # 转化率（模拟）
        conversion_rate = round(random.uniform(0.02, 0.08), 4)
        
        # 库存周转率（模拟）
        inventory_turnover = round(random.uniform(1.5, 4.0), 2)
        
        weekly_data.append({
            "week": f"W{week_num}",
            "date_range": f"{week_data['start_date'].strftime('%m/%d')}-{week_data['end_date'].strftime('%m/%d')}",
            "revenue": round(total_revenue, 2),
            "orders": total_orders,
            "aov": round(avg_order_value, 2),
            "conversion_rate": conversion_rate,
            "inventory_turnover": inventory_turnover,
            "remarks": ""
        })
    
    return weekly_data


def generate_all_data():
    """
    生成所有示例数据
    
    Returns:
        所有数据的字典
    """
    # 设置随机种子以保证可重复性
    random.seed(42)
    
    skus = generate_sku_master()
    listings = generate_platform_listings(skus)
    sales = generate_daily_sales(skus)
    inventory = generate_inventory_data(skus)
    inquiries = generate_inquiry_data(skus)
    weekly_review = generate_weekly_review(sales)
    
    return {
        "skus": skus,
        "listings": listings,
        "sales": sales,
        "inventory": inventory,
        "inquiries": inquiries,
        "weekly_review": weekly_review
    }


if __name__ == "__main__":
    # 测试数据生成
    data = generate_all_data()
    
    print("=== 数据生成完成 ===")
    print(f"SKU 数量: {len(data['skus'])}")
    print(f"Listing 数量: {len(data['listings'])}")
    print(f"销售记录: {len(data['sales'])}")
    print(f"库存记录: {len(data['inventory'])}")
    print(f"询盘记录: {len(data['inquiries'])}")
    print(f"周复盘: {len(data['weekly_review'])}")
