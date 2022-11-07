#VARS
HOME_DIR="/home/ec2-user"
JEMKINS_WORKSPACE="/var/lib/jenkins/workspace/Bynet_attendance"
INPUT=$1
echo "Connect to $1 server"
echo "Creating project dir"
ssh ec2-user@test "hostname;mkdir -p /home/ec2-user/final;ls -la;"
echo "Copying docker-compose file to test"
scp /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@test:/home/ec2-user/final/docker-compose.yml
scp -v /var/lib/jenkins/workspace/Bynet_attendance/.env ec2-user@test:/home/ec2-user/final/.env
ssh ec2-user@test "cd /home/ec2-user/final;ls -la;"
ssh "ec2-user@test" "pwd;cd /home/ec2-user/final;pwd;docker-compose up -d;sleep 30;docker container ls; docker-compose down;"
echo "done"
