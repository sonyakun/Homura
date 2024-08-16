import asyncio
import time
import sys

from app import Server, logger
from app.config import Config

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

HOMURAMC = "2024.08.16β"

startTime = time.time()
log = logger.get_module_logger("HomuraMC")

log.info(f"""Starting HomuraMC v{HOMURAMC}...""")

log.info("Loading properties from homura.yml")
config = Config().config
log.info("HomuraMC configuration file loaded successfully")


async def main():
    server = await asyncio.start_server(
        Server.serverLoop, config.listen.ip, config.listen.port
    )
    endTime = time.time()
    during = (endTime - startTime) * 1000
    during_s = during / 1000
    log.info(
        f"Done ({during_s}s)! listening on {config.listen.ip}:{config.listen.port}..."
    )
    await server.serve_forever()


asyncio.run(main())
