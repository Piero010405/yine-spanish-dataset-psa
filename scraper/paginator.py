from config.constants import BASE_URL, LIST_ENDPOINT

def build_page_url(page: int) -> str:
    return f"{BASE_URL}{LIST_ENDPOINT}?combine=&page={page}"
