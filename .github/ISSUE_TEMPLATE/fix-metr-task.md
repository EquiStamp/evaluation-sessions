---
name: Fix METR Task
about: Use this issue template to fix a METR task.
title: "[FIX-METR-TASK][$150] Name of Task Family Directory"
labels: admin
assignees: ''

---

### Task Errors

**What needs to be done?**
Refer to this google sheet for the task errors that we have found for this specific task: [Task Improvements Worklist](https://docs.google.com/spreadsheets/d/1d1M7ozvJeapPMpPXmdwnJc_dIFrgHVRjA1MgosX4brA/edit?userstoinvite=sami%40metr.org&sharingaction=manageaccess&role=writer&gid=323653529#gid=323653529).

**Please track your time working on this down to the minute**

### Business Driver

**Why do we need to do it?**
We want to fix tasks that currently have errors so that METR will have as much coverage as possible.

### Scope

**What are the high level steps to resolve this issue?**
Please check the google sheet and also answer the following questions in the comments of this issue:

- [ ] Check the [Task Improvements Worklist](https://docs.google.com/spreadsheets/d/1d1M7ozvJeapPMpPXmdwnJc_dIFrgHVRjA1MgosX4brA/edit?userstoinvite=sami%40metr.org&sharingaction=manageaccess&role=writer&gid=323653529#gid=323653529) and note the errors listed and make a comment on this issue about what errors we need to fix. Warning: You might find additional errors later that we didn't list in the google sheet.
- [ ] Does the task have task family structure? If not, modify the task to have the correct structure.
- [ ] Does the task have a task manaifest file? If not, create one.
- [ ] Does it have pytest? If not, add at least one test that seems relevant.
- [ ] Can the tasks be graded properly? If it doesn't have automatic grading, add a scoring function.
- [ ] Does the docker container start? If not, fix it.
- [ ] Does the task run with viv? If not, fix it.
- [ ] Does the task have a descriptive README.md in the correct format? If not, fix it.
- [ ] Open a PR with your changes.
- [ ] Add time spent to comments on ticket


### Acceptance Criteria

**How will a reviewer determine that work is complete?**
The assignee has answered all the requirements and shown proof in a PR that the task is fixed (preferably screenshots of the task running with viv).

### Price

**How much will EquiStamp Pay for Successful Resolution?**
**USD:$150**
**PRICE EXPIRATION DATETIME UTC:October 10, 2024 11:59 PM UTC**

### Resolution Criteria Evaluator

**Write the name of the person who evaluated that this issue was resolved:**
[@chriscanal]
