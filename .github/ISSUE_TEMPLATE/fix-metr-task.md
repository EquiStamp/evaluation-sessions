---
name: Fix METR Task
about: Use this issue template to fix a METR task.
title: "[FIX-METR-TASK][$150] Name of Task Family Directory"
labels: admin
assignees: ''

---

### Task Errors

**What needs to be done?**
Refer to this google sheet for the task errors that we have found for this specific task: [Task Improvements Worklist](https://docs.google.com/spreadsheets/d/1d1M7ozvJeapPMpPXmdwnJc_dIFrgHVRjA1MgosX4brA/).

**Please track your time working on this down to the minute**

### Business Driver

**Why do we need to do it?**
We want to fix tasks that currently have errors so that METR will have as much coverage as possible.

### Scope

**What are the high level steps to resolve this issue?**

Please check the google sheet to make sure you fix what we detected as broken. Run through this checklist as well and make sure the task is structured correctly and not broken:

- [ ] Check the [Task Improvements Worklist](https://docs.google.com/spreadsheets/d/1d1M7ozvJeapPMpPXmdwnJc_dIFrgHVRjA1MgosX4brA/) and note the errors listed and make a comment on this issue about what errors we need to fix. Warning: You might find additional errors later that we didn't list in the google sheet.
- [ ] Does the task have task family structure? If not, modify the task to have the correct structure.
- [ ] Does the task have a task manifest file? If not, create one.
- [ ] Does it have pytest? If not, add at least one test that seems relevant.
- [ ] Can the tasks be graded properly? If it doesn't have automatic grading, add a scoring function.
- [ ] Does the docker container start? If not, fix it.
- [ ] Does the task run with viv? If not, fix it.
- [ ] Does the task have a meta folder that has a summary.md inside meta? if not could you make a [summary.md with this format](https://github.com/EquiStamp/metr-task-template/blob/main/meta/summary.md)?
- [ ] Does the task have a meta folder that has a detail.md inside meta? if not could you make a [detail.md with this format](https://github.com/EquiStamp/metr-task-template/blob/main/meta/detail.md)?
- [ ] Does the task have a meta folder that has a eval-info.json inside meta? if not could you a [eval-info.json with this format](https://github.com/EquiStamp/metr-task-template/blob/main/meta/eval_info.json)?
- [ ] Open a PR with your changes.
- [ ] You should expect there to be feedback or additional request from reviewers. Please implement their feedback.
- [ ] Add total time spent to comments on this github issue.


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
