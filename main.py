import asyncio
import time

from app import Server, logger

HOMURAMC = "2024.08.15β"

startTime = time.time()
log = logger.get_module_logger("HomuraMC")

log.info(f"""HomuraMC v{HOMURAMC} is starting...""")


async def main():
    server = await asyncio.start_server(Server.serverLoop, "0.0.0.0", 25565)
    endTime = time.time()
    during = endTime - startTime
    log.info(f"loaded!({during}ms)")
    await server.serve_forever()


asyncio.run(main())
