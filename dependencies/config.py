from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  azure_openai_embeddings_api_key: str
  azure_openai_embeddings_host_url: str
  
  azure_openai_gpt4omini_api_key: str
  azure_openai_gpt4omini_host_url: str
  
  pinecone_api_key: str
  
  mail_username: str
  mail_password: str
  mail_from: str
  mail_port: int
  mail_server: str
  model_config = SettingsConfigDict(env_file=".env")


def get_settings():
  return Settings()