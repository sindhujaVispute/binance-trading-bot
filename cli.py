import typer
from rich import print
from rich.prompt import Prompt, Confirm

from bot.orders import OrderService
from bot.logging_config import setup_logger
from bot.exceptions import TradingBotException

app = typer.Typer()


@app.command()
def trade(
    symbol: str = typer.Option(None),
    side: str = typer.Option(None),
    order_type: str = typer.Option(None),
    quantity: float = typer.Option(None),
    price: float = typer.Option(None),
):
    setup_logger()

    try:
        if not symbol:
            symbol = Prompt.ask("Enter symbol (e.g. BTCUSDT)")

        if not side:
            side = Prompt.ask("Enter side (BUY/SELL)")

        if not order_type:
            order_type = Prompt.ask("Order type (MARKET/LIMIT/STOP_LIMIT)")

        if not quantity:
            quantity = float(Prompt.ask("Quantity"))

        if order_type.upper() in ["LIMIT", "STOP_LIMIT"] and not price:
            price = float(Prompt.ask("Price"))

        print("\n[bold yellow]Order Summary[/bold yellow]")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Type: {order_type}")
        print(f"Quantity: {quantity}")
        print(f"Price: {price}")

        if not Confirm.ask("Proceed with order?"):
            print("[red]Order cancelled[/red]")
            return

        # ✅ FIX: create service instance
        service = OrderService()

        response = service.create_order(
            symbol,
            side.upper(),
            order_type.upper(),
            quantity,
            price
        )

        print("\n[bold green]Response[/bold green]")
        print({
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty"),
            "avgPrice": response.get("avgPrice", "N/A")
        })

    except TradingBotException as e:
        print(f"[red]Error: {e}[/red]")
    except Exception as e:
        print(f"[red]Unexpected Error: {e}[/red]")


if __name__ == "__main__":
    app()