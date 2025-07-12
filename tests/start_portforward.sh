#!/bin/bash

nohup kubectl port-forward --address=0.0.0.0 svc/react-service 8000:80 &
nohup kubectl port-forward --address=0.0.0.0 svc/flask-service 8001:80 &
nohup kubectl port-forward --address=0.0.0.0 svc/inventory-chart-grafana 8010:80 &
