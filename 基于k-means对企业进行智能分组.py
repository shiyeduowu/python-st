# 导入工具包
import numpy as np  # numpy:数据处理库
import pandas as pd  # pandas :数据分析库
from sklearn.cluster import KMeans  # 导入K均值聚类算法
from sklearn import preprocessing  # sklearn:机器学习库
from sklearn import metrics
import matplotlib.pyplot as plt  # matplotlib：数据可视化库
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['simhei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示


#获取数据
data = pd.read_csv('聚类分析原表.csv')


# 数据清洗
# 数据存在空值, 删除空值
data = data.dropna()
# 删除完全一样的数据，去重
data = data.drop_duplicates()


#选择聚类变量的数据
df = data[['净资产收益率','营业利润率','总资产报酬率']]

# 手肘法找到最佳聚类个数
# 存储每次聚类的误差平方和
squares_sum = []
# 遍历多个可能的候选簇数量
for n_clusters in range(1, 9):
    kmeans = KMeans(n_clusters = n_clusters)
    kmeans.fit(df)
    squares_sum.append(kmeans.inertia_)  # 衡量模型性能
    
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(squares_sum) + 1), squares_sum)
plt.grid(linestyle=':')
plt.xlabel('聚类个数')
plt.ylabel('SSE')
plt.title('样本到其最近的聚类中心的距离的平方之和')
plt.show()

best_k = input("请输入最佳聚类个数：")
best_k = int(best_k)


#建立模型
kmodel = KMeans(n_clusters=best_k )
#训练模型
kmodel.fit(data)

#模型评估
labels = kmodel.labels_
# 平均轮廓系数  越大越好
silhouette_value = metrics.silhouette_score(df, labels)
print('平均轮廓系数(越大越好)：', silhouette_value)
# DBI指数  越小越好
DBI_value = metrics.davies_bouldin_score(df, labels)
print('DBI指数(越小越好)：', DBI_value)

data['标签'] = labels
data.to_csv('基于k-means实现航空公司客户价值分析/聚类结果.csv', index=False, encoding='utf-8-sig')
