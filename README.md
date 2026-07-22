# 跨境运营数据追踪系统 📊

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![xlsxwriter](https://img.shields.io/badge/xlsxwriter-3.x-green.svg)](https://xlsxwriter.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Python xlsxwriter 实战项目：自动生成跨境运营专用多维追踪台账**

本项目基于 excel-report-automation 改造，从"通用 Excel 报表"升级为"跨境运营专用多维追踪台账"，支持中英文双语表头，可一键切换。

## ✨ 功能特性

- ✅ **多工作表结构**：6 个核心工作表 + 汇总表
- ✅ **中英双语支持**：所有表头支持中英文切换
- ✅ **空气能热泵场景**：模拟真实的跨境销售数据
- ✅ **自动数据聚合**：按品类、平台、日期等多维度汇总
- ✅ **图表可视化**：柱状图、折线图、饼图
- ✅ **条件格式化**：大额订单高亮、库存预警

## 📂 工作表结构

| 工作表 | 中文名 | 英文名 | 用途 |
|--------|--------|--------|------|
| 1 | 汇总 Summary | Summary | 总览数据、语言切换控制 |
| 2 | SKU 主档 | SKU Master | 产品基础信息管理 |
| 3 | 平台 Listing 状态 | Platform Listing | 各平台上架状态追踪 |
| 4 | 库存追踪 | Inventory Tracking | 库存变动记录 |
| 5 | 销售日表 | Daily Sales | 每日销售记录 |
| 6 | 询盘记录 | Inquiry Records | 客户询盘跟踪 |
| 7 | 每周复盘 | Weekly Review | 周度运营分析 |

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/liaogengqin-creator/cross-border-ops-dashboard-—-跨境运营数据追踪系统.git
cd cross-border-ops-dashboard-—-跨境运营数据追踪系统
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python main.py
```

### 输出文件

运行成功后，在 `output/` 目录下会生成两个 Excel 文件：
- `跨境运营追踪台账_中文_YYYYMMDD.xlsx` - 中文版报告
- `Cross-border_Ops_Dashboard_EN_YYYYMMDD.xlsx` - 英文版报告

## 📊 示例数据场景

### 产品线
- **空气能热泵**：5HP / 10HP / 15HP 三个规格
- **中央空调**：12HP
- **空气能热水器**：50L

### 销售平台
- Amazon US / Amazon DE / Amazon UK
- eBay
- 独立站

### 目标市场
- 美国 (US)、德国 (DE)、英国 (UK)
- 澳大利亚 (AU)、加拿大 (CA)

## 🛠 技术栈

- **Python**：3.8+
- **xlsxwriter**：3.x（Excel 写入引擎）
- **架构**：模块化设计，数据层与展示层分离

## 📁 项目结构

```
cross-border-ops-dashboard/
├── main.py                    # 主程序入口
├── config.py                  # 配置文件（币种、汇率、平台等）
├── data_generator.py          # Sample data 生成器
├── report_builder.py          # 报告生成器（核心逻辑）
├── translators.py             # 双语翻译器
├── requirements.txt           # 依赖管理
├── README.md                  # 项目文档
└── output/                    # 输出目录
    ├── 跨境运营追踪台账_中文_YYYYMMDD.xlsx
    └── Cross-border_Ops_Dashboard_EN_YYYYMMDD.xlsx
```

## 🔧 自定义配置

### 修改币种汇率

编辑 `config.py` 中的 `CURRENCIES` 字典：

```python
CURRENCIES = {
    "USD": {"symbol": "$", "rate": 7.25, "name": "美元"},
    "EUR": {"symbol": "€", "rate": 7.80, "name": "欧元"},
    # 添加更多币种...
}
```

### 修改产品数据

编辑 `data_generator.py` 中的 `generate_sku_master()` 函数：

```python
def generate_sku_master():
    skus = [
        {
            "sku_id": "SKU-HP-005",
            "product_name": "空气能热泵 5HP",
            # 添加更多产品...
        }
    ]
    return skus
```

### 修改双语翻译

编辑 `translators.py` 中的翻译表：

```python
def _load_translations(self):
    return {
        "sku_master_headers": {
            "zh": ["SKU 编码", "产品名称", ...],
            "en": ["SKU ID", "Product Name", ...]
        }
    }
```

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📝 更新日志

### [1.0.0] - 2026-07-22
- 初始版本发布
- 支持 7 个工作表：SKU 主档、平台 Listing、库存追踪、销售日表、询盘记录、每周复盘、汇总
- 中英文双语表头支持
- 空气能热泵跨境销售场景示例数据
- 条件格式：大额订单高亮、库存预警
- 图表可视化：柱状图、折线图、饼图

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

