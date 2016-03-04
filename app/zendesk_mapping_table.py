"""
CUSTOM API MAPPING FOR Zendesk API V2
"""

mapping_table = {
    # Forums
    'list_all_posts': {
        'path': '/community/posts.json',
        'method': 'GET',
        'valid_params': ['filter_by', 'sort_by']
    }
}

# Patch mapping table with correct HTTP Status expected
for method, api_map in mapping_table.iteritems():
    status = 200
    if method.startswith('create_'):
        status = 201
    api_map['status'] = status
