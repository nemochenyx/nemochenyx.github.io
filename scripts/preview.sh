#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if [ -x .local/tools/hugo ]; then
  HUGO_BIN=.local/tools/hugo
elif command -v hugo >/dev/null 2>&1; then
  HUGO_BIN=hugo
else
  echo '尚未安装 Hugo。请参阅 docs/使用说明.md，或在 GitHub 网页中直接修改内容。'
  exit 1
fi
echo '本地预览：http://localhost:1313/；修改 content 中的文件并保存，预览会自动更新。'
exec "$HUGO_BIN" server --bind 127.0.0.1 --port 1313 --baseURL http://localhost:1313/ --disableFastRender

