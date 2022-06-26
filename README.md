<h1 align="center">
  Welcome to get-all-slack-emojis 👋
</h1>

<h3 align="center">
  This package allows to get all custom emojis in your Slack workspace.
</h3>

## Installation

1. Get Slack API Token

2. Add an OAuth scope for your API Token **emoji:read**

3. Install your Slack App to target workspace

4. Git clone this repository:

  ```zsh
  git clone git@github.com:user/get-all-slack-emojis.git
  ```

## Usage

1. Access [here](https://api.slack.com/apps)

2. [Your Apps] -> Select App -> [OAuth & Permissions]

3. Get your OAuth Token

4. Open Terminal, move to clone directory, and run this:

  ```zsh:zsh
  python all_slack_emojis -o <OUTPUT DIR> <YOUR OAUTH TOKEN>
  ```

5. ***Get 'em all!***

## Reference

I created this package because the following repo does not work, maybe due to some specification changes of Slack API.

jkloo / slack-emojis
<https://github.com/jkloo/slack-emojis>
