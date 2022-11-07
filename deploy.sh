# VARS
HOME_DIR="/home/ec2-user"
JEMKINS_WORKSPACE="/var/lib/jenkins/workspace/Bynet_attendance"
input=$1
echo "$input"
mechine=test
echo "Connect to ${mechine} server"
echo "Creating project dir"
ssh "ec2-user@$test" "mkdir -p /home/ec2-user/final-proj"
echo "Copying docker-compose file to test"
scp "/var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml" "ec2-user@${mechine}:/home/ec2-user/final-proj"
echo "Starting project"
ssh "ec2-user@test" "pwd;cd /home/ec2-user/final-proj;pwd;docker-compose up -d;sleep 30;docker container ls; docker-compose down"
echo "END UP"
