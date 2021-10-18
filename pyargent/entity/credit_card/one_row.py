from dataclasses import dataclass
from dataclasses import field
import re
import mojimoji


@dataclass(init=True, order=True)
class OneRow:
    date: str = field(default_factory=str)
    description: str = field(default_factory=str, compare=False)
    total_billing: int = field(default_factory=int)
    count: int = field(default_factory=int, compare=False)
    num: int = field(default_factory=int, compare=False)
    actual_billing: int = field(default_factory=int, compare=False)
    comment: str = field(default_factory=str, compare=False)

    # candidate pattern regex
    DATE = r"(?P<date>[0-9]{4}/[0-9]{2}/[0-9]{2})"
    DESCRIPTION = r"(?P<description>[^,.]+?)"
    TOTAL_BILLING = r"(?P<total_billing>-?[0-9]*)"
    COUNT = r"(?P<count>[0-9]*)"
    NUM = r"(?P<num>[0-9]*)"
    ACTUAL_BILLING = r"(?P<actual_billing>-?[0-9]*)"
    COMMENT = r"(?P<comment>[^,.]*)"

    PATTERN_LIST_1 = [DATE, DESCRIPTION, TOTAL_BILLING, COUNT, NUM, ACTUAL_BILLING, COMMENT]

    @classmethod
    def from_text(cls, text: str):
        pattern = ",".join(cls.PATTERN_LIST_1)
        result = re.match(pattern, cls.format_str(text))
        if result:
            return OneRow(**result.groupdict())
        return None

    @staticmethod
    def format_str(text: str) -> str:
        table = str.maketrans({"\u3000": "", " ": "", "\t": "", "\n": "", "－": "ー", "−": "ー", "―": "ー"})
        _text = text.translate(table)
        _text = mojimoji.zen_to_han(_text, kana=False)
        _text = mojimoji.han_to_zen(_text, digit=False, ascii=False)
        return _text
