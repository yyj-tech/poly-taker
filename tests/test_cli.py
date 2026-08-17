from poly_taker.cli import main


def test_cli_buy_runs_and_reports_fill(capsys):
    exit_code = main(["--side", "BUY", "--amount", "100", "--order-type", "FAK"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "status         : FILLED" in out
    assert "average price" in out


def test_cli_fok_rejected_when_too_large(capsys):
    exit_code = main(["--side", "BUY", "--amount", "100000", "--order-type", "FOK"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "status         : REJECTED" in out
