# FROM debian:bullseye-slim

# RUN apt-get update && \
#     apt-get install -y dovecot-core dovecot-imapd && \
#     useradd -m testuser && echo 'testuser:testpass' | chpasswd && \
#     mkdir -p /var/mail/testuser/Maildir && \
#     chown -R testuser: /var/mail/testuser && \
#     apt-get clean

# COPY config/dovecot.conf /etc/dovecot/dovecot.conf

# CMD ["dovecot", "-F"]
FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dovecot-core dovecot-imapd dovecot-lmtpd && \
    groupadd -g 5000 vmail && \
    useradd -u 5000 -g vmail -m -d /var/mail/testuser vmail && \
    mkdir -p /var/mail/testuser/Maildir && \
    chown -R vmail:vmail /var/mail/testuser && \
    mkdir -p /var/log && touch /var/log/dovecot.log && chmod 666 /var/log && \
    apt-get clean

COPY config/dovecot.conf /etc/dovecot/dovecot.conf
COPY config/users /etc/dovecot/users
RUN chown vmail:vmail /etc/dovecot/users
COPY config/master-users /etc/dovecot/master-users
RUN chown vmail:vmail /etc/dovecot/master-users


CMD ["dovecot", "-F"]

