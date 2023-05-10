FROM python:slim

RUN apt update && \
	apt install openssh-server apache2 wget git -y && \
	echo "PermitRootLogin yes" >>  /etc/ssh/sshd_config
	
RUN echo "root:123" > user.txt && chpasswd < user.txt
	

EXPOSE 22

RUN pip3 install webssh supervisor && \
	cp -r /usr/local/lib/python3.11/site-packages/supervisor/ui/* /var/www/html/
	
ADD docker-work /etc/apache2/sites-available/

RUN a2enmod proxy && a2enmod proxy_http && service apache2 restart 

RUN chmod +x /etc/apache2/sites-available/startssh.sh
	
RUN systemctl disable apache2

CMD ["supervisord","-nc","/etc/apache2/sites-available/supervisor-wssh.conf"]

