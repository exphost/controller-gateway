def prepare_common_headers(g):
    headers = {}
    if g.get('user', None):
        headers['X-User'] = g.user
    if g.get('user_full', None):
        headers['X-User-Full'] = g.user_full
    if g.get('token', None):
        headers['Authorization'] = "Bearer " + g.token
    if g.get('Authorization', None):
        headers['Authorization'] = g.get('Authorization')
    return headers
