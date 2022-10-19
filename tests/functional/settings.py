from pydantic import BaseSettings, Field


# ...


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    # es_index: str =
    # es_id_field: str =
    # es_index_mapping: dict =

    redis_host: str = Field('http://127.0.0.1:6379', env='REDIS_HOST')
    service_url: str = Field('http://127.0.0.1:8106', env='SERVICE_HOST')


test_settings = TestSettings()
