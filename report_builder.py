"""
跨境运营数据追踪系统 - 报告生成器

生成多 Sheet Excel 报告，支持双语切换
"""

import xlsxwriter
import datetime
from config import CURRENCIES, INVENTORY_WARNING_THRESHOLD
from translators import Translator


class ReportBuilder:
    """报告生成器"""
    
    def __init__(self, language="zh"):
        """
        初始化报告生成器
        
        Args:
            language: 语言，"zh" 或 "en"
        """
        self.translator = Translator(language)
        self.formats = {}
    
    def _init_formats(self, workbook):
        """初始化格式定义"""
        # 标题格式
        self.formats["title"] = workbook.add_format({
            "bold": True, "font_size": 16, "font_color": "#1a1a2e",
            "bottom": 2, "bottom_color": "#1a1a2e", "align": "left",
        })
        
        # 表头格式（中文）
        self.formats["header_zh"] = workbook.add_format({
            "bold": True, "bg_color": "#1a1a2e", "font_color": "#ffffff",
            "border": 1, "text_wrap": True, "align": "center", "valign": "vcenter",
            "font_size": 11,
        })
        
        # 表头格式（英文）
        self.formats["header_en"] = workbook.add_format({
            "bold": True, "bg_color": "#0f3460", "font_color": "#ffffff",
            "border": 1, "text_wrap": True, "align": "center", "valign": "vcenter",
            "font_size": 11,
        })
        
        # 金额格式
        self.formats["money"] = workbook.add_format({
            "num_format": "¥#,##0.00", "border": 1, "align": "center",
        })
        
        # 外币金额格式
        self.formats["money_usd"] = workbook.add_format({
            "num_format": "$#,##0.00", "border": 1, "align": "center",
        })
        
        self.formats["money_eur"] = workbook.add_format({
            "num_format": "€#,##0.00", "border": 1, "align": "center",
        })
        
        self.formats["money_gbp"] = workbook.add_format({
            "num_format": "£#,##0.00", "border": 1, "align": "center",
        })
        
        # 数字格式
        self.formats["number"] = workbook.add_format({
            "num_format": "#,##0", "border": 1, "align": "center",
        })
        
        # 百分比格式
        self.formats["percent"] = workbook.add_format({
            "num_format": "0.00%", "border": 1, "align": "center",
        })
        
        # 文本格式
        self.formats["text"] = workbook.add_format({
            "border": 1, "align": "center", "valign": "vcenter",
        })
        
        # 偶数行格式
        self.formats["even"] = workbook.add_format({
            "border": 1, "align": "center", "bg_color": "#f5f5f5",
        })
        
        # 金额偶数行格式
        self.formats["money_even"] = workbook.add_format({
            "num_format": "¥#,##0.00", "border": 1, "align": "center",
            "bg_color": "#f5f5f5",
        })
        
        # 大额订单格式（红色高亮）
        self.formats["high_amount"] = workbook.add_format({
            "num_format": "¥#,##0.00", "border": 1, "align": "center",
            "bg_color": "#ffcccc", "font_color": "#cc0000",
        })
        
        # 库存预警格式（橙色高亮）
        self.formats["stock_warning"] = workbook.add_format({
            "num_format": "#,##0", "border": 1, "align": "center",
            "bg_color": "#ffcccc", "font_color": "#cc0000",
        })
        
        # 合计行格式
        self.formats["total"] = workbook.add_format({
            "bold": True, "bg_color": "#1a1a2e", "font_color": "#ffffff",
            "border": 1, "num_format": "¥#,##0.00",
        })
        
        self.formats["total_num"] = workbook.add_format({
            "bold": True, "bg_color": "#1a1a2e", "font_color": "#ffffff",
            "border": 1, "num_format": "#,##0",
        })
        
        # 副标题格式
        self.formats["subtitle"] = workbook.add_format({
            "bold": True, "font_size": 12, "font_color": "#333333",
            "bottom": 1, "bottom_color": "#cccccc",
        })
        
        # 日期格式
        self.formats["date"] = workbook.add_format({
            "num_format": "yyyy-mm-dd", "border": 1, "align": "center",
        })
        
        # 语言控制格式
        self.formats["control"] = workbook.add_format({
            "bold": True, "bg_color": "#e94560", "font_color": "#ffffff",
            "border": 1, "align": "center",
        })
        
        # 标签格式
        self.formats["label"] = workbook.add_format({
            "bold": True, "font_size": 10, "font_color": "#666666",
        })
    
    def _get_money_format(self, currency):
        """根据币种获取金额格式"""
        format_map = {
            "USD": self.formats["money_usd"],
            "EUR": self.formats["money_eur"],
            "GBP": self.formats["money_gbp"],
            "CNY": self.formats["money"],
        }
        return format_map.get(currency, self.formats["money"])
    
    def _write_sheet_with_language(self, ws, sheet_type, headers, data, row_start=0):
        """
        写入带双语支持的工作表
        
        Args:
            ws: 工作表对象
            sheet_type: 工作表类型
            headers: 表头数据
            data: 数据列表
            row_start: 起始行
        """
        # 写入中文表头
        for col, h in enumerate(headers["zh"]):
            ws.write(row_start, col, h, self.formats["header_zh"])
        
        # 写入英文表头（下一行）
        for col, h in enumerate(headers["en"]):
            ws.write(row_start + 1, col, h, self.formats["header_en"])
        
        # 写入数据
        for row_idx, record in enumerate(data):
            row = row_start + 2 + row_idx
            is_even = row_idx % 2 == 1
            
            for col_idx, key in enumerate(headers["zh_keys"]):
                value = record.get(key, "")
                
                # 根据列类型选择格式
                if "金额" in headers["zh"][col_idx] or "价格" in headers["zh"][col_idx]:
                    fmt = self.formats["money_even"] if is_even else self.formats["money"]
                elif "数量" in headers["zh"][col_idx] or "库存" in headers["zh"][col_idx]:
                    fmt = self.formats["number"]
                elif "日期" in headers["zh"][col_idx]:
                    fmt = self.formats["date"]
                else:
                    fmt = self.formats["even"] if is_even else self.formats["text"]
                
                ws.write(row, col_idx, value, fmt)
        
        return row_start + 2 + len(data)
    
    def build_sku_master_sheet(self, wb, skus):
        """
        构建 SKU 主档工作表
        
        Args:
            wb: 工作簿对象
            skus: SKU 数据列表
        """
        sheet_name = self.translator.get_sheet_name("sku_master")
        ws = wb.add_worksheet(sheet_name)
        ws.set_tab_color("#1a1a2e")
        ws.hide_gridlines(2)
        
        # 设置列宽
        col_widths = [15, 20, 12, 20, 18, 14, 16, 10, 14, 14]
        for i, w in enumerate(col_widths):
            ws.set_column(i, i, w)
        
        # 写入标题
        ws.merge_range("A1:J1", f"📊 {self.translator.get('labels', 'report_title')}", self.formats["title"])
        ws.write(2, 0, f"{self.translator.get('labels', 'generated_at')}：{datetime.date.today()}", 
                self.formats["label"])
        
        # 准备表头
        headers = {
            "zh": self.translator.get_headers("sku_master"),
            "en": self.translator.get_headers("sku_master"),
            "zh_keys": ["sku_id", "product_name", "category", "spec", "supplier", 
                       "cost_price", "retail_price", "status", "created_at", "updated_at"]
        }
        
        # 写入表头和数据
        data_row = self._write_sheet_with_language(ws, "sku_master", headers, skus, row_start=4)
        
        # 添加自动筛选
        ws.autofilter(4, 0, data_row - 1, len(headers["zh"]) - 1)
        
        return ws
    
    def build_platform_listing_sheet(self, wb, listings):
        """
        构建平台 Listing 状态工作表
        
        Args:
            wb: 工作簿对象
            listings: Listing 数据列表
        """
        sheet_name = self.translator.get_sheet_name("platform_listing")
        ws = wb.add_worksheet(sheet_name)
        ws.set_tab_color("#e94560")
        ws.hide_gridlines(2)
        
        # 设置列宽
        col_widths = [15, 15, 20, 14, 12, 12, 10, 10, 14]
        for i, w in enumerate(col_widths):
            ws.set_column(i, i, w)
        
        # 写入标题
        ws.merge_range("A1:I1", f"📊 {self.translator.get('labels', 'report_title')}", self.formats["title"])
        ws.write(2, 0, f"{self.translator.get('labels', 'generated_at')}：{datetime.date.today()}", 
                self.formats["label"])
        
        # 准备表头
        headers = {
            "zh": self.translator.get_headers("platform_listing"),
            "en": self.translator.get_headers("platform_listing"),
            "zh_keys": ["sku_id", "platform", "listing_id", "listed_date", "status",
                       "price", "currency", "stock", "last_updated"]
        }
        
        # 写入表头和数据
        data_row = self._write_sheet_with_language(ws, "platform_listing", headers, listings, row_start=4)
        
        # 添加自动筛选
        ws.autofilter(4, 0, data_row - 1, len(headers["zh"]) - 1)
        
        return ws
    
    def build_inventory_sheet(self, wb, inventory):
        """
        构建库存追踪工作表
        
        Args:
            wb: 工作簿对象
            inventory: 库存数据列表
        """
        sheet_name = self.translator.get_sheet_name("inventory")
        ws = wb.add_worksheet(sheet_name)
        ws.set_tab_color("#0f3460")
        ws.hide_gridlines(2)
        
        # 设置列宽
        col_widths = [15, 14, 12, 12, 12, 14, 14]
        for i, w in enumerate(col_widths):
            ws.set_column(i, i, w)
        
        # 写入标题
        ws.merge_range("A1:G1", f"📊 {self.translator.get('labels', 'report_title')}", self.formats["title"])
        ws.write(2, 0, f"{self.translator.get('labels', 'generated_at')}：{datetime.date.today()}", 
                self.formats["label"])
        
        # 准备表头
        headers = {
            "zh": self.translator.get_headers("inventory"),
            "en": self.translator.get_headers("inventory"),
            "zh_keys": ["sku_id", "date", "inbound", "outbound", "balance", "warehouse", "remarks"]
        }
        
        # 写入表头和数据
        data_row = self._write_sheet_with_language(ws, "inventory", headers, inventory, row_start=4)
        
        # 添加库存预警格式
        # 注意：这里需要根据实际数据添加条件格式
        
        # 添加自动筛选
        ws.autofilter(4, 0, data_row - 1, len(headers["zh"]) - 1)
        
        return ws
    
    def build_daily_sales_sheet(self, wb, sales):
        """
        构建销售日表工作表
        
        Args:
            wb: 工作簿对象
            sales: 销售数据列表
        """
        sheet_name = self.translator.get_sheet_name("daily_sales")
        ws = wb.add_worksheet(sheet_name)
        ws.set_tab_color("#533483")
        ws.hide_gridlines(2)
        
        # 设置列宽
        col_widths = [14, 15, 15, 22, 8, 12, 10, 15, 8, 10, 14]
        for i, w in enumerate(col_widths):
            ws.set_column(i, i, w)
        
        # 写入标题
        ws.merge_range("A1:K1", f"📊 {self.translator.get('labels', 'report_title')}", self.formats["title"])
        ws.write(2, 0, f"{self.translator.get('labels', 'generated_at')}：{datetime.date.today()}", 
                self.formats["label"])
        
        # 准备表头
        headers = {
            "zh": self.translator.get_headers("daily_sales"),
            "en": self.translator.get_headers("daily_sales"),
            "zh_keys": ["date", "sku_id", "platform", "order_id", "quantity",
                       "amount", "currency", "buyer", "country", "exchange_rate", "amount_cny"]
        }
        
        # 写入表头和数据
        data_row = self._write_sheet_with_language(ws, "daily_sales", headers, sales, row_start=4)
        
        # 添加汇总行
        total_amount = sum(s["amount_cny"] for s in sales)
        total_orders = len(sales)
        
        ws.write(data_row, 0, self.translator.get("labels", "total"), self.formats["total"])
        ws.write(data_row, 4, total_orders, self.formats["total_num"])
        ws.write(data_row, 5, "", self.formats["total"])
        ws.write(data_row, 10, round(total_amount, 2), self.formats["total"])
        
        # 添加自动筛选
        ws.autofilter(4, 0, data_row - 1, len(headers["zh"]) - 1)
        
        return ws
    
    def build_inquiry_sheet(self, wb, inquiries):
        """
        构建询盘记录工作表
        
        Args:
            wb: 工作簿对象
            inquiries: 询盘数据列表
        """
        sheet_name = self.translator.get_sheet_name("inquiry")
        ws = wb.add_worksheet(sheet_name)
        ws.set_tab_color("#16213e")
        ws.hide_gridlines(2)
        
        # 设置列宽
        col_widths = [14, 18, 20, 14, 12, 30, 14]
        for i, w in enumerate(col_widths):
            ws.set_column(i, i, w)
        
        # 写入标题
        ws.merge_range("A1:G1", f"📊 {self.translator.get('labels', 'report_title')}", self.formats["title"])
        ws.write(2, 0, f"{self.translator.get('labels', 'generated_at')}：{datetime.date.today()}", 
                self.formats["label"])
        
        # 准备表头
        headers = {
            "zh": self.translator.get_headers("inquiry"),
            "en": self.translator.get_headers("inquiry"),
            "zh_keys": ["date", "customer", "product", "source", "status", "follow_up", "expected_close"]
        }
        
        # 写入表头和数据
        data_row = self._write_sheet_with_language(ws, "inquiry", headers, inquiries, row_start=4)
        
        # 添加自动筛选
        ws.autofilter(4, 0, data_row - 1, len(headers["zh"]) - 1)
        
        return ws
    
    def build_weekly_review_sheet(self, wb, weekly_review):
        """
        构建每周复盘工作表
        
        Args:
            wb: 工作簿对象
            weekly_review: 每周复盘数据列表
        """
        sheet_name = self.translator.get_sheet_name("weekly_review")
        ws = wb.add_worksheet(sheet_name)
        ws.set_tab_color("#e94560")
        ws.hide_gridlines(2)
        
        # 设置列宽
        col_widths = [8, 14, 14, 10, 14, 12, 14, 20]
        for i, w in enumerate(col_widths):
            ws.set_column(i, i, w)
        
        # 写入标题
        ws.merge_range("A1:H1", f"📊 {self.translator.get('labels', 'report_title')}", self.formats["title"])
        ws.write(2, 0, f"{self.translator.get('labels', 'generated_at')}：{datetime.date.today()}", 
                self.formats["label"])
        
        # 准备表头
        headers = {
            "zh": self.translator.get_headers("weekly_review"),
            "en": self.translator.get_headers("weekly_review"),
            "zh_keys": ["week", "date_range", "revenue", "orders", "aov", 
                       "conversion_rate", "inventory_turnover", "remarks"]
        }
        
        # 写入表头和数据
        data_row = self._write_sheet_with_language(ws, "weekly_review", headers, weekly_review, row_start=4)
        
        # 添加汇总行
        total_revenue = sum(w["revenue"] for w in weekly_review)
        total_orders = sum(w["orders"] for w in weekly_review)
        avg_aov = total_revenue / total_orders if total_orders > 0 else 0
        avg_conversion = sum(w["conversion_rate"] for w in weekly_review) / len(weekly_review)
        
        ws.write(data_row, 0, self.translator.get("labels", "total"), self.formats["total"])
        ws.write(data_row, 2, round(total_revenue, 2), self.formats["total"])
        ws.write(data_row, 3, total_orders, self.formats["total_num"])
        ws.write(data_row, 4, round(avg_aov, 2), self.formats["total"])
        ws.write(data_row, 5, round(avg_conversion, 4), self.formats["total"])
        
        return ws
    
    def build_summary_sheet(self, wb, data):
        """
        构建汇总工作表
        
        Args:
            wb: 工作簿对象
            data: 所有数据
        """
        ws = wb.add_worksheet("汇总 Summary")
        ws.set_tab_color("#1a1a2e")
        ws.hide_gridlines(2)
        
        # 设置列宽
        ws.set_column(0, 0, 20)
        ws.set_column(1, 1, 15)
        ws.set_column(2, 2, 15)
        ws.set_column(3, 3, 15)
        
        # 写入标题
        ws.merge_range("A1:D1", f"📊 {self.translator.get('labels', 'report_title')}", self.formats["title"])
        ws.write(2, 0, f"{self.translator.get('labels', 'generated_at')}：{datetime.date.today()}", 
                self.formats["label"])
        
        # 语言切换控制
        ws.write(4, 0, f"{self.translator.get('labels', 'language_switch')}:", self.formats["label"])
        ws.write(4, 1, "中文", self.formats["control"])
        ws.write(4, 2, "English", self.formats["control"])
        
        # 汇总数据
        summary_data = [
            {"指标": "SKU 总数", "指标_en": "Total SKUs", "值": len(data["skus"])},
            {"指标": "平台 Listing 数", "指标_en": "Total Listings", "值": len(data["listings"])},
            {"指标": "销售记录数", "指标_en": "Total Sales", "值": len(data["sales"])},
            {"指标": "总销售额 (CNY)", "指标_en": "Total Revenue (CNY)", "值": round(sum(s["amount_cny"] for s in data["sales"]), 2)},
            {"指标": "总订单数", "指标_en": "Total Orders", "值": len(data["sales"])},
            {"指标": "平均客单价 (CNY)", "指标_en": "Avg Order Value (CNY)", "值": round(sum(s["amount_cny"] for s in data["sales"]) / len(data["sales"]), 2)},
            {"指标": "询盘总数", "指标_en": "Total Inquiries", "值": len(data["inquiries"])},
            {"指标": "成交询盘数", "指标_en": "Closed Won", "值": sum(1 for i in data["inquiries"] if i["status"] == "已成交")},
        ]
        
        # 写入表头
        headers = ["指标", "指标_en", "值", "备注"]
        for col, h in enumerate(headers):
            ws.write(6, col, h, self.formats["header_zh"])
        
        # 写入数据
        for row_idx, item in enumerate(summary_data):
            row = 7 + row_idx
            is_even = row_idx % 2 == 1
            
            ws.write(row, 0, item["指标"], self.formats["even"] if is_even else self.formats["text"])
            ws.write(row, 1, item["指标_en"], self.formats["even"] if is_even else self.formats["text"])
            ws.write(row, 2, item["值"], self.formats["money_even"] if is_even else self.formats["money"])
            ws.write(row, 3, "", self.formats["even"] if is_even else self.formats["text"])
        
        return ws
    
    def build_report(self, data, output_path):
        """
        构建完整报告
        
        Args:
            data: 所有数据
            output_path: 输出文件路径
        """
        wb = xlsxwriter.Workbook(output_path)
        self._init_formats(wb)
        
        # 构建各个工作表
        self.build_summary_sheet(wb, data)
        self.build_sku_master_sheet(wb, data["skus"])
        self.build_platform_listing_sheet(wb, data["listings"])
        self.build_inventory_sheet(wb, data["inventory"])
        self.build_daily_sales_sheet(wb, data["sales"])
        self.build_inquiry_sheet(wb, data["inquiries"])
        self.build_weekly_review_sheet(wb, data["weekly_review"])
        
        wb.close()
        
        print(f"✅ 报告已生成：{output_path}")
        print(f"   • 语言：{self.translator.language}")
        print(f"   • SKU 数量：{len(data['skus'])}")
        print(f"   • Listing 数量：{len(data['listings'])}")
        print(f"   • 销售记录：{len(data['sales'])}")
        print(f"   • 库存记录：{len(data['inventory'])}")
        print(f"   • 询盘记录：{len(data['inquiries'])}")
        print(f"   • 周复盘：{len(data['weekly_review'])}")
        print(f"   • 生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    # 测试报告生成
    from data_generator import generate_all_data
    
    data = generate_all_data()
    
    # 生成中文报告
    builder_zh = ReportBuilder(language="zh")
    builder_zh.build_report(data, "cross_border_ops_zh.xlsx")
    
    # 生成英文报告
    builder_en = ReportBuilder(language="en")
    builder_en.build_report(data, "cross_border_ops_en.xlsx")
