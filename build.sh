#!/usr/bin/env bash
source .venv/bin/activate
pip install -r requirements.txt
python3 -m PyInstaller --onefile --paths src --hidden-import="googleapiclient" main.py
tar -czvf dist/archive.tar.gz dist/main
