FROM --platform=linux/amd64 python:3.10

RUN apt-get update && apt-get install -y sudo git neovim vim zsh

COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

ADD https://api.github.com/repos/eycjur/dotfiles/git/refs/heads/main version.json
RUN git clone https://github.com/eycjur/dotfiles.git ~/dotfiles
RUN cp ~/dotfiles/.gitconfig.local.sample ~/dotfiles/.gitconfig.local
RUN ~/dotfiles/install.sh

CMD ["/bin/zsh"]
