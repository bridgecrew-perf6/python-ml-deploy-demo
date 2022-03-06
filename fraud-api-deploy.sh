NAMESPACE=fraud-detector-model

oc new-project $NAMESPACE

oc new-app https://github.com/troy-adianto/python-ml-deploy-demo.git -n $NAMESPACE \
--context-dir=model-deploy \
--strategy=source \
--name=fraud-detector-api

oc expose service fraud-detector-api -n $NAMESPACE

ROUTE_URL="http://"$(oc get route fraud-detector-api -n $NAMESPACE -o jsonpath='{.spec.host}')

oc apply -f ./kubefiles/fraud-detector-service-monitor.yaml -n $NAMESPACE

echo "\n\nFraud detector api succesfully deployed please use the following link to test after the build is completed\n\n"   $ROUTE_URL"\n\n"

echo "use 'predict' endpoint to get detection result"