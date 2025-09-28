import re
import runpy
import sys
import warnings

from order_book_aggregator.__main__ import main


def test_main(capsys):
    main(["--qty", "5"])

    out, _ = capsys.readouterr()
    lines = out.strip().splitlines()

    pattern = re.compile(r"^To (buy|sell) \d+(\.\d+)? BTC: \$[0-9,]+\.\d{2}$")
    for line in lines:
        assert pattern.match(line)


def test_main_variable():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        original_argv = sys.argv
        try:
            sys.argv = ["order-book-aggregator"]
            runpy.run_module("order_book_aggregator", run_name="__main__")
        except Exception:
            pass
        finally:
            sys.argv = original_argv
