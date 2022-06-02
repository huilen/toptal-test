env=$1

[[ -z "$1" ]] && { echo "You must specify an environment (dev|stage|prod)" ; exit 1; }

terraform workspace select $env || exit 1
terraform apply -var-file=config/$env.tfvars
