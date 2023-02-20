from logging import getLogger, StreamHandler, DEBUG, INFO
import sys
import boto3  # Sagemaker SDKとしては必須ではないが、任意のAWSプロファイルを指定して実行するため利用。
import sagemaker
from sagemaker import get_execution_role
from sagemaker.tensorflow import TensorFlow

# ログ出力設定
stdout_handler = StreamHandler(stream=sys.stdout)
stdout_handler.setLevel(DEBUG)
logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(stdout_handler)

# セッション作成
boto3_session = boto3.Session(profile_name="sagemaker-poc-profile")
sagemaker_session = sagemaker.Session(boto_session=boto3_session)

# IAMロール/実行リージョン/デフォルトバケット取得
execute_role = "arn:aws:iam::017094810799:role/service-role/AmazonSageMaker-ExecutionRole-20230201T172445"
region = sagemaker_session.boto_session.region_name
default_bucket = sagemaker_session.default_bucket()

# MNISTデータ格納先バケットの設定
training_data_uri = "s3://sagemaker-sample-data-{}/tensorflow/mnist".format(
    region)

# デバック情報出力

logger.debug("region = {}".format(region))
logger.debug("default_bucket    = {}".format(default_bucket))
logger.debug("execute_role      = {}".format(execute_role))
logger.debug("training_data_url = {}".format(training_data_uri))


# Sagemakerのトレーニング用エンドポイント作成
mnist_estimator2 = TensorFlow(
    entry_point="src/mnist-2.py",
    role=execute_role,
    instance_count=2,
    instance_type="ml.p3.2xlarge",
    framework_version="2.1.0",
    py_version="py3",
    distribution={"parameter_server": {"enabled": True}},
    sagemaker_session=sagemaker_session,
)

# トレーニングの実行
mnist_estimator2.fit(training_data_uri)