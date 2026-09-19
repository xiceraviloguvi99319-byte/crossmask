# CrossMask 中文说明

CrossMask 是一个**本地运行的多文件一致性脱敏工具**。它面向相互关联的 Excel 和 CSV 数据：同一身份在不同文件、不同工作表中出现时，只要使用同一个密钥，就会得到相同的化名，从而尽量保留脱敏后的关联分析能力。

> 当前版本为 v0.1.0 Alpha。自动检测不能保证数据已经完全匿名，任何输出在共享前都必须人工复核。

## 主要功能

- 批量处理 `.xlsx` 和 `.csv`；
- 跨文件、跨工作表生成一致化名；
- 支持常见中英文字段名；
- 处理姓名、手机号、身份证号、银行卡号、邮箱和地址；
- 输出脱敏副本与 Excel 安全检查报告；
- 检查输出中常见的残留敏感信息；
- 不需要连接网络。

## 快速体验

```bash
python -m pip install -e .
crossmask scan examples/input
crossmask run examples/input --output demo-output --secret "replace-this-demo-secret"
crossmask verify demo-output
```

正常使用时，建议通过环境变量设置密钥，避免将密钥写入命令历史：

```bash
export CROSSMASK_SECRET="请替换为长期保存的随机密钥"
crossmask run ./input --output ./safe-output
```

需要多次运行仍保持化名一致时，必须使用同一个密钥。密钥和原始数据都不得提交到 GitHub。

## 输出内容

```text
safe-output/
├── 原文件名_sanitized.xlsx
├── 原文件名_sanitized.csv
└── crossmask_privacy_report.xlsx
```

安全报告仅记录处理数量、字段位置和单向指纹，不复制原始敏感值。

## 配置规则

复制 `crossmask.example.yaml`，按照自己的字段名修改规则：

```yaml
rules:
  - columns: ["姓名", "name", "full_name"]
    entity: person
    action: alias
```

可用动作：`alias`（稳定化名）、`mask`（局部遮盖）、`redact`（统一替换）、`drop`（清空）和 `keep`（保留）。

## 安全边界

- 示例数据全部为人工合成数据；
- 不得上传真实案件、业务或个人数据；
- v0.1 会以单元格值重建工作簿，不保留复杂格式、宏、批注和图表；
- 公式会原样保留，不会自动改写；
- 验证功能只能发现常见格式，不能证明数据已经达到法律意义上的匿名化。

更多内容见 [隐私模型](docs/privacy-model.md) 与 [安全策略](SECURITY.md)。
