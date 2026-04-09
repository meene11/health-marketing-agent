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

    # Facebook
    facebook_page_id: str = ""
    facebook_page_access_token: str = ""

    # 슬랙 알림
    slack_webhook_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
