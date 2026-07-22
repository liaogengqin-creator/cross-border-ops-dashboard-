"""
跨境运营数据追踪系统 - 主程序入口

生成空气能热泵跨境销售场景的示例 Excel 报告
"""

import datetime
import os
from data_generator import generate_all_data
from report_builder import ReportBuilder


def main():
    """主函数"""
    print("🚀 跨境运营数据追踪系统")
    print("=" * 50)
    
    # 生成示例数据
    print("📊 正在生成示例数据...")
    data = generate_all_data()
    
    # 创建输出目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成中文报告
    print("\n📝 正在生成中文报告...")
    output_zh = os.path.join(output_dir, f"跨境运营追踪台账_中文_{datetime.date.today().strftime('%Y%m%d')}.xlsx")
    builder_zh = ReportBuilder(language="zh")
    builder_zh.build_report(data, output_zh)
    
    # 生成英文报告
    print("\n📝 正在生成英文报告...")
    output_en = os.path.join(output_dir, f"Cross-border_Ops_Dashboard_EN_{datetime.date.today().strftime('%Y%m%d')}.xlsx")
    builder_en = ReportBuilder(language="en")
    builder_en.build_report(data, output_en)
    
    print("\n" + "=" * 50)
    print("✅ 所有报告生成完成！")
    print(f"   中文报告：{output_zh}")
    print(f"   英文报告：{output_en}")
    print("\n💡 提示：")
    print("   - 汇总工作表中有语言切换控制（但 Excel 公式切换需要手动设置）")
    print("   - 所有工作表都包含中英双语表头")
    print("   - 数据基于空气能热泵跨境销售场景模拟")


if __name__ == "__main__":
    main()
