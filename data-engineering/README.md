# 데이터 엔지니어링 (Data Engineering)

ETL 파이프라인, 특성 공학, 실시간 데이터 처리

## 📚 학습 내용

### 1. ETL 파이프라인 (Apache Airflow)
- DAG (Directed Acyclic Graph) 구성
- Task Dependencies
- 스케줄링 및 모니터링
- 📓 [01_airflow_etl.ipynb](./notebooks/01_airflow_etl.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/data-engineering/notebooks/01_airflow_etl.ipynb)

### 2. 특성 공학 (Feature Engineering)
- Feature Selection
- Feature Transformation
- Feature Extraction
- Automated Feature Engineering
- 📓 [02_feature_engineering.ipynb](./notebooks/02_feature_engineering.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/data-engineering/notebooks/02_feature_engineering.ipynb)

### 3. 데이터 검증 (Data Validation)
- Great Expectations
- Data Quality Checks
- Schema Validation
- 📓 [03_data_validation.ipynb](./notebooks/03_data_validation.ipynb)

### 4. 실시간 데이터 처리
- Apache Kafka
- Spark Streaming
- Real-time Feature Store
- 📓 [04_realtime_processing.ipynb](./notebooks/04_realtime_processing.ipynb)

### 5. 데이터 레이크 & 웨어하우스
- Delta Lake
- Apache Iceberg
- Data Lakehouse Architecture
- 📓 [05_data_lakehouse.ipynb](./notebooks/05_data_lakehouse.ipynb)

## 🚀 빠른 시작

```bash
# 의존성 설치
pip install -r requirements.txt

# Airflow 초기화
export AIRFLOW_HOME=~/airflow
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Airflow 시작
airflow webserver --port 8080
airflow scheduler
```

## 💻 주요 예제

### Apache Airflow DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_data(**context):
    """데이터 추출"""
    import pandas as pd
    df = pd.read_csv('data/raw/input.csv')
    context['ti'].xcom_push(key='raw_data', value=df.to_json())

def transform_data(**context):
    """데이터 변환"""
    import pandas as pd
    import json
    raw_data = context['ti'].xcom_pull(key='raw_data', task_ids='extract')
    df = pd.read_json(json.loads(raw_data))

    # 변환 로직
    df['processed'] = df['value'] * 2
    context['ti'].xcom_push(key='transformed_data', value=df.to_json())

def load_data(**context):
    """데이터 로드"""
    import pandas as pd
    import json
    transformed_data = context['ti'].xcom_pull(key='transformed_data', task_ids='transform')
    df = pd.read_json(json.loads(transformed_data))
    df.to_csv('data/processed/output.csv', index=False)

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline Example',
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load_data,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
```

### 특성 공학

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from feature_engine.creation import CyclicalFeatures
from feature_engine.encoding import RareLabelEncoder

# 데이터 로드
df = pd.read_csv('data.csv')

# 1. 시간 특성
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek

# 2. 순환 특성 (Cyclical Features)
cyclical = CyclicalFeatures(
    variables=['month', 'day_of_week'],
    drop_original=False
)
df = cyclical.fit_transform(df)

# 3. 범주형 인코딩
rare_encoder = RareLabelEncoder(
    tol=0.05,
    n_categories=1,
    variables=['category']
)
df = rare_encoder.fit_transform(df)

# 4. 특성 스케일링
scaler = StandardScaler()
numeric_features = ['feature1', 'feature2', 'feature3']
df[numeric_features] = scaler.fit_transform(df[numeric_features])

# 5. 특성 선택
selector = SelectKBest(score_func=f_classif, k=10)
X_selected = selector.fit_transform(X, y)
```

### Great Expectations 데이터 검증

```python
import great_expectations as gx

# Context 생성
context = gx.get_context()

# 데이터소스 추가
datasource = context.sources.add_pandas("my_datasource")
data_asset = datasource.add_dataframe_asset(name="my_dataframe_asset")

# Batch Request
batch_request = data_asset.build_batch_request(dataframe=df)

# Expectation Suite 생성
expectation_suite_name = "my_suite"
context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)

# Validator 생성
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
)

# Expectations 추가
validator.expect_table_row_count_to_be_between(min_value=100, max_value=100000)
validator.expect_column_values_to_not_be_null(column="user_id")
validator.expect_column_values_to_be_between(column="age", min_value=0, max_value=120)
validator.expect_column_values_to_be_in_set(column="status", value_set=["active", "inactive"])

# 검증 실행
results = validator.validate()
print(results)
```

