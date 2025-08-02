import asyncio
import psutil


from scraping import *
from typing import Sequence


DEFAULT_MEMORY_LIMITS = {'rss': float('inf'), 'pss': 700, 'uss': float('inf')}


def _get_process_memory_usage(pid: int) -> list[float]:
    """Get memory usage (USS, PSS, RSS) of a process and its children in MB."""
    try:
        process = psutil.Process(pid)
        memory_full_info = process.memory_full_info()
        memory_uss = memory_full_info.uss / (1024 ** 2)
        memory_pss = memory_full_info.pss / (1024 ** 2)
        memory_rss = memory_full_info.rss / (1024 ** 2)
        children = process.children(recursive=True)  # Get all child processes
        _total_memory = [memory_uss, memory_pss, memory_rss] 
        for child in children:
            try:
                child_memory_full_info = child.memory_full_info()
                _total_memory[0] += child_memory_full_info.uss  / (1024 ** 2)
                _total_memory[1] += child_memory_full_info.pss  / (1024 ** 2)
                _total_memory[2] += child_memory_full_info.rss  / (1024 ** 2)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return _total_memory
    except psutil.NoSuchProcess:
        return [0.0, 0.0, 0.0]


class TaskProcessor:

    def __init__(self):
        self.driver = None 
        self.wait   = None 
        self.driver_pid = None
        self.loop = None
        self.monitor = None

    def __call__(self, batch: Sequence[str], memory_limits=DEFAULT_MEMORY_LIMITS):
        
        results = asyncio.run(self.run(batch, memory_limits))
        return results

    def __del__(self):
        if self.driver is not None: 
            self.driver.quit() # type: ignore

    async def run(self, batch, memory_limits=DEFAULT_MEMORY_LIMITS):
        self.loop =  asyncio.get_running_loop()
        
        if self.driver is None:
            print("START NEW DRIVER")
            self.reset_driver()
        
        self.monitor = asyncio.create_task(self._monitor_driver_memory(memory_limits))
        results = await asyncio.gather(self.async_batch_search(batch))
        self.monitor.cancel()
        results = results[0]
        return results

    def _poll_driver_memory_usage_greater_than(self, memory_limits):
        driver_memory = _get_process_memory_usage(self.driver_pid) # type: ignore
        print(f'DRIVER {self.driver_pid}: POLLED MEMORY: {driver_memory}')
        driver_memory_map = {'uss': 0, 'pss': 1, 'rss': 2}
        if any([driver_memory[driver_memory_map[arg]] > memory_limit for arg, memory_limit in memory_limits.items()]):
            return True
        return False            

    async def _monitor_driver_memory(self, memory_limits) -> None:
        
        while True:
            try:
                if self._poll_driver_memory_usage_greater_than(memory_limits): # type: ignore
                    self.reset_driver()
                await asyncio.sleep(2)
            except asyncio.exceptions.CancelledError:
                break
            
    def reset_driver(self):
        if self.driver is not None:
            self.driver.quit()
            print(f'DRIVER {self.driver_pid}: RESET')
        else:    
            self.driver, self.wait = setup_driver()
            navigate_to_search_page(self.driver, self.wait)
            self.driver_pid = self.driver.service.process.pid # type: ignore
            print(f'DRIVER {self.driver_pid}: SET')

    async def async_batch_search(self, batch):
        results = []
        try:
            results = await self.loop.run_in_executor( # type: ignore
                None, 
                lambda: list(batch_search(self.driver, self.wait, batch))
            )
        except:
            self.reset_driver()
            raise
        return results
