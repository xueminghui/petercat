from typing import AsyncIterator, Optional
from github import Auth
from agent.base import AgentBuilder
from agent.llm import get_llm

from core.models.bot import Bot
from agent.prompts.bot_template import generate_prompt_by_repo_name
from petercat_utils.data_class import ChatData

from agent.tools import issue, pull_request, sourcecode, knowledge, git_info


def get_tools(bot: Bot, token: Optional[Auth.Token]):
    issue_tools = issue.factory(token=token)
    pull_request_tools = pull_request.factory(token=token)
    print(f"get_tools, token={token.token}")
    return {
        "search_knowledge": knowledge.factory(bot_id=bot.id),
        "create_issue": issue_tools["create_issue"],
        "get_issues": issue_tools["get_issues"],
        "get_file_content": pull_request_tools["get_file_content"],
        "create_review_comment": pull_request_tools["create_review_comment"],
        "create_pr_summary": pull_request_tools["create_pr_summary"],
        "search_issues": issue_tools["search_issues"],
        "search_code": sourcecode.search_code,
        "search_repo": git_info.search_repo,
    }

def agent_stream_chat(input_data: ChatData, token: Auth.Token, bot: Bot) -> AsyncIterator[str]:
    agent = AgentBuilder(
        chat_model=get_llm(bot.llm),
        prompt=bot.prompt or generate_prompt_by_repo_name("ant-design"),
        tools=get_tools(bot=bot, token=token),
    )
    return agent.run_stream_chat(input_data)


def agent_chat(input_data: ChatData, token: Auth.Token, bot: Bot) -> AsyncIterator[str]:

    prompt = bot.prompt or generate_prompt_by_repo_name("ant-design")

    if input_data.prompt is not None:
        prompt = f"{prompt}\n\n{input_data.prompt}"

    agent = AgentBuilder(
        chat_model=get_llm(bot.llm),
        prompt=prompt,
        tools=get_tools(bot, token=token),
    )

    return agent.run_chat(input_data)
