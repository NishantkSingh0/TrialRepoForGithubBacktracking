import shutil
import os
import stat
from git import Repo
from git.exc import GitCommandError

def remove_readonly(func, path, _):
    """Force delete read-only files on Windows"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def Pull(url: str):
    """Cloning Repo if not already cloned"""
    
    print('Pulling:',url)
    if url[-4:]!='.git':
        url=url+'.git'

    # Check if Repository is already cloned
    StoredRepoUrl=''
    Message=''
    try:
        with open("SampleMemoryWorks/repositoryInfo.txt", "r") as f:
            StoredRepoUrl = f.read()
    except FileNotFoundError:
        with open("SampleMemoryWorks/repositoryInfo.txt", "w") as f:
            f.write(url)

    # Clone only if RepoUrl are new else read previously cloned one..
    if StoredRepoUrl!=url:
        with open("SampleMemoryWorks/repositoryInfo.txt", "w") as f:
            f.write(url)

        try:
            repo = Repo.clone_from(url, "SampleMemoryWorks/FetchedData/")
        except GitCommandError:
            if os.path.exists("SampleMemoryWorks/FetchedData/"):
                shutil.rmtree("SampleMemoryWorks/FetchedData/", onerror=remove_readonly)
            repo = Repo.clone_from(url, "SampleMemoryWorks/FetchedData/")
    else:
        repo=Repo('SampleMemoryWorks/FetchedData/')
        Message="Already Pulled in local"
    return repo, Message 