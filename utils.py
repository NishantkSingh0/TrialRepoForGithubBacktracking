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