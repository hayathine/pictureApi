import logging
from logging import StreamHandler, Formatter
from logging import INFO

# ロガーの作成
def get_logger(name):
#ストリームハンドラーの作成
    handler = StreamHandler()
    handler.setLevel(INFO)
    handler.setFormatter(Formatter("%(message)s"))

    logging.basicConfig(level=INFO, handlers=[handler])