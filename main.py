import streamlit as st
import git_fetcher as gitf
import utils as ut

# Building sample Streamlit Layout for taking Github URL
if "url" not in st.session_state:
    st.session_state.url=""

st.set_page_config(layout="wide")  
st.session_state.url = st.text_input("Git URL", "")

run_analysis = st.button("🚀 Analyze")

if run_analysis:
    if st.session_state.url.strip()[:19] != "https://github.com/":
        st.error("⚠️ Please enter a valid GitHub URL")
    else:
        with st.status("Pulling repository...") as status:
            repo,Message=gitf.Pull(st.session_state.url)
            if Message:
                st.write(Message)
            status.update(label="Repository pulled", state="complete")
        
        with st.status("Processing Scores...", expanded=True) as status:
            placeholder = st.empty()
            scores = []
            WhyImportant = []

            # Detect Core branch
            try:
                branch_name = repo.active_branch.name
            except TypeError:
                branch_name = repo.head.ref.name

            # Cache tagged commits for O(1) lookup
            tagged_commits = {tag.commit.hexsha for tag in repo.tags}

            # Predefine keywords and their respective scores
            keywords = ["fix", "security", "feature", "implement", "perf", "refactor", "release", "revert"]
            keywordScores={"fix": 3, "security": 4, "feature": 2, "implement": 1, "perf": 3, "refactor": 1, "release": 3, "revert": 1}

            Commits = list(repo.iter_commits(branch_name))
            lenCommits=len(Commits)

            for i, commit in enumerate(Commits):
                score = 0
                why_imp_parts = "Have "
                temp=0
                stats = commit.stats.total  # compute once
                message_lower = commit.message.lower()

                # Analyze number of Lines changed
                temp=stats["lines"]
                score += temp*0.01
                if temp>100:
                    why_imp_parts+=f"{temp} line updates, "

                # Analyze number of files changed
                temp = stats.get("files", len(commit.stats.files))
                score += temp*0.6
                if temp>5:
                    why_imp_parts+=f"{temp} file updates, "

                # Find Matching tags
                if commit.hexsha in tagged_commits:
                    score += 10
                    why_imp_parts+=f"Matching tag, "

                # Search for Important keywords in commits
                temp=""
                for kw in keywords:
                    if kw in message_lower:
                        score += keywordScores[kw]
                        temp+=kw+", "
                if temp:
                    why_imp_parts+=f"Matched Keywords [{temp}]"

                # Collect results
                scores.append(score)
                WhyImportant.append(why_imp_parts if why_imp_parts!="Have " else "Nothing special to showcase")

                # Update UI for realtime evaluation
                placeholder.write(f"Processing commit {i+1}/{lenCommits}")
            
            # Filter Top 100 Commits based on analyzed scores
            Commits, WhyImp, OutputScores = ut.FilterCommits(scores, Commits, WhyImportant)
            
            # --------------------------------------------------------------
            # Commits, WhyImp, OutputScores = ut.ScoreAndFilterCommits(repo)
            # --------------------------------------------------------------

            status.update(label="Scores Processed", state="complete",expanded=False)


        with st.status("Creating DataFrame...") as status:
            df=ut.CreateDataFrame(Commits=Commits, WhyImp=WhyImp, OutputScores=OutputScores)
            status.update(label="DataFrame Created", state="complete")

        st.markdown("---") 

        # Top 100 analyzed Commits
        with st.expander("Commits History", expanded=False):
            st.dataframe(
                df[["Commit Date", "ID", "Contributor", "Files Changed", "Why Important", "Scored", "Commit Message"]],
                use_container_width=True
            )

        # group based on batch of 10
        grouped_df = df.groupby(df.index // 10).agg({
            "Commit Date": "first", 
            "ID": list,
            "Contributor": "first",
            "Files Changed": list,
            "Why Important": list,
            "Scored": list,
            "Commit Message": lambda x: ",\n\n".join(x) 
        }).sort_values("Commit Date", ascending=True).reset_index(drop=True)

        # Show grouped data
        with st.expander("Top 10 Commits with neighbour information", expanded=False):
            st.dataframe(grouped_df[["Commit Date","Contributor","Commit Message"]], use_container_width=True)
        
        CommitMessage = grouped_df['Commit Message'].tolist()
        Prompt = ""
        for i,comms in enumerate(CommitMessage):
            Prompt+=f"Step{i+1}: "+comms+"\n---\n"

        st.markdown("---") 
        st.subheader("Series wise Repository Explanations")
        with st.status("Generating Commit Explanations...") as status:
            response=llm.respond(prompt=Prompt)
            status.update(label="Commit explanation Generated", state="complete")
        sections = response.split("\n---\n")
        
        for section in sections:
            with st.container(border=True):
                st.markdown(section)
