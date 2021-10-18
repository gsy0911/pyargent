from injector import Module, Binder

# interface
from pyargent.entity.salary import SalaryRepository

# external
from pyargent.infrastructure import SalaryLocal, SalaryS3


class DiS3(Module):
    """
    DIコンテナ

    Args:
        s3_bucket: データ保存に利用するのS3バケットの名前
    """

    def __init__(self, s3_bucket: str, prefix: str):
        self.s3_bucket = s3_bucket
        self.prefix = prefix

    def configure(self, binder: Binder) -> None:
        # データの保存とか
        binder.bind(SalaryRepository, SalaryS3(s3_bucket=self.s3_bucket, prefix=self.prefix))


class DiLocal(Module):
    """
    DIコンテナ

    """

    def __init__(self, prefix: str):
        self.prefix = prefix

    def configure(self, binder: Binder) -> None:
        # データの保存とか
        binder.bind(SalaryRepository, SalaryLocal(prefix=self.prefix))
