env=$1
nodes=$2

[[ -z "$env" ]] && { echo "You must specify an environment (dev|stage|prod)" ; exit 1; }

if [ ! "$nodes" ]; then
  echo You must specify the number of nodes.
  exit
fi

aws ecs update-service --desired-count $nodes --cluster realworld-$env --service webapp