### Apache Kafka 실시간 처리

```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 메시지 전송
data = {'user_id': 123, 'action': 'click', 'timestamp': '2024-01-01T10:00:00'}
producer.send('user_events', value=data)
producer.flush()

# Consumer
consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# 메시지 처리
for message in consumer:
    data = message.value
    print(f"Received: {data}")
    # 실시간 특성 추출 및 처리
    process_event(data)
```

### PySpark 데이터 처리

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, when

# Spark 세션 생성
spark = SparkSession.builder \
    .appName("DataProcessing") \
    .getOrCreate()

# 데이터 로드
df = spark.read.csv("data/large_dataset.csv", header=True, inferSchema=True)

# 데이터 변환
df_transformed = df \
    .withColumn("processed_value", col("value") * 2) \
    .withColumn("category", when(col("value") > 100, "high").otherwise("low")) \
    .groupBy("category") \
    .agg(
        count("*").alias("count"),
        avg("value").alias("avg_value")
    )

# 결과 저장
df_transformed.write \
    .mode("overwrite") \
    .parquet("data/output.parquet")

spark.stop()
```

## 🎯 주요 기술 스택

### 워크플로우 오케스트레이션
- ✅ Apache Airflow - ETL 파이프라인
- ✅ Prefect - 현대적인 워크플로우 엔진
- ✅ Dagster - 데이터 파이프라인

### 데이터 처리
- ✅ Apache Spark - 대규모 데이터 처리
- ✅ Pandas - 데이터 분석
- ✅ Polars - 고성능 데이터프레임

### 실시간 처리
- ✅ Apache Kafka - 메시지 큐
- ✅ Apache Flink - 스트림 처리
- ✅ Spark Streaming - 실시간 분석

### 데이터 저장
- ✅ Delta Lake - 데이터 레이크
- ✅ Apache Iceberg - 테이블 포맷
- ✅ PostgreSQL - RDBMS
- ✅ MongoDB - NoSQL

### 데이터 품질
- ✅ Great Expectations - 데이터 검증
- ✅ Deequ - 데이터 품질
- ✅ Soda - 데이터 관찰성

## 📊 Feature Store

### Feast (Feature Store)

```python
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from feast.types import Int64, Float32, String
from datetime import timedelta

# Entity 정의
user = Entity(
    name="user_id",
    value_type=ValueType.INT64,
    description="User ID"
)

# Feature View 정의
user_features = FeatureView(
    name="user_features",
    entities=["user_id"],
    ttl=timedelta(days=1),
    features=[
        Feature(name="age", dtype=ValueType.INT64),
        Feature(name="total_purchases", dtype=ValueType.INT64),
        Feature(name="avg_purchase_amount", dtype=ValueType.FLOAT),
    ],
    online=True,
    batch_source=FileSource(
        path="data/user_features.parquet",
        event_timestamp_column="timestamp",
    )
)
```

## 🔧 프로젝트 구조

```
data-engineering/
├── notebooks/          # Jupyter 노트북
├── scripts/            # Python 스크립트
│   ├── etl_pipeline.py
│   ├── feature_engineering.py
│   └── data_validation.py
├── airflow_dags/       # Airflow DAG 파일
│   ├── daily_etl.py
│   └── weekly_batch.py
├── data/               # 데이터 디렉토리
│   ├── raw/
│   ├── processed/
│   └── features/
├── configs/            # 설정 파일
│   ├── airflow.cfg
│   └── spark-defaults.conf
└── requirements.txt
```

## 🚀 실전 프로젝트

1. **실시간 추천 시스템**: Kafka + Spark Streaming
2. **데이터 레이크하우스**: Delta Lake + Databricks
3. **특성 파이프라인**: Airflow + Feature Store
4. **데이터 품질 모니터링**: Great Expectations
5. **ETL 자동화**: Airflow + dbt

## 📈 성능 최적화

- Partitioning & Bucketing
- Columnar Storage (Parquet, ORC)
- Caching & Materialized Views
- Parallel Processing
- Incremental Processing

## 🔒 데이터 거버넌스

- Data Lineage (Apache Atlas)
- Data Catalog (AWS Glue, Datahub)
- Access Control (Ranger)
- Audit Logging
- Data Masking & Encryption

---

**축하합니다! 모든 섹션을 완료했습니다!**

다음 단계로 [프로젝트 선택](../)하여 실전 학습을 시작하세요!
