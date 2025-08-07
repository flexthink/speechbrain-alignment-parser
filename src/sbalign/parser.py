import re
from dataclasses import dataclass, field
from enum import Enum

RE_ITEM_ERROR_RATE = re.compile(
    r"%\w+ (?P<error_rate>\d+\.(\d+)?) \[ (?P<errors>\d+) / (?P<tokens>\d+)"
    r", (?P<ins>\d+) ins, (?P<del>\d+) del, (?P<sub>\d+) sub \]"
)
RE_UTT_ERROR_RATE = re.compile(
    r"%\w+ (?P<error_rate>\d+\.(\d+)?) "
    r"\[ (?P<errors>\d+) / (?P<total>\d+?) \]"
)

RE_SEP = re.compile("^=+$")

RE_ITEM_HEADER = re.compile(
    r"(?P<uttid>\S+), %\w+ (?P<error_rate>\d+\.(\d+)?) "
    r"\[ (?P<errors>\d+) / (?P<tokens>\d+), (?P<ins>\d+) ins,"
    r" (?P<del>\d+) del, (?P<sub>\d+) sub \]"
)


@dataclass
class Alignment:
    error_rate: float = 0.0
    insertions: int = 0
    deletions: int = 0
    substitutions: int = 0
    items: list = field(default_factory=list)
    utt_error_rate: float = 0.0
    utt_errors: int = 0
    utt_total: int = 0


@dataclass
class AlignmentItem:
    uttid: str = ""
    ref: list = field(default_factory=list)
    hyp: list = field(default_factory=list)
    alignment: list = field(default_factory=list)
    error_rate: float = 0.0
    errors: int = 0
    tokens: int = 0
    insertions: int = 0
    deletions: int = 0
    substitutions: int = 0


class State(Enum):
    START = 0
    UTT_ERROR_RATE = 1
    LEGEND = 2
    BODY = 3
    HEADER = 4
    REF = 6
    ALIGNMENT = 7
    HYP = 8


def parse_alignment_file(file_name):
    with open(file_name) as alignment_file:
        return parse_alignment(alignment_file)


def parse_alignment(lines):
    if isinstance(lines, str):
        lines = lines.split("\n")
    state = State.START
    alignment = Alignment()
    item = AlignmentItem()
    for line in lines:
        line = line.strip()
        if state == State.START:
            if match_error_rate(line, alignment):
                state = State.UTT_ERROR_RATE
        elif state == State.UTT_ERROR_RATE:
            if match_utt_error_rate(line, alignment):
                state = State.LEGEND
        elif state == State.LEGEND:
            if is_separator(line):
                state = State.BODY
        elif state == State.BODY:
            if is_separator(line):
                state = State.HEADER
        elif state == State.HEADER:
            match_item_header(line, item)
            state = State.REF
        elif state == State.REF:
            match_ref(line, item)
            state = State.ALIGNMENT
        elif state == State.ALIGNMENT:
            match_alignment(line, item)
            state = State.HYP
        elif state == State.HYP:
            if is_separator(line):
                alignment.items.append(item)
                item = AlignmentItem()
                state = State.BODY
            else:
                match_hyp(line, item)

    return alignment


def match_error_rate(line: str, alignment: Alignment):
    result = False
    match = RE_ITEM_ERROR_RATE.match(line)
    if match:
        alignment.error_rate = float(match.group("error_rate"))
        alignment.insertions = int(match.group("ins"))
        alignment.deletions = int(match.group("del"))
        alignment.substitutions = int(match.group("sub"))
        result = True
    return result


def match_utt_error_rate(line: str, alignment: Alignment):
    result = False
    match = RE_UTT_ERROR_RATE.match(line)
    if match:
        alignment.utt_error_rate = float(match.group("error_rate"))
        alignment.utt_errors = int(match.group("errors"))
        alignment.utt_total = int(match.group("total"))
        result = True
    return result


def match_item_header(line: str, alignment_item: AlignmentItem):
    result = False
    match = RE_ITEM_HEADER.match(line)
    if match:
        alignment_item.uttid = match.group("uttid")
        alignment_item.error_rate = float(match.group("error_rate"))
        alignment_item.insertions = int(match.group("ins"))
        alignment_item.deletions = int(match.group("del"))
        alignment_item.substitutions = int(match.group("sub"))
        alignment_item.errors = int(match.group("errors"))
        alignment_item.tokens = int(match.group("tokens"))
        result = True
    return result


def strip_split(line):
    return [item.strip() for item in line.split(" ; ")]


def match_ref(line, alignment_item):
    alignment_item.ref = strip_split(line)


def match_hyp(line, alignment_item):
    alignment_item.hyp = strip_split(line)


def match_alignment(line, alignment_item):
    alignment_item.alignment = strip_split(line)


def is_separator(line):
    return RE_SEP.match(line)
