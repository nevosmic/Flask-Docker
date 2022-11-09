MACHINE=$1
IMAGE=$2
echo "Connect to $MACHINE server"

ssh ec2-user@$MACHINE "mkdir -p /home/ec2-user/final_proj;ls -la;"
ssh ec2-user@$MACHINE "mkdir -p /home/ec2-user/final_proj/app;ls -la;"
echo "Copy docker compose file to $MACHINE"
scp /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@$MACHINE:/home/ec2-user/final_proj/docker-compose.yml
scp /home/ec2-user/my_proj1/Flask-Docker.env ec2-user@$MACHINE:/home/ec2-user/final_proj/.env
ssh -v ec2-user@$MACHINE "cd /home/ec2-user/final_proj;ls -la;docker pull $IMAGE;docker-compose up -d --no-build;sleep 100;docker container ls -a;"
ssh -v ec2-user@$MACHINE "curl -Is 35.76.115.227:5000"
#clean up
ssh ec2-user@$MACHINE "cd /home/ec2-user/final_proj;docker-compose down;sleep 160;docker system prune --volumes;docker rmi $IMAGE;echo 'FINISH'"