env=$1

[[ -z "$env" ]] && { echo "You must specify an environment (dev|stage|prod)" ; exit 1; }

aws ecs update-service --desired-count 1 --cluster realworld-$env --service webapp
