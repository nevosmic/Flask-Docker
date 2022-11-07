# VARS
HOME_DIR="/home/ec2-user"
JEMKINS_WORKSPACE="/var/lib/jenkins/workspace/Bynet_attendance"
INPUT=$1
echo "Connect to $1 server"
echo "Creating project dir"
ssh ec2-user@test "hostname;mkdir -p /home/ec2-user/final;ls -la;"