# VARS
HOME_DIR="/home/ec2-user"
JEMKINS_WORKSPACE="/var/lib/jenkins/workspace/Bynet_attendance"
input=$1
echo "${input}"
MECHINE="test"
echo "Connect to ${MECHINE} server"
echo "Creating project dir"
ssh ec2-user@$test "mkdir -p /home/ec2-user/final-proj"
echo "Copying docker-compose file to test"
scp /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@$test:/home/ec2-user/final-proj/docker-compose.yml
scp "/var/lib/jenkins/workspace/Bynet_attendance/.env" "ec2-user@test:/home/ec2-user/final-proj/.env"
echo "Starting project"
ssh "ec2-user@test" "pwd;cd /home/ec2-user/final-proj;pwd;docker-compose up -d;sleep 30;docker container ls; docker-compose down"
echo "END UP"
