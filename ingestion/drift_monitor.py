import asyncio
import time

from .async_collector import collect_all_resources_async
from .state_snapshot import (
    create_state_snapshot,
    find_changed_resources,
)


async def monitor_drift(poll_interval=2, max_cycles=None):
    """
    Continuously poll AWS and detect resource changes.

    poll_interval:
        Seconds between AWS polls.

    max_cycles:
        Optional number of polling cycles.
        None means continuous monitoring.
    """

    print("Starting AeroDrift monitor...")

    initial_data = await collect_all_resources_async()
    previous_snapshot = create_state_snapshot(initial_data)

    cycle = 0

    while max_cycles is None or cycle < max_cycles:
        await asyncio.sleep(poll_interval)

        poll_started = time.perf_counter()

        current_data = await collect_all_resources_async()
        current_snapshot = create_state_snapshot(current_data)

        changes = find_changed_resources(
            previous_snapshot,
            current_snapshot,
        )

        detection_time = time.perf_counter() - poll_started

        if changes:
            print("DRIFT DETECTED")

            for change in changes:
                print(change)

            print(
                f"Detection processing time: "
                f"{detection_time:.3f} seconds"
            )
        else:
            print("No drift detected")

        previous_snapshot = current_snapshot
        cycle += 1