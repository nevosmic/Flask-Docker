INPUT=$1
echo "Connect to $1 server"
ssh ec2-user@test "mkdir -p /home/ec2-user/app;ls -la;"
echo "Copy docker compose file to test"
scp -v /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@test:/home/ec2-user/app/docker-compose.yml
scp -v /var/lib/jenkins/workspace/Bynet_attendance/.env ec2-user@test:/home/ec2-user/app/.env
ssh -v ec2-user@test "cd /home/ec2-user/app;ls -la;docker pull nevosmic/bynet_docker:v0.6; docker-compose up -d --no-build; sleep 160; docker container ls -a;"
#ssh ec2-user@test "curl -I 35.79.222.182:5000"
