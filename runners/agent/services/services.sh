export TASK=c2c ; export SERVICE_PORT=8761
gunicorn --workers=1 service:app -b 0.0.0.0:${SERVICE_PORT} --reload --timeout 120 &
export TASK=htr ; export SERVICE_PORT=8762
gunicorn --workers=1 service:app -b 0.0.0.0:${SERVICE_PORT} --reload --timeout 120 &
export TASK=vqa ; export SERVICE_PORT=8763
gunicorn --workers=1 service:app -b 0.0.0.0:${SERVICE_PORT} --reload --timeout 120 &
export TASK=zsod ; export SERVICE_PORT=8764
gunicorn --workers=1 service:app -b 0.0.0.0:${SERVICE_PORT} --reload --timeout 120 &