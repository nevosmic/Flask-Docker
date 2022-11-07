# VARS
HOME_DIR="/home/ec2-user"
JEMKINS_WORKSPACE="/var/lib/jenkins/workspace/Bynet_attendance"
INPUT=$1
echo "${input}"
MECHINE="test"
echo "Connect to $1 server"
echo "Creating project dir"
ssh ec2-user@test "hostname;mkdir /home/ec2-user/app;ls -la;"
echo "Copying docker-compose file to test"
ssh ec2-user@test "cd /home/ec2-user/app;pwd;"
scp /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@test:/home/ec2-user/app
scp /var/lib/jenkins/workspace/Bynet_attendance/.env ec2-user@test:/home/ec2-user/app
echo "Starting project"
ssh ec2-user@test "pwd;cd /home/ec2-user/app;ls;pwd;docker-compose up -d;sleep 30;docker container ls; docker-compose down;"
echo "END UP"
