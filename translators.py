"""
跨境运营数据追踪系统 - 双语翻译器

提供中英文双语支持，实现一键切换
"""


class Translator:
    """双语翻译器"""
    
    def __init__(self, language="zh"):
        """
        初始化翻译器
        
        Args:
            language: 初始语言，"zh" 或 "en"
        """
        self.language = language
        self.translations = self._load_translations()
    
    def _load_translations(self):
        """加载翻译表"""
        return {
            # 工作表名称
            "sheet_names": {
                "sku_master": {"zh": "SKU 主档", "en": "SKU Master"},
                "platform_listing": {"zh": "平台 Listing 状态", "en": "Platform Listing"},
                "inventory": {"zh": "库存追踪", "en": "Inventory Tracking"},
                "daily_sales": {"zh": "销售日表", "en": "Daily Sales"},
                "inquiry": {"zh": "询盘记录", "en": "Inquiry Records"},
                "weekly_review": {"zh": "每周复盘", "en": "Weekly Review"},
            },
            
            # SKU 主档表头
            "sku_master_headers": {
                "zh": ["SKU 编码", "产品名称", "品类", "规格", "供应商", "成本价", "建议零售价", "状态", "创建日期", "更新日期"],
                "en": ["SKU ID", "Product Name", "Category", "Spec", "Supplier", "Cost Price", "Retail Price", "Status", "Created At", "Updated At"]
            },
            
            # 平台 Listing 表头
            "platform_listing_headers": {
                "zh": ["SKU 编码", "平台", "Listing ID", "上架日期", "状态", "价格", "币种", "库存", "最后更新"],
                "en": ["SKU ID", "Platform", "Listing ID", "Listed Date", "Status", "Price", "Currency", "Stock", "Last Updated"]
            },
            
            # 库存追踪表头
            "inventory_headers": {
                "zh": ["SKU 编码", "日期", "入库数量", "出库数量", "库存余额", "仓库", "备注"],
                "en": ["SKU ID", "Date", "Inbound", "Outbound", "Balance", "Warehouse", "Remarks"]
            },
            
            # 销售日表表头
            "daily_sales_headers": {
                "zh": ["日期", "SKU 编码", "平台", "订单号", "数量", "金额", "币种", "买家", "国家", "汇率", "人民币金额"],
                "en": ["Date", "SKU ID", "Platform", "Order ID", "Qty", "Amount", "Currency", "Buyer", "Country", "Rate", "Amount (CNY)"]
            },
            
            # 询盘记录表头
            "inquiry_headers": {
                "zh": ["日期", "客户", "产品", "询盘来源", "状态", "跟进记录", "预计成交日期"],
                "en": ["Date", "Customer", "Product", "Source", "Status", "Follow-up", "Expected Close"]
            },
            
            # 每周复盘表头
            "weekly_review_headers": {
                "zh": ["周次", "日期范围", "销售额", "订单数", "客单价", "转化率", "库存周转率", "备注"],
                "en": ["Week", "Date Range", "Revenue", "Orders", "AOV", "Conversion", "Inventory Turnover", "Remarks"]
            },
            
            # 通用标签
            "labels": {
                "report_title": {"zh": "跨境运营数据追踪台账", "en": "Cross-border Ops Dashboard"},
                "generated_at": {"zh": "报告生成时间", "en": "Report Generated At"},
                "language_switch": {"zh": "语言切换", "en": "Language"},
                "total": {"zh": "合计", "en": "Total"},
                "average": {"zh": "平均", "en": "Average"},
                "summary": {"zh": "汇总", "en": "Summary"},
                "details": {"zh": "明细", "en": "Details"},
            },
            
            # 状态标签
            "status": {
                "active": {"zh": "在售", "en": "Active"},
                "inactive": {"zh": "停售", "en": "Inactive"},
                "clearance": {"zh": "清仓", "en": "Clearance"},
                "new_inquiry": {"zh": "新询盘", "en": "New"},
                "quoted": {"zh": "已报价", "en": "Quoted"},
                "negotiating": {"zh": "谈判中", "en": "Negotiating"},
                "closed_won": {"zh": "已成交", "en": "Closed Won"},
                "closed_lost": {"zh": "已流失", "en": "Closed Lost"},
            },
        }
    
    def get(self, key, subkey=None):
        """
        获取翻译文本
        
        Args:
            key: 一级键
            subkey: 二级键（可选）
        
        Returns:
            翻译后的文本
        """
        if subkey:
            return self.translations.get(key, {}).get(subkey, {}).get(self.language, key)
        return self.translations.get(key, {}).get(self.language, key)
    
    def get_headers(self, sheet_type):
        """
        获取工作表表头
        
        Args:
            sheet_type: 工作表类型
        
        Returns:
            表头列表
        """
        return self.get(f"{sheet_type}_headers")
    
    def get_sheet_name(self, sheet_type):
        """
        获取工作表名称
        
        Args:
            sheet_type: 工作表类型
        
        Returns:
            工作表名称
        """
        return self.get("sheet_names", sheet_type)
    
    def switch_language(self):
        """切换语言"""
        self.language = "en" if self.language == "zh" else "zh"
        return self.language
    
    def set_language(self, language):
        """
        设置语言
        
        Args:
            language: "zh" 或 "en"
        """
        if language in ["zh", "en"]:
            self.language = language
