sudo docker run --name scrape-backward -d --rm -v /home/ec2-user/atx-permit-bot:/app -w /app atx-permit-bot python scrape.py -d backward -n 500