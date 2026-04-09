import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase (건강 DB)
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_health_table: str = "documents_v2"

    # 네이버 블로그
    naver_id: str = ""
    naver_password: str = ""
    naver_blog_id: str = ""

    # WordPress
    wordpress_site: str = ""
    wordpress_username: str = ""
    wordpress_app_password: str = ""

    # Blogger (구글 블로그)
    blogger_blog_id: str = ""
    blogger_client_id: str = ""
    blogger_client_secret: str = ""
    blogger_refresh_token: str = ""  # 배포 환경용 (blogger_token.json 대체)

    # 슬랙 알림
    slack_webhook_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()


def refresh_from_streamlit():
    """Streamlit secrets에서 settings 값을 직접 업데이트한다."""
    try:
        import streamlit as st
        for key, value in st.secrets.items():
            if isinstance(value, str):
                attr = key.lower()
                if hasattr(settings, attr):
                    object.__setattr__(settings, attr, value)
    except Exception:
        pass
