#!/bin/bash
# make file executable by running this command in the terminal: chmod + x clone.sh
# clone at current directory and cd into cloned project -> clone git@github.com:reshinto/myrepo.git
# clone at target directory and cd into cloned project -> clone git@github.com:reshinto/myrepo.git ./some/path

mkdir -p $2
cd $2

function lazyclone() {
    gitURL=$1;
    reponame="$(echo $gitURL | awk -F/ '{print $NF}' | sed -e 's/.git$//')";
    git clone $gitURL $reponame;
    cd $reponame;
    #open .;
}

lazyclone "$1"
