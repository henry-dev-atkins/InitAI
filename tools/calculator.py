#!/usr/bin/env python3
"""Evaluate one safe arithmetic expression with Decimal values."""

from __future__ import annotations

import argparse
import ast
from decimal import Decimal, DecimalException, localcontext
import sys
from typing import Final


class CalculatorError(ValueError):
    """Report an invalid or unsupported calculator expression."""


MAX_PRECISION: Final[int] = 28


def _evaluate(node: ast.AST, source: str) -> Decimal:
    """Evaluate one approved AST node using Decimal arithmetic.

    Args:
        node: Parsed expression node to evaluate.
        source: Original expression used to preserve decimal literals.

    Returns:
        The Decimal value represented by the node.

    Raises:
        CalculatorError: If the node is outside the arithmetic grammar or
            Decimal arithmetic cannot evaluate it.
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculatorError("only decimal numbers are supported")
        literal = ast.get_source_segment(source, node)
        if literal is None:
            raise CalculatorError("could not read numeric literal")
        try:
            return Decimal(literal)
        except DecimalException as exc:
            raise CalculatorError("invalid decimal number") from exc

    if isinstance(node, ast.UnaryOp):
        value = _evaluate(node.operand, source)
        if isinstance(node.op, ast.UAdd):
            return value
        if isinstance(node.op, ast.USub):
            return -value
        raise CalculatorError("only unary plus and minus are supported")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left, source)
        right = _evaluate(node.right, source)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        raise CalculatorError("only +, -, * and / are supported")

    raise CalculatorError("only numbers, parentheses and arithmetic operators are supported")


def evaluate_expression(expression: str) -> Decimal:
    """Evaluate one arithmetic expression without executing arbitrary code.

    Args:
        expression: Text containing Decimal literals, parentheses and the
            operators +, -, * and /.

    Returns:
        The calculated Decimal value, using 28 significant digits.

    Raises:
        CalculatorError: If the expression is empty, malformed or unsupported.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise CalculatorError("an arithmetic expression is required")

    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError as exc:
        raise CalculatorError("invalid arithmetic expression") from exc

    try:
        with localcontext() as context:
            context.prec = MAX_PRECISION
            return _evaluate(tree.body, expression.strip())
    except (DecimalException, ZeroDivisionError) as exc:
        raise CalculatorError("Decimal arithmetic failed") from exc


def main() -> int:
    """Read one expression, print its result and return a process status."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "expression",
        nargs="*",
        help="arithmetic expression; read one expression from stdin when omitted",
    )
    args = parser.parse_args()
    expression = " ".join(args.expression) if args.expression else sys.stdin.read()

    try:
        result = evaluate_expression(expression)
    except CalculatorError as exc:
        parser.error(str(exc))

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
