import requests
import json


class GrowiAPIError(Exception):
    """GrowiAPIのエラーを表す例外クラス"""
    def __init__(self, description):
        super().__init__()
        self.description = description
    
    def __repr__(self):
        return str(self.description)

    def __str__(self):
        return str(self.description)


def get_page_list(url: str, access_token: str, path: str) -> dict:
    """複数記事の取得
    Args:
        url: GrowiのURL
        access_token: APIトークン
        path: 取得する記事のパス
    Returns:
        res (dict): 複数記事の情報
    """
    api_endpoint = f'{url}/_api/v3/pages/list'

    params = {
        'access_token': access_token,
        'path': path,
    }

    res = requests.get(api_endpoint, params=params)
    print(f'response_code: {res.status_code}')

    if res.status_code == 200:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)

def get_page_info(url: str, access_token: str, pageId: str) -> dict:
    """記事の詳細情報取得
    Args:
        url: GrowiのURL
        access_token: APIトークン
        pageId: 取得する記事のID
    Returns:
        dict: 記事の詳細情報
    """
    api_endpoint = f'{url}/_api/v3/page'

    params = {
        'access_token': access_token,
        'pageId': pageId,
    }

    res = requests.get(api_endpoint, params=params)
    print(f'response_code: {res.status_code}')

    if res.status_code == 200:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)
    
def create_page(url: str, access_token: str, path: str, body: str) -> None:
    api_endpoint = f'{url}/_api/v3/page'
    params = {
        'access_token': access_token,
    }
    data = {
        'path': path,
        'body': body,
    }

    res = requests.post(api_endpoint, data=data, params=params)
    print(f'response_code: {res.status_code}')

    if res.status_code == 201:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)


def update_page(url: str, access_token: str, pageId: str, revisionId: str ,body: str) -> None:
    api_endpoint = f'{url}/_api/v3/page'
    params = {
        'access_token': access_token,
    }
    # 公式ドキュメントだとrevision_idだがコード上はrevisionIdのため修正
    data = {
        'pageId': pageId,
        'revisionId': revisionId,
        'body': body,
    }

    res = requests.put(api_endpoint, data=data, params=params)
    print(f'response_code: {res.status_code}')

    if res.status_code in [200, 201]:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)

