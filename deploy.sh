# VARS
HOME_DIR="/home/ec2-user"
JEMKINS_WORKSPACE="/var/lib/jenkins/workspace/Bynet_attendance"
mechine=$1

echo "Connect to $mechine server"
echo "Creating project dir"
ssh "ec2-user@${mechine}" "mkdir -p ${HOME_DIR}/final-proj"
echo "Copying docker-compose file to $mechine"
scp "${JEMKINS_WORKSPACE}/docker-compose.yml" "ec2-user@${mechine}:${HOME_DIR}/final-proj"
echo "Starting project"
ssh "ec2-user@${mechine}" "pwd;cd ${HOME_DIR}/final-proj;pwd;docker-compose up -d;sleep 30;docker container ls; docker-compose down"
echo "END UP"
