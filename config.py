"""
跨境运营数据追踪系统 - 配置文件

定义币种、平台、国家等基础配置
"""

# 币种配置
CURRENCIES = {
    "USD": {"symbol": "$", "rate": 7.25, "name": "美元"},
    "EUR": {"symbol": "€", "rate": 7.80, "name": "欧元"},
    "GBP": {"symbol": "£", "rate": 9.10, "name": "英镑"},
    "AUD": {"symbol": "A$", "rate": 4.85, "name": "澳元"},
    "CAD": {"symbol": "C$", "rate": 5.35, "name": "加元"},
    "CNY": {"symbol": "¥", "rate": 1.00, "name": "人民币"},
}

# 平台配置
PLATFORMS = [
    "Amazon US",
    "Amazon DE", 
    "Amazon UK",
    "eBay",
    "独立站"
]

# 国家配置
COUNTRIES = [
    {"code": "US", "name": "美国", "name_en": "United States"},
    {"code": "DE", "name": "德国", "name_en": "Germany"},
    {"code": "UK", "name": "英国", "name_en": "United Kingdom"},
    {"code": "AU", "name": "澳大利亚", "name_en": "Australia"},
    {"code": "CA", "name": "加拿大", "name_en": "Canada"},
]

# SKU 状态
SKU_STATUSES = ["在售", "停售", "清仓"]
SKU_STATUSES_EN = ["Active", "Inactive", "Clearance"]

# 询盘状态
INQUIRY_STATUSES = ["新询盘", "已报价", "谈判中", "已成交", "已流失"]
INQUIRY_STATUSES_EN = ["New", "Quoted", "Negotiating", "Closed Won", "Closed Lost"]

# 库存预警阈值
INVENTORY_WARNING_THRESHOLD = 10  # 低于此数量预警

# 汇率更新日期（示例）
EXCHANGE_RATE_DATE = "2026-07-22"
