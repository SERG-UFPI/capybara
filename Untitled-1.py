from lib.get_metrics import retrieve_issues

if __name__ == "__main__":
    issues = retrieve_issues("gatsbyjs", "gatsby")
    print(issues)
    print(len(issues))