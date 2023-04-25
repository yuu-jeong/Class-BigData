import pandas as pd
# 1. 엑셀에서 열 구분자를 세미콜론으로 인식시키기
red_df=pd.read_csv('./winequality-red.csv', sep=';', header=0, engine='python')
red_df.to_csv('./winequality-red2.csv', index=False)
white_df=pd.read_csv('./winequality-white.csv', sep=';', header=0, engine='python')
white_df.to_csv('./winequality-white2.csv',index=False)

# 2. 데이터 병합하기
#레드와인 데이터
print(red_df.head())
print(red_df.shape)
print(red_df.insert(0, column='type', value='red'))
print(red_df.head())
print(red_df.shape)


#화이트와인 데이터
print(white_df.head())
print(white_df.shape)
print(white_df.insert(0, column='type', value='white'))
print(white_df.head())
print(white_df.shape)

wine = pd.concat([red_df, white_df])
wine.to_csv('./wine.csv', index=False)
wine.shape

#기본 정보 확인하기
print(wine.info())

wine.columns = wine.columns.str.replace(' ', '_')
wine.to_csv('./wine.csv', index=False)
wine.head()

wine.describe() #해당 데이터의 기술 통계값 출력
desResult = wine.describe()
desResult.to_csv('./descriptive.csv')

#데이터 탐색 결과
wine.info()
print(wine.describe())
print(sorted(wine.quality.unique())) #속성값 중 유일한 값 출력
print(wine.quality.value_counts()) # 속성값의 빈도 수 출력

#3. 데이터 모델링: 기술 통계 분석
#type 별 그룹 비교하기
print(wine.groupby('type')['quality'].describe())

#agg()로 다중 통계량 구하기
print(wine.groupby('type').agg(['mean','var']))
print(wine.groupby('type').agg({'quality':'mean','alcohol':'max'}))
print(wine.groupby('type').agg({'quality':['mean','std'],'alcohol':['mean','std']}))

#4. 데이터 모델링: 회귀 분석
#종속변수(v) 독립변수(x1~x10) 구성
from scipy import stats
from statsmodels.formula.api import ols, glm

#종속변수 quality ~ 독립변수1+ ... + 독립변수quality
Rformula='quality~fixed_acidity+volatile_acidity+citric_acid+residual_sugar+chlorides+free_sulfur_dioxide+free_sulfur_dioxide+density+pH+sulphates+alcohol'
regression_result = ols(Rformula, data=wine).fit()
print(regression_result.summary())

#회귀 분석 모델로 새로운 샘플 품질 등급 예측
sample1 = wine[wine.columns.difference(['quality', 'type'])]
sample1 = sample1[0:5][:]

sample1_predict = regression_result.predict(sample1)
print(sample1_predict)

wine[0:5]['quality']
'''
data={"fixed_acidity":[8.5, 8.1],
      "volatile_acidity":[0.8, 0.5],
      "citric_acid":[0.3, 0.4],
      "residual_sugar":[6.1, 5.8],
      "cholorides":[0.055, 0.04],
      "free_sulfur_dioxide":[30.0, 30.1],
      "total_sulfur_dioxide":[98.0, 99],
      "density":[0.996, 0.91],
      "pH":[3.25, 3.01],
      "sulphates":[0.4, 0.35],
      "alcohol":[9.0, 0.88]}
sample2 = pd.DataFrame(data, columns=sample1.columns)
sample2_predict=regression_result.predict(sample2)
print(sample2_predict)
'''

#5. 결과 시각화
import matplotlib.pyplot as plt
import seaborn as sns

# 와인 유형에 따른 품질 등급 히스토그램 그리기
sns.set_style('dark')
sns.histplot(red_df['quality'], kde=True, color='red', label='red wine')
sns.histplot(white_df['quality'], kde=True, label='white wine')
plt.title("Quality of Wine Type")
plt.legend()
plt.show()

# 부분 회귀 플롯으로 시각화
import statsmodels.api as sm

fig=plt.figure(figsize=(8,13))
sm.graphics.plot_partregress_grid(regression_result, fig=fig)
plt.show()
