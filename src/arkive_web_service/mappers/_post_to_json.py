from arkive_db.models import Post
from typing import Dict


def post_to_json(post: Post) -> Dict:
    return {
        "id": str(post.id),
        "description": post.description,
        "url": post.url,
        "banner": post.banner,
        "timestamp": str(post.timestamp),
    }
