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

-1c. read any new issues in known-issues/

0a. familiarize yourself with @specs/

0b. familiarize yourself with @IMPLEMENTATION_PLAN.md to understand the plan so far

0c. familiarize yourself with the code in @src/

0d. familiarize yourself with the code in @examples/

1. First task is to study @IMPLEMENTATION_PLAN.md (it may be incorrect) and is to use subagents to study existing source code in src/ and compare it against the specifications. From that create/update a @IMPLEMENTATION_PLAN.md which is a bullet point list sorted in priority of the items which have yet to be implemeneted. Think extra hard and use the oracle to plan. Consider searching for TODO, minimal implementations and placeholders. Study @IMPLEMENTATION_PLAN.md to determine starting point for research and keep it up to date with items considered complete/incomplete using subagents.


2. Second task is to use subagents to study existing source code in examples/ then compare it against the specifications. From that create/update a @IMPLEMENTATION_PLAN.md which is a bullet point list sorted in priority of the items which have yet to be implemeneted. Think extra hard and use the oracle to plan. Consider searching for TODO, minimal implementations and placeholders. Study @IMPLEMENTATION_PLAN.md to determine starting point for research and keep it up to date with items considered complete/incomplete.


3. use `git add -A` and `git commit -m "..."` to commit your changes - do not include any claude attribution


999. DO NOT EXPLORE THE `.pixi` directory it only contains the pixi environments. Any information about the environment can be found in the `pixi.toml`. Trying to explore it will take to long. 

9999. FOCUS ON ACCOMPLISHING THE ABOVE TASKS

99999.  DO NOT EXPLORE THE `.pytest_cache` directory

999999.  DO NOT EXPLORE THE `.ruff_cache` directory


9999999.  DO NOT EXPLORE THE `.devcontainer` directory

99999999.  DO NOT EXPLORE THE `.config` directory

999999999. DO NOT try to glob for python files in the root directory! Only glob python files in src, test, specs, scripts, and exmaples

9999999999. When search the code base only search in these folders src, test, specs, scripts, and exmaples and the file on the root level

9999999999999. The python package should be called `cadcode`