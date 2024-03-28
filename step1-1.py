import pandas as pd

########信贷风险等级的量化分析########

# 读取企业信息、进项发票信息和销项发票信息
# pd.read_excel() 用于从 Excel 文件中读取数据
# 读取企业信息
df_enterprise = pd.read_excel("question_content/附件1：123家有信贷记录企业的相关数据.xlsx", sheet_name="企业信息")
# 读取进项发票信息
df_input_invoice = pd.read_excel("question_content/附件1：123家有信贷记录企业的相关数据.xlsx", sheet_name="进项发票信息")
# 读取销项发票信息
df_output_invoice = pd.read_excel("question_content/附件1：123家有信贷记录企业的相关数据.xlsx", sheet_name="销项发票信息")

# 合并进项发票和销项发票信息，计算每家企业的交易额
# pd.concat() 用于将两个 DataFrame 连接起来
# df.groupby().sum() 用于按企业代号分组并计算总金额
# 计算进项发票的总额
df_input_sum = df_input_invoice.groupby("企业代号")["金额"].sum()
# 计算销项发票的总额
df_output_sum = df_output_invoice.groupby("企业代号")["金额"].sum()
# 将进项总额和销项总额合并成一个 DataFrame
df_transaction = pd.concat([df_input_sum, df_output_sum], axis=1)
# 重命名列名
df_transaction.columns = ["进项总额", "销项总额"]
# 计算交易差额
df_transaction["交易差额"] = df_transaction["销项总额"] - df_transaction["进项总额"]

# 合并企业信息和交易信息
# pd.merge() 用于将两个 DataFrame 按照指定的键连接起来
df_enterprise = pd.merge(df_enterprise, df_transaction, left_on="企业代号", right_index=True)

# 根据企业的交易差额等信息，进行信贷风险量化分析（这里仅做示例，实际分析需根据具体情况确定）
# pd.cut() 用于将数值分成离散的区间
df_enterprise["信贷风险等级"] = pd.cut(df_enterprise["交易差额"], bins=3, labels=["高", "中", "低"])

# 根据信贷总额固定时，确定每家企业的贷款额度（这里仅做示例，实际根据具体情况确定）
# 计算每家企业的贷款额度
total_loan_amount = 1000000  # 信贷总额固定为100万元
# 计算每家企业的贷款额度，按照每家企业的交易差额占总交易差额的比例分配
df_enterprise["贷款额度"] = total_loan_amount * df_enterprise["交易差额"] / df_enterprise["交易差额"].sum()

# 设置 pandas 的显示选项
# pd.set_option() 用于设置 pandas 的显示选项
# 设置显示的最大行数为 None，表示所有行都会显示
# pd.set_option('display.max_rows', None)  
# 设置显示的最大列数为 None，表示所有列都会显示
# pd.set_option('display.max_columns', None)  
# 设置显示的宽度为 None，表示自动调整宽度以适应显示内容
# pd.set_option('display.width', None)  

# 输出结果
# 打印出包含企业代号、信贷风险等级和贷款额度的 DataFrame
# print(df_enterprise[["企业代号", "信贷风险等级", "贷款额度"]])
# 将输出结果保存到新的 Excel 文件中
# df_enterprise[["企业代号", "信贷风险等级", "贷款额度"]].to_excel("output_src/step1-1_result.xlsx", index=False)


########制定简单的信贷策略########

# 制定信贷策略
# df.apply() 用于对 DataFrame 的每一行或每一列应用指定的函数
# 根据信贷风险等级确定贷款利率和贷款期限
df_enterprise["贷款利率"] = df_enterprise.apply(lambda row: 0.04 if row["信贷风险等级"] == "低" else 0.06, axis=1)
df_enterprise["贷款期限"] = df_enterprise.apply(lambda row: 1 if row["信贷风险等级"] == "低" else 0.5, axis=1)

# 输出结果
# 打印出包含企业代号、信贷风险等级、贷款额度、贷款利率和贷款期限的 DataFrame
print(df_enterprise[["企业代号", "信贷风险等级", "贷款额度", "贷款利率", "贷款期限"]])
# 将输出结果保存到新的 Excel 文件中
df_enterprise[["企业代号", "信贷风险等级", "贷款额度", "贷款利率", "贷款期限"]].to_excel("output_src/step1-1_result.xlsx", index=False)
