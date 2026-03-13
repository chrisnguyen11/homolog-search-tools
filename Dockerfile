FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

# Setup ssh.
RUN mkdir -p -m 0600 ~/.ssh \
    && ssh-keyscan -H github.com >> ~/.ssh/known_hosts

# Install python-based dependencies.
RUN --mount=type=ssh,id=github_ssh_key pip install --no-cache-dir -r requirements.txt

# # Install third-party dependencies.
RUN cd / \
    && wget https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz \
    && tar xfz mmseqs-linux-avx2.tar.gz \
    && rm mmseqs-linux-avx2.tar.gz \
    && ln -s /mmseqs/bin/mmseqs /usr/bin \
    && cd 

RUN cd / \
    && wget http://github.com/bbuchfink/diamond/releases/download/v2.1.11/diamond-linux64.tar.gz \
    && tar xfz diamond-linux64.tar.gz \
    && rm diamond-linux64.tar.gz \
    && cd 

RUN apt-get update \
    && apt-get -y install clustalo \
    && apt-get -y install ncbi-blast+

# Launch notebook
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8899", "--no-browser", "--allow-root"]