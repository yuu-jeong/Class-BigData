import seaborn as sns
import pandas as pd

#1. 데이터 준비
#seaborn 내장 데이터셋 csv 파일로 저장
titanic = sns.load_dataset("titanic")
titanic.to_csv('./titanic.csv', index = False)

#2. 데이터 탐색
#결측값 확인
print(titanic.isnull().sum())

titanic['age'] = titanic['age'].fillna(titanic['age'].median()) #나이는 중앙값
print(titanic['embarked'].value_counts()) #최빈값 확인

titanic['embarked']=titanic['embarked'].fillna('S') #embarked는 최빈값
print(titanic['embark_town'].value_counts())

titanic['embark_town'] = titanic['embark_town'].fillna('Southampton')
print(titanic['deck'].value_counts())
titanic['deck']=titanic['deck'].fillna('C')

#결측치가 모두 0인 것 확인
print(titanic.isnull().sum())

#기본 정보 확인하기
titanic.info()
titanic.survived.value_counts()
titanic.to_csv('./titanic2.csv', index = False)

#시각적 데이터 탐색1 > pie 차트
#성별별 생존자 수를 차트로 나타내기 
import matplotlib.pyplot as plt

male_color=['red', 'grey']
female_color=['grey', 'red']

plt.subplot(1, 2, 1)
titanic['survived'][titanic['sex']=='male'].value_counts().plot.pie(explode=[0, 0.1], colors=male_color, autopct='%1.1f%%', shadow=True)
plt.title('Survived(Male)')

plt.subplot(1, 2, 2)
titanic['survived'][titanic['sex']=='female'].value_counts().plot.pie(explode=[0, 0.1], colors=female_color, autopct='%1.1f%%', shadow=True)
plt.title('Survived(Female)')

plt.show()

#시각적 데이터 탐색2 > 막대 그래프
#등급별 생존자 수를 차트로 나타내기 
import seaborn as sns
sns.countplot(x='pclass', hue='survived', data=titanic)
plt.title('Pclass vs Servived')
plt.show()

#3. 데이터 모델링
# 피어쓴 상관 분석
corr_vars = ['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']
titanic_corr = titanic[corr_vars].corr(method='pearson')
titanic_corr.to_csv('titanic_corr.csv', index=False)

titanic_corr.to_csv('titanic_corr.csv', index="False")

# 특정 변수 사이의 상관계
titanic['survived'].corr(titanic['adult_male'])
titanic['survived'].corr(titanic['fare'])

# 산점도로 상관 분석 시각화
sns.pairplot(titanic, hue='survived')
plt.show()

# 두 변수의 상관 관계 시각화
sns.catplot(x='pclass', y='survived', hue='sex', data=titanic, kind='point')
plt.show()

# 한글 폰트 설정
from matplotlib import rcParams
rcParams['font.family'] = 'NanumGothic'

# 남녀 사망자 비율 Pie Chart
# 1등급 남녀 사망자 비율
plt.subplot(1, 3, 1)
titanic['sex'][titanic['pclass']==1][titanic['survived']==0].value_counts().plot.pie(explode=[0, 0.1], colors=['red', 'grey'], autopct='%1.1f%%', shadow=True)
plt.ylabel('sex')
plt.title('1등급 남녀 사망자 비율')

# 2등급 남녀 사망자 비율
plt.subplot(1, 3, 2)
titanic['sex'][titanic['pclass']==2][titanic['survived']==0].value_counts().plot.pie(explode=[0, 0.1], colors=['red', 'grey'], autopct='%1.1f%%', shadow=True)
plt.ylabel('sex')
plt.title('2등급 남녀 사망자 비율')

# 3등급 남녀 사망자 비율
plt.subplot(1, 3, 3)
titanic['sex'][titanic['pclass']==3][titanic['survived']==0].value_counts().plot.pie(explode=[0, 0.1], colors=['red', 'grey'], autopct='%1.1f%%', shadow=True)
plt.ylabel('sex')
plt.title('3등급 남녀 사망자 비율')

plt.show()
