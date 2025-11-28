import pandas as pd

def FilterCommits(Scores: list, Commits: list, WhyImportant: list, top: int = 100):
    """Filters Top 100 Commits from Whole Score Integrity"""

    FilteredCommit=[]
    WhyImp=[]
    OutputScores=[]

    if len(Scores)!=len(Commits) and len(Commits)!=len(WhyImportant):
        print("Scores and Commits size are not Same")
        print("LenOf Scores:",len(Scores),"!= LenOf Commits:",len(Commits))
        return

    for _ in range(min(top,len(Commits))):
        maxid=0
        for j,num in enumerate(Scores):
            if num>Scores[maxid]:
                maxid=j

        OutputScores.append(Scores[maxid])
        FilteredCommit.append(Commits[maxid])
        WhyImp.append(WhyImportant[maxid])
        del Scores[maxid]
        del Commits[maxid]
        del WhyImportant[maxid]

    return FilteredCommit, WhyImp, OutputScores


def CreateDataFrame(Commits: list, WhyImp: list, OutputScores: list) -> pd.DataFrame:
    """Creates DataFrame of Filtered Commits"""
    rows = []

    for commit in Commits:
        temp=commit.stats.total
        commitMessage=commit.message.strip()
        row = [
            commit.committed_datetime.strftime("%Y-%m-%d"),
            commit.hexsha[:7]+'..',
            commit.author.name,
            temp.get('files', len(commit.stats.files)),
            temp['insertions'],
            temp['deletions'],
            commitMessage if len(commitMessage)<70 else commitMessage[:70]+'...',
        ]
        rows.append(row)
    
    df = pd.DataFrame(rows,columns=["Commit Date", "ID", "Contributor", "Files Changed", "Insertion Lines", "Deletion Lines", "Commit Message"])
    df['Why Important']=WhyImp
    df['Scored']=OutputScores
    return df.sort_values("Commit Date", ascending=True).reset_index(drop=True)