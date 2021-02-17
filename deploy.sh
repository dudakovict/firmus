#!/bin/bash


echo "Creating the volume..."

kubectl apply -f ./kubernetes/postgres/postgres-persistent-volume.yaml
kubectl apply -f ./kubernetes/postgres/postgres-persistent-volume-claim.yaml


echo "Creating the database credentials..."

kubectl apply -f ./kubernetes/postgres/postgres-secret.yaml


echo "Creating the postgres deployment and service..."

kubectl create -f ./kubernetes/postgres/postgres-deployment.yaml
kubectl create -f ./kubernetes/postgres/postgres-service.yaml


echo "Creating twilio credentials..."

kubectl apply -f ./kubernetes/auth/twilio-secret.yaml

echo "Creating the flask deployment and service..."

kubectl create -f ./kubernetes/auth/auth-deployment.yaml
kubectl create -f ./kubernetes/auth/auth-service.yaml


echo "Adding the ingress..."

kubectl apply -f ./kubernetes/ingress/ingress-service.yaml