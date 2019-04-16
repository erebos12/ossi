#!/usr/bin/env bash

K8S_DIR=./manifests

#clean old generated files
if [ -f ${K8S_DIR}/.generated ]; then
   rm -r ${K8S_DIR}/.generated
fi

TARGET_DIR=${K8S_DIR}/.generated
mkdir -p ${TARGET_DIR}
for f in ${K8S_DIR}/*.yaml
do
  jinja2 $f ./variables/${CI_ENVIRONMENT_SLUG}.yaml --format=yaml --strict -D REPLICAS=${REPLICAS} -D CI_PROJECT_NAME=${CI_PROJECT_NAME} -D CI_PROJECT_NAMESPACE=${CI_PROJECT_NAMESPACE} -D DOCKER_IMAGE_TAG=${CI_BUILD_REF} -D CI_ENVIRONMENT_SLUG=${CI_ENVIRONMENT_SLUG} -D TRACK=${TRACK} > "${TARGET_DIR}/$(basename ${f})"
done

# generate nginx config
jinja2 ./conf/nginx.conf.tmpl ./variables/${CI_ENVIRONMENT_SLUG}.yaml --format=yaml --strict > ./conf/nginx.conf

kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} apply -f ${TARGET_DIR}/10-ns.yaml
# add SECRET here
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} delete configmap nginx-conf-backend || true
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} create configmap nginx-conf-backend --from-file=conf/nginx.conf
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} delete secret ecregistry
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} create secret docker-registry ecregistry --docker-server=ecregistry.azurecr.io --docker-username=ecregistry --docker-password=${DOCKER_REGISTRY_PASSWORD} --docker-email=foo.bar@pwc.com

# Deploy
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} apply -f ${TARGET_DIR}

# show status
echo "****** INGRESS ******"
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} get ingress ${CI_PROJECT_NAME}
echo "****** SERVICE ******"
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} get services ${CI_PROJECT_NAME}
echo "****** DEPLOYMENTS ******"
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} describe deployments
echo "****** PODS ******"
kubectl --namespace=${CI_PROJECT_NAMESPACE}-${CI_ENVIRONMENT_SLUG} describe pods

