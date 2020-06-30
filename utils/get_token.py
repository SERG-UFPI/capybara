from github import Github
import os

def get_token():
    tokens = []
    index = 1
    while 1:
        token = os.environ.get(f"TOKEN_{index}")
        if token != None:
            tokens.append(token)
            index += 1
        else:
            break
    token_with_greatest_rate_limiting = None
    greatest_rate_limiting = -1
    for token in tokens:
        g_temp = Github(token)
        try:
            rate_limiting = g_temp.rate_limiting[0]
            if rate_limiting != None and rate_limiting > greatest_rate_limiting:
                greatest_rate_limiting = rate_limiting
                token_with_greatest_rate_limiting = token
        except Exception as identifier:
            continue

    return token_with_greatest_rate_limiting