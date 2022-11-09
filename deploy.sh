INPUT=$1
echo "Connect to $1 server"
ssh ec2-user@test "mkdir -p /home/ec2-user/final_proj;ls -la;"
ssh ec2-user@test "mkdir -p /home/ec2-user/final_proj/db;ls -la;"
echo "Copy docker compose file to test"
scp /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@test:/home/ec2-user/final_proj/docker-compose.yml
scp /var/lib/jenkins/workspace/Bynet_attendance/.env ec2-user@test:/home/ec2-user/final_proj/.env
scp -v /var/lib/jenkins/workspace/Bynet_attendance/db/init.sql ec2-user@test:/home/ec2-user/final_proj/db/init.sql
ssh -v ec2-user@test "cd /home/ec2-user/app;ls -la;docker-compose up -d --no-build; sleep 30; docker container ls -a;"
ssh ec2-user@test "ANS=$(curl -Is 127.0.0.1:5000);echo $ANS"
