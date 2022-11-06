echo "Connect to test server"
echo "Creating project dir"
SSH_KEY=/var/lib/jenkins/.ssh/id_dsa
JENKINS_WORKSPACE=/var/lib/jenkins/workspace/git and docker connection
ssh -i "/home/ec2-user/.ssh/id_dsa" -o StrictHostKeyChecking=no test "mkdir -p /home/ec2-user/final-proj"
scp $JENKINS_WORKSPACE/docker-compose.yml ec2-user@test:/home/ec2-user/final-proj/docker-compose.yml
scp $JENKINS_WORKSPACE/.env ec2-user@test:/home/ec2-user/final-proj/.env
ssh -i "/home/ec2-user/.ssh/id_dsa" -o StrictHostKeyChecking=no test "ls -a"
ssh -i "/home/ec2-user/.ssh/id_dsa" -o StrictHostKeyChecking=no test "cd /home/ec2-user/final-proj;docker-compose up --no-build -d;sleep 20;docker container ls; docker-compose down"
