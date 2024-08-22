
---

# Product Interaction Tracker

This project is a Django-based application designed to track and analyze user interactions with products. It utilizes a Redis Cluster to store interaction data such as view durations, view timestamps, and other relevant metrics. The project is built using Django, Django REST Framework (DRF), and custom middleware to efficiently track and manage data.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Redis Cluster Configuration](#redis-cluster-configuration)
- [Middleware Details](#middleware-details)
- [API Endpoints](#api-endpoints)


## Project Overview

The Product Interaction Tracker is designed to monitor and log user interactions with products on a website. It captures data such as:

- **View Duration**: How long a user spends viewing a product.
- **View Timestamps**: The exact time a user views a product.
- **Interaction Frequency**: How often a user views a product.

This data is stored in a Redis Cluster, enabling fast access and real-time analytics. The application uses Django middleware to capture this data automatically during user interactions.

## Features

- **Automatic Interaction Tracking**: Tracks user interactions with products using Django middleware.
- **View Duration Logging**: Captures the time users spend on each product page.
- **Redis Cluster Storage**: Utilizes a Redis Cluster to store and manage interaction data efficiently.
- **RESTful API**: Built with Django REST Framework to provide API endpoints for product interactions.

## Technologies Used

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework (DRF)**: A powerful and flexible toolkit for building Web APIs in Django.
- **Redis**: An in-memory data structure store, used as a database, cache, and message broker.
- **Redis Cluster**: A distributed implementation of Redis that provides automatic sharding and fault tolerance.

## System Requirements

- **Python 3.8+**
- **Django 3.2+**
- **Redis Cluster (with multiple nodes)**
- **pip (Python package installer)**

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mehdizhd11/https://github.com/mehdizhd11/Real-Time-Analytics-Dashboard-Redis.git
   cd Real-Time-Analytics-Dashboard-Redis
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the Django project:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. **Configure Redis Cluster:**

   Ensure your Redis Cluster is up and running. The configuration for Redis Cluster nodes should be set in your Django settings file (explained below).

## Configuration

### Django Settings

In your Django `settings.py`, configure the following:

```python
# Redis Cluster settings
REDIS_NODES = [
    {'host': 'redis-node1', 'port': 7000},
    {'host': 'redis-node2', 'port': 7001},
    {'host': 'redis-node2', 'port': 7002},
    {'host': 'redis-node2', 'port': 7003},
    {'host': 'redis-node2', 'port': 7004},
    {'host': 'redis-node3', 'port': 7005},
]
```

### Middleware Configuration

Add the custom middleware to track product interactions in your `MIDDLEWARE` setting:

```python
MIDDLEWARE = [
    # Other middleware classes
    'product.middleware.ProductMiddleware',  # Add your custom middleware here
]
```

## Usage

After setting up the project and running the server, the middleware will automatically track user interactions with products. The interaction data is stored in the Redis Cluster, and you can access and analyze it as needed.

### Running the Server

Start the Django development server with:

```bash
python manage.py runserver
```

## Redis Cluster Configuration

The Redis Cluster should be configured with multiple nodes to ensure data is distributed and fault-tolerant. Make sure Redis is properly set up and configured according to the Redis Cluster documentation.

### Example Configuration

```python
REDIS_NODES = [
    {'host': 'redis-node1', 'port': 7000},
    {'host': 'redis-node2', 'port': 7001},
    {'host': 'redis-node2', 'port': 7002},
    {'host': 'redis-node2', 'port': 7003},
    {'host': 'redis-node2', 'port': 7004},
    {'host': 'redis-node3', 'port': 7005},
]
```

## Middleware Details

### ProductMiddleware

This custom middleware captures the following data:

- **Start Time**: When a user starts viewing a product.
- **View Duration**: The total time spent viewing the product.
- **User Identification**: The middleware captures the user ID for authenticated users or an anonymous identifier.

#### Example Code

```python
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
```

## API Endpoints

This project uses Django REST Framework to expose various API endpoints. Below are some of the key endpoints:

- **POST /products/**: Create a new product.
- **GET /products/{id}/**: Retrieve details of a specific product.

You can extend the API by adding more views and serializers as required.

---