import os
import re
from datetime import date, datetime
from typing import Any, Callable, Iterable, TypeVar, overload

from rich import print
from simple_term_menu import TerminalMenu

from utils import bad_input, error, stress

T = TypeVar("T")
CT = TypeVar("CT", bound=Callable)


class Menu:
    @staticmethod
    def _invalid_input(i: Any = "") -> None:
        print(error("Invalid input" + (f": {bad_input(i)}" if i else "")))

    @staticmethod
    def _range_error(
        *,
        min_value: Any | None = None,
        max_value: Any | None = None,
        type: str = "value",
    ) -> None:
        if min_value is None:
            print(error(f"Expected {type} less than {stress(max_value)}"))
        elif max_value is None:
            print(error(f"Expected {type} greater than {stress(min_value)}"))
        else:
            print(
                error(
                    f"Expected {type} between {stress(min_value)} and {stress(max_value)}"
                )
            )

    @staticmethod
    def _validate_range(
        value: Any,
        /,
        *,
        min_value: int | float | None = None,
        max_value: int | float | None = None,
    ) -> bool:
        comparison_value = len(value) if isinstance(value, Iterable) else value
        if min_value is None and max_value is None:
            return True
        _m = (
            min_value
            if min_value is not None and comparison_value < min_value
            else None
        )
        _M = (
            max_value
            if max_value is not None and comparison_value > max_value
            else None
        )
        if _m is not None or _M is not None:
            Menu._range_error(
                min_value=min_value,
                max_value=max_value,
                type="length" if isinstance(value, Iterable) else "value",
            )
            return False
        return True

    @overload
    def _get_multi(
        self,
        sequence: Callable[[Any], list],
        cast: CT = str,
        /,
        prompt_text: str = "",
        default: list | tuple | set = None,
        *,
        delimiter: str = ": ",
        separator: str = ",",
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> list[T]:
        ...

    @overload
    def _get_multi(
        self,
        sequence: Callable[[Any], tuple],
        cast: CT = str,
        /,
        prompt_text: str = "",
        default: list | tuple | set = None,
        *,
        delimiter: str = ": ",
        separator: str = ",",
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> tuple[T]:
        ...

    @overload
    def _get_multi(
        sequence: Callable[[Any], set],
        cast: CT = str,
        /,
        prompt_text: str = "",
        default: list | tuple | set = None,
        *,
        delimiter: str = ": ",
        separator: str = ",",
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> set[T]:
        ...

    def _get_multi(
        self,
        sequence: Callable[[Any], list | tuple | set],
        cast: CT = str,
        /,
        prompt_text: str = "",
        default: list | tuple | set = None,
        *,
        delimiter: str = ": ",
        separator: str = ",",
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> list[CT] | tuple[CT] | set[CT]:
        _d = f" {list(default)}" if default is not None else ""
        raw = input(
            f"{prompt_text} (Seperate values by `{separator}`){_d}{delimiter}"
        ).strip()
        try:
            cleaned = sequence(map(cast, map(str.strip, raw.split(separator))))
        except ValueError:
            if len(raw) != 0 or default is None:
                Menu._invalid_input()
                cleaned = self._get_multi(
                    sequence,
                    cast,
                    prompt_text,
                    default,
                    delimiter=delimiter,
                    separator=separator,
                    min_length=min_length,
                    max_length=max_length,
                )
            else:
                cleaned = default
        else:
            if not Menu._validate_range(
                cleaned, min_value=min_length, max_value=max_length
            ):
                cleaned = self._get_multi(
                    sequence,
                    cast,
                    prompt_text,
                    default,
                    delimiter=delimiter,
                    separator=separator,
                    min_length=min_length,
                    max_length=max_length,
                )
        return cleaned

    def clear_screen(self) -> None:
        cmd = "cls" if os.name == "nt" else "clear"
        os.system(cmd)

    def get_int(
        self,
        prompt_text: str = "",
        /,
        default: int = None,
        *,
        delimiter: str = ": ",
        min_value: int = None,
        max_value: int = None,
    ) -> int:
        _d = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt_text}{_d}{delimiter}").strip()
        try:
            cleaned = int(raw)
        except ValueError:
            if len(raw) != 0 or default is None:
                Menu._invalid_input()
                cleaned = self.get_int(
                    prompt_text,
                    default,
                    delimiter=delimiter,
                    min_value=min_value,
                    max_value=max_value,
                )
            else:
                cleaned = default
        else:
            if not Menu._validate_range(
                cleaned, min_value=min_value, max_value=max_value
            ):
                cleaned = self.get_int(
                    prompt_text,
                    default,
                    delimiter=delimiter,
                    min_value=min_value,
                    max_value=max_value,
                )
        return cleaned

    def get_float(
        self,
        prompt_text: str = "",
        /,
        default: float = None,
        *,
        delimiter: str = ": ",
        min_value: int = None,
        max_value: int = None,
    ) -> float:
        _d = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt_text}{_d}{delimiter}").strip()
        try:
            cleaned = float(raw)
        except ValueError:
            if len(raw) != 0 or default is None:
                Menu._invalid_input()
                cleaned = self.get_float(
                    prompt_text,
                    default,
                    delimiter=delimiter,
                    min_value=min_value,
                    max_value=max_value,
                )
            else:
                cleaned = default
        else:
            if not Menu._validate_range(
                cleaned, min_value=min_value, max_value=max_value
            ):
                cleaned = self.get_float(
                    prompt_text,
                    default,
                    delimiter=delimiter,
                    min_value=min_value,
                    max_value=max_value,
                )
        return cleaned

    def get_list(
        self,
        prompt_text: str,
        /,
        default: list = None,
        *,
        cast_to: CT = str,
        delimiter: str = ": ",
        separator: str = ",",
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> list[CT]:
        return self._get_multi(
            list,
            cast_to,
            prompt_text,
            default,
            delimiter=delimiter,
            separator=separator,
            min_length=min_length,
            max_length=max_length,
        )

    def get_tuple(
        self,
        prompt_text: str,
        /,
        default: tuple = None,
        *,
        cast_to: CT = str,
        delimiter: str = ": ",
        separator: str = ",",
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> tuple[CT]:
        return self._get_multi(
            tuple,
            cast_to,
            prompt_text,
            default,
            delimiter=delimiter,
            separator=separator,
            min_length=min_length,
            max_length=max_length,
        )

    def get_set(
        self,
        prompt_text: str,
        /,
        default: set = None,
        *,
        cast_to: CT = str,
        delimiter: str = ": ",
        separator: str = ",",
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> set[CT]:
        return self._get_multi(
            set,
            cast_to,
            prompt_text,
            default,
            delimiter=delimiter,
            separator=separator,
            min_length=min_length,
            max_length=max_length,
        )

    def get_str(
        self,
        prompt_text: str = "",
        /,
        default: str = None,
        *,
        delimiter: str = ": ",
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> str:
        _d = f" [{default}]" if default is not None else ""
        cleaned = input(f"{prompt_text}{_d}{delimiter}").strip()
        if len(cleaned) == 0:
            if default is None:
                Menu._invalid_input()
                cleaned = self.get_str(
                    prompt_text,
                    default,
                    delimiter=delimiter,
                    min_length=min_length,
                    max_length=max_length,
                )
            else:
                cleaned = default
        elif not Menu._validate_range(
            cleaned, min_value=min_length, max_value=max_length
        ):
            cleaned = self.get_str(
                prompt_text,
                default,
                delimiter=delimiter,
                min_length=min_length,
                max_length=max_length,
            )
        return cleaned

    def get_date(
        self,
        prompt_text: str = "",
        /,
        default: date = None,
        *,
        delimiter: str = ": ",
        after: date | None = None,
        before: date | None = None,
        format: str = "%d/%m/%y",
    ) -> date:
        _format_display_map = {
            "%d": "dd",
            "%b": "MMM",
            "%m": "mm",
            "%y": "yy",
            "%Y": "YYYY",
        }
        if "%" in re.sub("%[dbmyY]", "", format):
            raise ValueError(f"Only `{'`, `'.join(_format_display_map)}` are supported")

        _format = format
        for k, v in _format_display_map.items():
            _format = _format.replace(k, v)
        _default = default.strftime(format) if default else None

        raw = self.get_str(
            f"{prompt_text} ({_format})",
            _default,
            delimiter=delimiter,
            min_length=len(_format) - 2,
            max_length=len(_format),
        )

        if raw == _default:
            cleaned = default
        else:
            try:
                cleaned = datetime.strptime(raw, format).date()
            except (ValueError, TypeError):
                Menu._invalid_input()
                cleaned = self.get_date(
                    prompt_text,
                    default,
                    delimiter=delimiter,
                    after=after,
                    before=before,
                    format=format,
                )
            else:
                if not Menu._validate_range(cleaned, min_value=after, max_value=before):
                    cleaned = self.get_date(
                        prompt_text,
                        default,
                        delimiter=delimiter,
                        after=after,
                        before=before,
                        format=format,
                    )

        return cleaned

    def confirm(self, prompt_text: str, /, default: bool | None = None) -> bool:
        raw = TerminalMenu(
            (
                "Yes" + (" ✓" if default else ""),
                "No" + (" ✓" if default is False else ""),
            ),
            title=prompt_text,
            cursor_index=1 if default is False else 0,
        ).show()
        if raw is None:
            if default is not None:
                cleaned = default
            else:
                Menu._invalid_input()
                cleaned = self.confirm(prompt_text, default)
        else:
            cleaned = raw == 0
        return cleaned

    @overload
    def choose(
        prompt_text: str, /, options: list[str] | tuple[str], default: int | str
    ) -> int:
        ...

    @overload
    def choose(prompt_text: str, /, options: dict[str, T], default: str) -> T:
        ...

    def choose(
        self,
        prompt_text: str,
        /,
        options: list[str] | tuple[str] | dict[str, T],
        default: int | str = None,
    ) -> int | T:
        _options = list(options)
        _default = _options.index(default) if isinstance(default, str) else default

        raw = TerminalMenu(_options, title=prompt_text, cursor_index=_default).show()
        if raw is None:
            if default is not None:
                cleaned = options[default] if isinstance(options, dict) else default
            else:
                Menu._invalid_input()
                cleaned = self.choose(prompt_text, options, default)
        else:
            cleaned = (
                raw if isinstance(options, list | tuple) else options[_options[raw]]
            )
        return cleaned

    @overload
    def choose_multi(
        prompt_text: str,
        /,
        options: list[str],
        default: list[int] | list[str],
        *,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> list[int]:
        ...

    @overload
    def choose_multi(
        prompt_text: str,
        /,
        options: tuple[str],
        default: tuple[int] | tuple[str],
        *,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> tuple[int]:
        ...

    @overload
    def choose_multi(
        prompt_text: str,
        /,
        options: dict[str, T],
        default: Iterable[str],
        *,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> list[T]:
        ...

    def choose_multi(
        self,
        prompt_text: str,
        options: list[str] | tuple[str] | dict[str, T],
        /,
        default: Iterable[int] | Iterable[str] = None,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> int | T:
        _options = list(options)
        raw = TerminalMenu(
            _options,
            title=prompt_text,
            preselected_entries=default,
            multi_select=True,
            show_multi_select_hint=True,
            multi_select_select_on_accept=False,
        ).show()
        if raw is None:
            if default is not None:
                cleaned = (
                    [options[d] for d in default]
                    if isinstance(options, dict)
                    else [options.index(d) for d in default]
                )
            else:
                Menu._invalid_input()
                cleaned = self.choose_multi(
                    prompt_text,
                    options,
                    default,
                    min_length=min_length,
                    max_length=max_length,
                )
        elif not Menu._validate_range(raw, min_value=min_length, max_value=max_length):
            cleaned = self.choose_multi(
                prompt_text,
                options,
                default,
                min_length=min_length,
                max_length=max_length,
            )
        else:
            cleaned = (
                raw
                if isinstance(options, list | tuple)
                else [options[_options[r]] for r in raw]
            )
        return cleaned


if __name__ == "__main__":
    from datetime import timedelta

    def _break() -> None:
        print("=" * 30, "\n")

    menu = Menu()

    print(
        "You entered",
        menu.get_int(
            "Enter number between 1 and 5",
            3,
            min_value=1,
            max_value=5,
            delimiter=" -> ",
        ),
    )
    _break()
    print(
        "You entered",
        menu.get_float("Enter decimal between 0 and 1", min_value=0, max_value=1),
    )
    _break()
    print(
        "You entered the string",
        menu.get_str(
            "Enter anything, with atleast 1 and utmost 5 chars",
            min_length=1,
            max_length=6,
        ),
    )

    _break()
    print(
        "You entered these values to list:",
        menu.get_list("Enter integer list items", default=list(range(3)), cast_to=int),
    )

    _break()
    print(
        "You entered these values to tuple:",
        menu.get_tuple(
            "Enter utmost 3 float items", separator=" ", cast_to=float, max_length=3
        ),
    )

    _break()
    print(
        "You entered these values to set:",
        menu.get_set("Enter atleast 3 string items", min_length=3),
    )

    _break()
    tdy = datetime.now().date()
    print(
        "You entered the date",
        menu.get_date("Enter a date after today", tdy + timedelta(days=1), after=tdy),
    )
    print(
        "You entered the date",
        menu.get_date("Enter a date before today", before=tdy, format="%d-%m-%Y"),
    )

    _break()
    print("Hmm..." if menu.confirm("Are you sure to continue?") else "Let me ask again")
    print(
        "That's what I thought"
        if menu.confirm("Are you really sure to continue?", True)
        else "Uh... we are going on anyway"
    )
    print(
        "I'm kidding, we are continuing ;P"
        if menu.confirm("Do you really want to stop?", False)
        else "Wokay! Let's go..."
    )

    _break()
    print(
        "You chose index",
        menu.choose("Choose an option", ("Option 1", "Option 2"), "Option 2"),
    )
    print(
        "You chose ",
        menu.choose(
            "Choose another option",
            {"Option 1": "First option", "Option 2": "Second option"},
            1,
        ),
    )

    _break()
    print(
        "You chose",
        ", ".join(
            map(
                str,
                menu.choose_multi(
                    "Choose alteast 2 items from list",
                    ["Option 1", "Option 2", "Option 3", "Option 4"],
                    ["Option 2", "Option 4"],
                    min_length=2,
                ),
            )
        ),
    )
    print(
        "You chose",
        ", ".join(
            map(
                str,
                menu.choose_multi(
                    "Choose utmost 3 items from tuple",
                    ("Option 1", "Option 2", "Option 3", "Option 4"),
                    (0, 2),
                    max_length=3,
                ),
            )
        ),
    )
    print(
        "You chose",
        ", ".join(
            map(
                str,
                menu.choose_multi(
                    "Choose multiple items from dict",
                    {
                        "Option 1": "First option",
                        "Option 2": "Second option",
                        "Option 3": "Third option",
                        "Option 4": "Fourth option",
                    },
                    ["Option 2", "Option 3"],
                ),
            )
        ),
    )
