NAMESPACE="fraud-monitor"

oc new-project $NAMESPACE

sed -e "s|NAMESPACE|$NAMESPACE|g" ./kubefiles/grafana-deployment.yaml | oc apply -n $NAMESPACE -f -
