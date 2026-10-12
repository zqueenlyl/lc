#!/usr/bin/env bash
# 从 lc 仓库根目录起一个本机静态预览。只监听 127.0.0.1。
# 用法：./preview.sh [端口]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT="${1:-8931}"
HOST="127.0.0.1"

cd "$ROOT"

echo "目录  ${ROOT}"
echo "本体  http://${HOST}:${PORT}/ai/knowledge/ontology/表示与推理.html"
echo "门禁  http://${HOST}:${PORT}/ai/knowledge/lean/发货门禁-证明.html"
echo "停止  Ctrl-C"

exec python3 -m http.server "$PORT" --bind "$HOST"
