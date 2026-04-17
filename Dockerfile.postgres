FROM postgres:17

RUN apt-get update && apt-get install -y \
    wget gnupg2 gpgv lsb-release curl && \
    wget https://repo.percona.com/apt/percona-release_latest.generic_all.deb && \
    dpkg -i percona-release_latest.generic_all.deb && \
    rm percona-release_latest.generic_all.deb && \
    percona-release setup ppg-17 && \
    apt-get update && \
    apt-get install -y percona-pg-stat-monitor17 && \
    rm -rf /var/lib/apt/lists/*


COPY ./setup.sql /docker-entrypoint-initdb.d/setup.sql
COPY ./postgresql.conf /etc/postgresql/postgresql.conf