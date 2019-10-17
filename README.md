# Cloud_Integrated_Metric_Dashboards-CIMD-
The cloud integrated metric dashboards will help close any gaps in visibility of the metrics for customers

# Requirements
Install the required modules running 'pip install -r stable-req.text'

# Get Started
Proivde the tenant/environment url, api-token and username params in the auth_param_example.yaml file found in etc/. Rename the file to auth_param.yaml.

# Executing
pyhton importdash.py --idash {cloud_technology} - aws/azure/k8s/cf/vmware

NOTE: May take some time to publish the dashboards to your environment
