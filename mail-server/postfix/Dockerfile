FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y postfix dovecot-core mailutils && \
    apt-get clean

COPY ./config/main.cf /etc/postfix/main.cf
COPY ./config/vmailbox /etc/postfix/vmailbox

RUN useradd -m testuser && echo 'testuser:testpass' | chpasswd && \
    mkdir -p /var/mail/testuser/Maildir && \
    chown -R testuser:testuser /var/mail/testuser && \
    mkdir -p /var/log && touch /var/log/mail.log && chmod 666 /var/log/mail.log

CMD service postfix start && tail -f /dev/null