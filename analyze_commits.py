from pydriller import Repository

repo_path = "./camel"
issue_ids = ["CAMEL-180", "CAMEL-321", "CAMEL-1818", "CAMEL-3214", "CAMEL-18065"]

unique_commits = {}

for commit in Repository(repo_path).traverse_commits():
    message = commit.msg.upper()

    for issue in issue_ids:
        if issue in message:
            unique_commits[commit.hash] = commit
            break

total_files_changed = 0

dmm_size = []
dmm_complexity = []
dmm_interface = []

for commit in unique_commits.values():
    total_files_changed += len(commit.modified_files)

    if commit.dmm_unit_size is not None:
        dmm_size.append(commit.dmm_unit_size)

    if commit.dmm_unit_complexity is not None:
        dmm_complexity.append(commit.dmm_unit_complexity)

    if commit.dmm_unit_interfacing is not None:
        dmm_interface.append(commit.dmm_unit_interfacing)

num_commits = len(unique_commits)

avg_files_changed = total_files_changed / num_commits if num_commits else 0

avg_dmm = 0
if dmm_size and dmm_complexity and dmm_interface:
    avg_dmm = (
        (sum(dmm_size) / len(dmm_size)) +
        (sum(dmm_complexity) / len(dmm_complexity)) +
        (sum(dmm_interface) / len(dmm_interface))
    ) / 3

print("Total commits analyzed:", num_commits)
print("Average number of files changed:", avg_files_changed)
print("Average DMM metrics:", avg_dmm)
