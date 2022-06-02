env=$1
ecr_url="806683838495.dkr.ecr.us-east-1.amazonaws.com"
image_name=realworld-$env-nginx
aws_region=us-east-1

[[ -z "$env" ]] && { echo "You must specify an environment (dev|stage|prod)" ; exit 1; }

aws ecr get-login-password --region $aws_region | \
  sudo docker login --username AWS --password-stdin $ecr_url

sudo docker build --tag "${image_name}" .
sudo docker tag "${image_name}:latest" "${ecr_url}/${image_name}:latest"

sudo docker push "${ecr_url}/${image_name}:latest"
