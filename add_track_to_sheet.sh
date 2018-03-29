set -x

ssh -o StrictHostKeyChecking=no -i arun_server.pem ubuntu@ec2-54-218-75-68.us-west-2.compute.amazonaws.com "

    cd
    python call_client.py

"