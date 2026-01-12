-1a. list open issues and compare with known-issues/:
    ```bash
    # List issue numbers from GitHub
    curl -s "https://api.github.com/repos/lllangWV/cadcode-1/issues?state=open" | jq -r '.[].number'

    # List existing known-issues files
    ls known-issues/
    ```

-1b. for any issues on GitHub not in known-issues/, fetch and save:
    ```bash
    # Fetch issue #N and save as markdown
    curl -s "https://api.github.com/repos/lllangWV/cadcode-1/issues/N" | \
      jq -r '"# \(.title)\n\n**Issue:** [#\(.number)](\(.html_url))\n**Author:** \(.user.login)\n**Created:** \(.created_at[:10])\n**State:** \(.state)\n\n\(.body)"' \
      > known-issues/issue-N-slug.md
    ```

-1c. read any new issues in known-issues/ and incorporate them into @IMPLEMENTATION_PLAN.md

0a. familiarize yourself with @specs/

0b. familiarize yourself with the code in @src/

1. read @IMPLEMENTATION_PLAN.md and implement the single highest priority feature using up to 5 subagents, including anything in the out of scope / future work - that's now in scope!

2. After implementing functionality or resolving problems, run the typechecking, linting, and tests for that unit of code that was improved. If functionality is missing then it's your job to add it as per the application specifications. Think hard. Ensure all tests and linting passes then update @IMPLEMENTATION_PLAN.md with your progress. 
-2a. For typechecking use `pixi run -q -e dev typecheck`
-2b. For testing use `pixi run -q -e dev test`
-2c. For linting use `pixi run -q -e dev lint`

3. use `git add -A` and `git commit -m "..."` to commit your changes - do not include any claude attribution

## Other instruction points

999. Important: When you learn something new about how to run the code runs or examples make sure you update @CLAUDE.md using a subagent but keep it brief. For example if you run commands multiple times before learning the correct command then that file should be updated.


9999. Important: For any bugs you notice, it's important to resolve them or document them in @IMPLEMENTATION_PLAN.md to be resolved using a subagent even if it is unrelated to the current piece of work after documenting it in @IMPLEMENTATION_PLAN.md

99999. Important: You may add extra logging if required to be able to debug the issues.

999999. Important:  When authoring documentation (ie. cadcode documentation) capture the why tests and the backing implementation is important.

9999999. ALWAYS KEEP @IMPLEMENTATION_PLAN.md up to do date with your learnings using a subagent. Especially after wrapping up/finishing your turn.

99999999. When @IMPLEMENTATION_PLAN.md becomes large periodically clean out the items that are completed from the file using a subagent.

999999999. If you find inconsistentcies in the specs/* then use the oracle and then update the specs. Specifically around types and lexical tokens.

9999999999. DO NOT IMPLEMENT PLACEHOLDER OR SIMPLE IMPLEMENTATIONS. WE WANT FULL IMPLEMENTATIONS. DO IT OR I WILL YELL AT YOU

99999999999. SUPER IMPORTANT DO NOT IGNORE. DO NOT PLACE STATUS REPORT UPDATES INTO @CLAUDE.md

999999999999. Keep CLAUDE.md up to date with information on how to build the cadcode and your learnings to optimise the build/test loop using a subagent.


9999999999999. The python package should be called `cadcode`