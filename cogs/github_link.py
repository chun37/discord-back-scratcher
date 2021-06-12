# from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from typing import Optional
from urllib.parse import ParseResult, urlparse

import aiohttp
from discord import File, Message
from discord.ext.commands import Bot

from custom import CustomCog

GITHUB_LINK_PATTERN = re.compile(
    r"https?://github\.com/(?P<owner>[^/]+)/(?P<repository>[^/]+?)/(?P<type>[^/]+?)(?P<path>.+)"
)


class AllowedExtenisons(Enum):
    PYTHON = "py"
    RUBY = "rb"
    YML = "yml"
    YAML = "yaml"
    VBS = "vbs"
    VBA = "vba"
    TS = "ts"
    TSX = "tsx"
    THRIFT = "thrift"
    SWIFT = "swift"
    SQL = "sql"
    SCSS = "scss"
    RUST = "rs"
    TEXT = "txt"
    PERL = "pl"
    PHP = "php"
    OBJECTIVE_C = "objc"
    MARKDOWN = "md"
    MAKE = "make"
    LUA = "lua"
    TEX = "tex"
    KOTLIN = "kt"
    JAVASCRIPT = "js"
    JSX = "jsx"
    JAVA = "java"
    JSON = "json"
    TOML = "toml"
    INI = "ini"
    HASKELL = "hs"
    SVG = "svg"
    PLIST = "plist"
    RSS = "rss"
    XHTML = "xhtml"
    HTML = "html"
    XML = "xml"
    GOLANG = "go"
    ELM = "elm"
    DIFF = "diff"
    BAT = "bat"
    CSV = "csv"
    CSS = "css"
    CPP = "cpp"
    C = "c"
    H = "h"
    CS = "cs"
    BRAINFUCH = "bf"
    SHELL = "sh"
    ASCIIDOC = "asciidoc"
    APPLESCRIPT = "applescript"


@dataclass
class GitHubLink:
    scheme: str
    domain: str
    owner: str
    repository: str
    type: str
    path: str
    fragment: str

    async def to_discord(self) -> Optional[File]:
        return None


@dataclass
class GitHubBlobLink(GitHubLink):
    line_start: int = 0
    line_end: int = 0

    def __post_init__(self) -> None:
        if not self.fragment:
            return

        lines = self.fragment.split("-")
        if len(lines) == 1:
            start, *_ = lines
            end = "L0"
        elif len(lines) == 2:
            start, end = lines

        self.line_start = int(start[1:])
        self.line_end = int(end[1:])

    def get_raw_link(self) -> str:
        return ParseResult(
            scheme=self.scheme,
            netloc=self.domain,
            path=f"/{self.owner}/{self.repository}/raw/{self.path}",
            params="",
            query="",
            fragment="",
        ).geturl()

    def crop_code(self, code: str) -> str:
        """
        all: start=0, end=0
        one line: start=N, end=0
        multi line: start=N, end=M
        """
        if self.line_start == 0 and self.line_end == 0:
            return code

        lines = code.split("\n")

        start = self.line_start - 1
        end = self.line_start if self.line_end == 0 else self.line_end
        selected_lines = lines[start:end]

        return "\n".join(selected_lines)

    async def get_code(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.get_raw_link()) as response:
                code = await response.text()

        cropped_code = self.crop_code(code)

        return cropped_code

    async def to_discord(self) -> Optional[File]:
        code = await self.get_code()
        base_file_name = self.path.split("/")[-1]
        raw_extension = base_file_name.split(".")[-1].lower()

        try:
            AllowedExtenisons(raw_extension)
            file_name = base_file_name
        except ValueError:
            file_name = base_file_name + ".txt"

        return File(StringIO(code), file_name)


def make_link(string: str) -> GitHubLink:
    parsed = urlparse(string)
    _, owner, repository, type_, *splitted_path = parsed.path.split("/")

    path = "/".join(splitted_path)

    class_ = GitHubLink

    if type_ == "blob":
        class_ = GitHubBlobLink

    return class_(
        parsed.scheme, parsed.netloc, owner, repository, type_, path, parsed.fragment
    )


class GitHubExpand(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @CustomCog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return

        expand_code_files = [
            await make_link(match.group(0)).to_discord()
            for match in GITHUB_LINK_PATTERN.finditer(message.content)
        ]
        non_empty_expands = [code for code in expand_code_files if code]

        if not non_empty_expands:
            return

        self.on_message_bot_has_permissions(
            message.guild,
            message.channel,
            self.bot.user,
            attach_files=True,
        )

        for code in non_empty_expands:
            await message.reply(file=code)


def setup(bot: Bot) -> None:
    bot.add_cog(GitHubExpand(bot))
