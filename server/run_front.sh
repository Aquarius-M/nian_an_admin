#!/usr/bin/env bash

# 运行服务
python -m uvicorn asgi_front:app --host 0.0.0.0 --port 1024 --reload
