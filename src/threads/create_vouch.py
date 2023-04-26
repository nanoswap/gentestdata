from typing import Self
import logging

log = logging.getLogger(__name__)
logging.basicConfig(filename=f'logs_{__name__}.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)



class CreateVouch():
    """Thread for randomly creating vouches."""

    thread_id: int
    name: str
    log: logging.Logger
    max_ticks: int
    tick_count: int

    def __init__(
            self: Self,
            thread_id: int,
            name: str,
            log: logging.Logger,
            max_ticks: int) -> None:
        """Construct."""
        self.thread_id = thread_id
        self.name = name
        self.log = log
        self.max_ticks = max_ticks
        self.tick_count = 0

    async def run(self: Self) -> None:
        """Start thread."""
        log.debug("Starting " + self.name)
        while self.tick_count < self.max_ticks:
            self.tick_count += 1
            log.debug("Running " + self.name)
            await self.tick()

        log.debug("Exiting " + self.name)

    async def tick(self: Self) -> None:
        """Iterate."""
        pass
