uvicorn main:app --reload --host 127.0.0.1 --port 8001 --workers 1
rem hypercorn main:app --reload --bind 0.0.0.0:8090 
rem hypercorn main:app --bind 0.0.0.0:8090 -w 2

