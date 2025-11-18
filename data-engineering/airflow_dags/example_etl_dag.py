"""
예제 ETL DAG

이 DAG는 데이터 추출, 변환, 로드의 전체 ETL 프로세스를 보여줍니다.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# DAG 기본 설정
default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['alert@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1),
}


def extract_data(**context):
    """
    데이터 추출 작업
    외부 소스에서 데이터를 추출합니다.
    """
    logger.info("Starting data extraction...")

    # 예제: CSV 파일 읽기 (실제로는 API, DB 등에서 추출)
    try:
        df = pd.DataFrame({
            'user_id': range(1, 101),
            'age': [20 + (i % 50) for i in range(100)],
            'purchases': [i * 10 for i in range(100)],
            'category': ['A', 'B', 'C', 'D'] * 25
        })

        # XCom에 데이터 전달
        context['ti'].xcom_push(key='raw_data', value=df.to_json())
        logger.info(f"Extracted {len(df)} rows")

        return "extract_success"

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise


def validate_data(**context):
    """
    데이터 검증 작업
    데이터 품질 체크를 수행합니다.
    """
    logger.info("Starting data validation...")

    # XCom에서 데이터 가져오기
    raw_data = context['ti'].xcom_pull(key='raw_data', task_ids='extract')
    df = pd.read_json(raw_data)

    # 검증 로직
    validations = {
        'row_count': len(df) > 0,
        'no_nulls': df.isnull().sum().sum() == 0,
        'valid_age': (df['age'] >= 0).all() and (df['age'] <= 120).all(),
        'valid_purchases': (df['purchases'] >= 0).all(),
    }

    logger.info(f"Validation results: {validations}")

    if not all(validations.values()):
        raise ValueError("Data validation failed!")

    return "validation_success"


def transform_data(**context):
    """
    데이터 변환 작업
    비즈니스 로직에 따라 데이터를 변환합니다.
    """
    logger.info("Starting data transformation...")

    # XCom에서 데이터 가져오기
    raw_data = context['ti'].xcom_pull(key='raw_data', task_ids='extract')
    df = pd.read_json(raw_data)

    # 변환 로직
    # 1. 새로운 특성 생성
    df['age_group'] = pd.cut(df['age'], bins=[0, 30, 50, 100],
                              labels=['young', 'middle', 'senior'])
    df['high_value'] = df['purchases'] > df['purchases'].median()

    # 2. 집계 (예: 카테고리별 통계)
    category_stats = df.groupby('category').agg({
        'purchases': ['mean', 'sum', 'count']
    }).reset_index()

    # 3. 정규화
    df['normalized_purchases'] = (df['purchases'] - df['purchases'].mean()) / df['purchases'].std()

    # XCom에 변환된 데이터 전달
    context['ti'].xcom_push(key='transformed_data', value=df.to_json())
    context['ti'].xcom_push(key='category_stats', value=category_stats.to_json())

    logger.info(f"Transformed {len(df)} rows")
    return "transform_success"


def load_data(**context):
    """
    데이터 로드 작업
    변환된 데이터를 최종 저장소에 저장합니다.
    """
    logger.info("Starting data loading...")

    # XCom에서 변환된 데이터 가져오기
    transformed_data = context['ti'].xcom_pull(key='transformed_data', task_ids='transform')
    category_stats = context['ti'].xcom_pull(key='category_stats', task_ids='transform')

    df = pd.read_json(transformed_data)
    stats_df = pd.read_json(category_stats)

    # 저장 (예제: CSV로 저장, 실제로는 DB, Data Warehouse 등)
    output_path = '/tmp/airflow_output'
    df.to_csv(f'{output_path}/transformed_data.csv', index=False)
    stats_df.to_csv(f'{output_path}/category_stats.csv', index=False)

    logger.info(f"Loaded {len(df)} rows to {output_path}")
    return "load_success"


def send_notification(**context):
    """
    완료 알림 전송
    """
    logger.info("Sending completion notification...")

    # 실행 정보 수집
    execution_date = context['execution_date']
    dag_id = context['dag'].dag_id

    message = f"""
    ETL Pipeline Completed Successfully!
    DAG: {dag_id}
    Execution Date: {execution_date}
    """

    logger.info(message)
    # 실제로는 이메일, Slack 등으로 알림 전송
    return "notification_sent"


# DAG 정의
with DAG(
    'example_etl_pipeline',
    default_args=default_args,
    description='Example ETL pipeline with data extraction, transformation, and loading',
    schedule_interval='@daily',  # 매일 실행
    catchup=False,
    tags=['etl', 'example', 'data-engineering'],
) as dag:

    # 시작 작업
    start = BashOperator(
        task_id='start',
        bash_command='echo "Starting ETL pipeline..."'
    )

    # 데이터 추출
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        provide_context=True
    )

    # 데이터 검증
    validate = PythonOperator(
        task_id='validate',
        python_callable=validate_data,
        provide_context=True
    )

    # 데이터 변환
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        provide_context=True
    )

    # 데이터 로드
    load = PythonOperator(
        task_id='load',
        python_callable=load_data,
        provide_context=True
    )

    # 알림 전송
    notify = PythonOperator(
        task_id='notify',
        python_callable=send_notification,
        provide_context=True
    )

    # 종료 작업
    end = BashOperator(
        task_id='end',
        bash_command='echo "ETL pipeline completed!"'
    )

    # Task Dependencies
    start >> extract >> validate >> transform >> load >> notify >> end
