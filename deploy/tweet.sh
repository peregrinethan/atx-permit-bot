sudo docker run --name tweets -d --rm -v /home/ec2-user/atx-permit-bot:/app -w /app atx-permit-bot python tweet.py