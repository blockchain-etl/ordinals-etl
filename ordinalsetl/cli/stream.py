import click

from blockchainetl.logging_utils import logging_basic_config
from blockchainetl.streaming.streaming_utils import configure_logging, configure_signals
from blockchainetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-l', '--last-synced-block-file', default='last_synced_block.txt', type=str,
              help='The file with the last synced block number.')
@click.option('--lag', default=0, type=int, help='The number of blocks to lag behind the network.')
@click.option('-p', '--provider-uri', default='http://localhost:8080', type=str,
              help='The URI of the remote ord server node.')
@click.option('-o', '--output', type=str,
              help='Google PubSub topic path e.g. projects/your-project/topics/bitcoin_blockchain. '
                   'If not specified will print to console.')
@click.option('-s', '--start-block', default=None, type=int, help='Start block.')
@click.option('--period-seconds', default=10, type=int, help='How many seconds to sleep between syncs.')
@click.option('-b', '--batch-size', default=2, type=int, help='How many blocks to batch in single request.')
@click.option('-B', '--block-batch-size', default=10, type=int, help='How many blocks to batch in single sync round.')
@click.option('-w', '--max-workers', default=5, type=int, help='The number of workers.')
@click.option('--log-file', default=None, type=str, help='Log file.')
@click.option('--pid-file', default=None, type=str, help='pid file.')
def stream(last_synced_block_file, lag, provider_uri, output, start_block,
           period_seconds=10, batch_size=2, block_batch_size=10, max_workers=5, log_file=None, pid_file=None):
    """Streams all data types to console or Google Pub/Sub."""
    configure_logging(log_file)
    configure_signals()

    from ordinalsetl.rpc.ord_rpc import OrdRpc
    from ordinalsetl.streaming.ord_streamer_adapter import OrdStreamerAdapter
    from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter

    streamer_adapter = OrdStreamerAdapter(
        ord_rpc=ThreadLocalProxy(lambda: OrdRpc(provider_uri)),
        # TODO: Add supoort for Google Pub/Sub exporting.
        item_exporter=ConsoleItemExporter(),
        batch_size=batch_size,
        max_workers=max_workers
    )

    from blockchainetl.streaming.streamer import Streamer

    streamer = Streamer(
        blockchain_streamer_adapter=streamer_adapter,
        last_synced_block_file=last_synced_block_file,
        lag=lag,
        start_block=start_block,
        period_seconds=period_seconds,
        block_batch_size=block_batch_size,
        pid_file=pid_file,
    )
    streamer.stream()
