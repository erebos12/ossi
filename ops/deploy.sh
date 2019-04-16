#!/usr/bin/env bash
K8S_DIR=./manifests

#clean old generated files
rm -r ${K8S_DIR}/.generated

TARGET_DIR=${K8S_DIR}/.generated
mkdir -p ${TARGET_DIR}

[[ "$MINIKUBE_DEPLOYMENT" = true ]] && echo 'Starting Minikube deployment' || echo 'Starting K8s deployment'

#Populate the yaml files with environment vars from Gitlab and config defined under variables
for f in ${K8S_DIR}/*.yaml
do  
  if [ "$MINIKUBE_DEPLOYMENT" = true ]; then
    #Skip k8s files for minikube deployment 
    [[ $f == *k8s.yaml ]] && echo 'Skipping k8s files ' $f && continue
  else
    #Skip minikube files for regular deployment
    [[ $f == *minikube.yaml ]] && echo 'Skipping minikube files ' $f && continue
  fi
  jinja2 $f ./variables/${CI_ENVIRONMENT_SLUG}.yaml --format=yaml --strict -D REPLICAS=${REPLICAS} -D CI_PROJECT_NAME=${CI_PROJECT_NAME} -D CI_PROJECT_NAMESPACE=${CI_PROJECT_NAMESPACE} -D DOCKER_IMAGE_TAG=${CI_COMMIT_SHA} -D CI_ENVIRONMENT_SLUG=${CI_ENVIRONMENT_SLUG} -D TRACK=${TRACK} -D MY_SECRET_GIT_VARIABLE="${MY_SECRET_GIT_VARIABLE}" > "${TARGET_DIR}/$(basename ${f})"
done

#Kubernetes deployment
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} apply -f ${TARGET_DIR}/10-ns.yaml
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} delete configmap ${CI_PROJECT_NAME}-app-config || true
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} delete secret ${CI_PROJECT_NAME}-app-secrets || true
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} delete secret ecregistry
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} create secret docker-registry ecregistry --docker-server=ecregistry.azurecr.io --docker-username=ecregistry --docker-password=${DOCKER_REGISTRY_PASSWORD} --docker-email=foo.bar@pwc.com
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} apply -f ${TARGET_DIR}

#Status and logs
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} get ingress ${CI_PROJECT_NAME}
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} get services ${CI_PROJECT_NAME}
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} describe pods ${CI_PROJECT_NAME}-stable
