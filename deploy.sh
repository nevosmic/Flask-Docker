# VARS
HOME_DIR="/home/ec2-user"
JEMKINS_WORKSPACE="/var/lib/jenkins/workspace/Bynet_attendance"
INPUT=$1
echo "Connect to $1 server"
echo "Creating project dir"
ssh ec2-user@test "hostname;mkdir -p /home/ec2-user/final;ls -la;"
echo "Copying docker-compose file to test"
scp -v /var/lib/jenkins/workspace/Bynet_attendance/docker-compose.yml ec2-user@test:/home/ec2-user/final
ssh ec2-user@test "cd /home/ec2-user/final;ls -la;"