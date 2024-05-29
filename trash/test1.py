import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# 数据加载
data1 = pd.read_excel('../question_content/附件1：123家有信贷记录企业的相关数据.xlsx')
data2 = pd.read_excel('../question_content/附件2：302家无信贷记录企业的相关数据.xlsx')
data3 = pd.read_excel('../question_content/附件3：银行贷款年利率与客户流失率关系的统计数据.xlsx')

# 数据预处理函数
def preprocess_data(data):
    # 处理缺失值
    data = data.dropna()
    # 选择数值型数据
    numerical_features = data.select_dtypes(include=['float64', 'int64']).columns
    data = data[numerical_features]
    # 标准化
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    return pd.DataFrame(data_scaled, columns=numerical_features)

try:
    data1_processed = preprocess_data(data1)
    data2_processed = preprocess_data(data2)
except Exception as e:
    print(f"Error in data preprocessing: {e}")
    data1_processed, data2_processed = None, None

# 假设标签列名为 '信贷风险标签'
label_col = '信贷风险标签'

# 确保数据已成功预处理并且标签列存在
if data1_processed is not None and label_col in data1.columns:
    # 分离特征和标签
    X = data1_processed.drop(label_col, axis=1, errors='ignore')
    y = data1_processed[label_col] if label_col in data1_processed else data1[label_col]

    # 数据集划分
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 模型训练
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # 模型评估
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
else:
    print("Data is not ready for model training. Please check the preprocessing steps or label column.")