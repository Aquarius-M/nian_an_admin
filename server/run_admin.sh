#!/usr/bin/env bash

# 运行服务
python -m uvicorn asgi:app --host 0.0.0.0 --port 9527 --reload
