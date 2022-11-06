echo "Connect to test server"
echo "Creating project dir"
SSH_TEST_KEY=/var/lib/jenkins/.ssh/test_key
JENKINS_WORKSPACE=/var/lib/jenkins/workspace/git and docker connection
ssh -i $SSH_TEST_KEY -o StrictHostKeyChecking=no test "mkdir -p /home/ec2-user/final-proj"
scp $JENKINS_WORKSPACE/docker-compose.yml ec2-user@test:/home/ec2-user/final-proj/docker-compose.yml
scp $JENKINS_WORKSPACE/.env ec2-user@test:/home/ec2-user/final-proj/.env
ssh -i $SSH_TEST_KEY -o StrictHostKeyChecking=no test "ls -a"
ssh -i $SSH_TEST_KEY -o StrictHostKeyChecking=no test "cd /home/ec2-user/final-proj;docker-compose up --no-build -d;sleep 20;docker container ls; docker-compose down"
