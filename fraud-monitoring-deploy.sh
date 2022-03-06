NAMESPACE="fraud-monitor"

oc new-project $NAMESPACE

sed -e "s|NAMESPACE|$NAMESPACE|g" ./kubefiles/grafana-deployment.yaml | oc apply -n $NAMESPACE -f -

oc adm policy add-cluster-role-to-user cluster-monitoring-view -z grafana-serviceaccount -n $NAMESPACE

TOKEN=$(oc serviceaccounts get-token grafana-serviceaccount -n $NAMESPACE)

sed -e "s|TOKEN|$TOKEN|g" ./kubefiles/grafana-datasource.yaml | oc apply -n $NAMESPACE -f -

oc apply -n $NAMESPACE -f ./kubefiles/fraud-detection-dashboard.yaml

ADMIN_USER=$(oc get secret grafana-admin-credentials -n $NAMESPACE --template={{.data.GF_SECURITY_ADMIN_USER}} | base64 -d)
ADMIN_PASSWORD=$(oc get secret grafana-admin-credentials -n $NAMESPACE --template={{.data.GF_SECURITY_ADMIN_PASSWORD}} | base64 -d)

GRAFANA_URL="https://"$(oc get route grafana-route -n $NAMESPACE -o jsonpath='{.spec.host}')

echo "\n\nGrafana has been successfully deployed, you can use the following url to access\n\n"    $GRAFANA_URL  "\n\n. Admin user : "$ADMIN_USER "\n. Password : "$ADMIN_PASSWORD"\n\n"