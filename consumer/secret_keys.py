from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
class SecretKeys(BaseSettings):
    AWS_SQS_RAW_VIDEO_PROCESSING : str = ""
    REGION_NAME: str = ""
    