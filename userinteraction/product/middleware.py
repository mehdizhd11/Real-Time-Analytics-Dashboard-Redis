import time
import datetime
from django.utils.deprecation import MiddlewareMixin
import redis
from redis.cluster import ClusterNode
from redis.exceptions import RedisError


class ProductMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self.redis_conn = redis.cluster.RedisCluster(
            startup_nodes=[
                ClusterNode('127.0.0.1', 7000),
                ClusterNode('127.0.0.1', 7001),
                ClusterNode('127.0.0.1', 7002),
                ClusterNode('127.0.0.1', 7003),
                ClusterNode('127.0.0.1', 7004),
                ClusterNode('127.0.0.1', 7005),
            ],
            decode_responses=True
        )


    def process_view(self, request, view_func, view_args, view_kwargs):
        request.start_time = time.time()
        if 'id' in view_kwargs:
            request.product_id = view_kwargs['id']
        return None


    def process_response(self, request, response):
        if hasattr(request, 'start_time') and hasattr(request, 'product_id'):
            try:
                elapsed_time = int((time.time() - request.start_time) * 1000)
                product_id = request.product_id

                # user_id = str(request.user.id)
                user_id = 'user'

                # Track product views
                self.redis_conn.hincrby(f"product:{product_id}:views", user_id, 1)

                # Track time spent on the product page
                self.redis_conn.hincrby(f"product:{product_id}:time_spent", user_id, elapsed_time)

                # Track view times
                view_time = datetime.datetime.now().isoformat()
                self.redis_conn.rpush(f"product:{product_id}:view_times:{user_id}", view_time)
            except RedisError as e:
                print(f"Redis error: {e}")

        return response
