from __future__ import annotations

import time
import discord
from discord.ext import commands
from discord import Colour
from datetime import datetime
from typing import Optional, Union, List
from datetime import timedelta
from itertools import groupby
from time import time

from internal.context import Context


class EmbedHelper(discord.Embed):
    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        colour: Optional[Union[Colour, int]] = None,
        thumbnail_url: Optional[str] = None,
        author_url: Optional[str] = None,
        author_name: Optional[str] = None,
        author_icon_url: Optional[str] = None,
        footer_url: Optional[str] = None,
        image_url: Optional[str] = None,
        footer_text: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        fields: Optional[Union[List[dict], List[tuple], dict, tuple]] = None,
    ):

        # TODO: ADD DOCSTRING

        super().__init__()

        self.title = title or self.Empty

        self.description = description or self.Empty

        self.colour = colour or 0x87CEEB

        self.timestamp = timestamp or self.Empty

        if footer_url or footer_text:
            if footer_url and footer_text:
                self.set_footer(text=footer_text, icon_url=footer_url)
            else:
                if footer_text:
                    self.set_footer(text=footer_text)
                else:
                    self.set_footer(icon_url=footer_url)

        if image_url:
            self.set_image(url=image_url)

        if author_name and any(author_url, author_icon_url):
            self.set_author(
                name=author_name,
                icon_url=author_url or self.Empty,
                url=author_url or self.Empty,
            )

        if thumbnail_url:
            self.set_thumbnail(url=thumbnail_url)

        if isinstance(fields, list):
            for field in fields:
                if isinstance(field, dict):
                    self.add_field(**field)
                else:
                    try:
                        name, value, inline = field

                        self.add_field(name=name, value=value, inline=inline)

                    except ValueError:
                        name, value = field
                        self.add_field(name=name, value=value, inline=True)

        elif isinstance(fields, dict):
            self.add_field(**fields)

        elif isinstance(fields, tuple):
            try:
                name, value, inline = fields

                self.add_field(name=name, value=value, inline=inline)

            except ValueError:
                name, value = fields
                self.add_field(name=name, value=value, inline=True)

    @classmethod
    def from_exception(cls, exception: Exception) -> EmbedHelper:
        return cls(
            title=f"⚠️ An Error Occurred.", description=str(exception), colour=0xE74C3C
        )


def convert_date(date: datetime) -> str:
    """Convert a datetime object to a readable format."""

    return date.strftime(f"%A, %B %-d, %Y at %-I:%M {('A', 'P')[date == 0]}M UTC")


def get_timedelta(arg: str) -> timedelta:
    """Converts a string of time for eg: 5h -> into an equivalent timedelta object."""
    arg = arg.lower()
    amts, units = [], []

    unit_mapping = {
        "h": "hours",
        "hour": "hours",
        "m": "minutes",
        "minute": "minutes",
        "s": "seconds",
        "second": "seconds",
        "d": "days",
        "day": "days",
        "M": "months",  # m already assigned for minutes
        "y": "years",
    }

    grouped = groupby(arg, key=str.isdigit)

    for key, group in grouped:
        if key:  # means isdigit returned true, meaning they are numbers
            amts.append(int("".join(group)))
        else:
            units.append(
                unit_mapping["".join(group)]
            )  # convert h -> hours, m -> minutes and so on

    return timedelta(**dict(zip(units, amts)))


def get_str_time_mapping(arg: str) -> str:
    """returns the string equivalent of get_timedelta"""
    unit_mapping = {
        "h": "hours",
        "hour": "hours",
        "m": "minutes",
        "minute": "minutes",
        "s": "seconds",
        "second": "seconds",
        "d": "days",
        "day": "days",
        "M": "months",  # m already assigned for minutes
        "y": "years",
    }

    arg_string = []
    arg_int = []
    for letter in arg:
        if not letter.isdigit():
            arg_string.append(letter)
        else:
            arg_int.append(letter)

    arg = "".join(l for l in arg_string)
    argint = "".join(i for i in arg_int)

    return {
        "unit": unit_mapping[arg],
        "amount": argint,
    }


class CustomTimeConverter(commands.Converter):
    """Returns a timedelta object."""

    async def convert(self, ctx: Context, arg: str) -> timedelta:
        return get_timedelta(arg)


class IDGenerator:
    def __init__(self):
        self.wid = 0
        self.inc = 0

    def __next__(self):
        t = round(time() * 1000) - 1609459200000
        self.inc += 1
        return (t << 14) | (self.wid << 6) | (self.inc % 2 ** 6)
