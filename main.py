import asyncio
import time

from app import Server, logger
from app.config import Config

HOMURAMC = "2024.08.15β"

startTime = time.time()
log = logger.get_module_logger("HomuraMC")

log.info(f"""Starting HomuraMC v{HOMURAMC}...""")

log.info("Loading properties from homura.yml")
config = Config().config
log.info("HomuraMC configuration file loaded successfully")


async def main():
    server = await asyncio.start_server(
        Server.serverLoop, config.server.ip, config.server.port
    )
    endTime = time.time()
    during = (endTime - startTime) * 1000
    during_s = during / 1000
    log.info(f"Done ({during_s}s)! listening on {config.server.ip}:{config.server.port}...")
    await server.serve_forever()


asyncio.run(main())
