# gca
~~git checkout all branches one shell cmd~~

I'm stupid. There's easier way to do this:

* http://stackoverflow.com/questions/3382679/git-how-do-i-update-my-bare-repo
* http://stackoverflow.com/questions/2756747/mirror-a-git-repository-by-pulling/2756894#2756894

shell:

```

git clone --mirror git@somewhere.com:repo.git
cd repo.git
git config remote.origin.fetch 'refs/heads/*:refs/heads/*'
echo "*/10 * * * * cd "$(pwd)" && git fetch -q --tags">crontabjob.txt
crontab crontabjob.txt

```



