from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_health_table: str = "health_data"

    # 네이버 블로그
    naver_id: str = ""
    naver_password: str = ""
    naver_blog_id: str = ""

    # WordPress
    wordpress_site: str = ""
    wordpress_username: str = ""
    wordpress_app_password: str = ""

    # 인스타그램
    instagram_username: str = ""
    instagram_password: str = ""

    # 슬랙
    slack_webhook_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
