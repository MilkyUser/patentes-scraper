from multiprocessing import Pool


class TaskProcessor:
    def __init__(self, pipe_conn):
        # TODO set driver, wait
        # TODO send via pipe browser main pid
        pass

    def restart_driver(self):
        # TODO reset driver, wait
        # TODO send via pipe previous and new browser main pid
        pass

    def __call__(self, item):
        # TODO batch search
        return f"{item} processed with base={self.base}"
    
    def __del__(self):
        # TODO closes pipe_conn
        # TODO quits driver
        pass


class TaskProcessor:

    def __init__(self, pipe_conn):
        # TODO set some important state
        # TODO set loop
        # TODO send some stats via pipe_conn
        pass

    def do_something(self):
        # TODO do something to state after event
        pass

    async def wait_for_event(self):
        
        while True:
            # Async wait for data in pipe
            await loop.run_in_executor(None, self.conn.recv)
            raise CustomException(some_data)

    async def background_work(self, stuff):
        try:
            # TODO some process
        Except CustomException:
            # Do something
        Finally:
            # returns something

    async def __call__(self, stuff):
        
        result = await asyncio.gather(
            background_work(),
            wait_for_event()
        )


if __name__ == '__main__':
# Setup communication pipes
    parent_conn1, child_conn1 = mp.Pipe()
    parent_conn2, child_conn2 = mp.Pipe()

    # Start workers
    workers = [
        mp.Process(target=TaskProcessor(child_conn1), args=(some_data)),
        mp.Process(target=TaskProcessor(child_conn2), args=(some_data)),
    ]
    
    for w in workers:
        w.start()
    

if __name__ == '__main__':
    with Pool(2) as pool:
        # Create new instance for each task (state not persisted)
        results = pool.map(TaskProcessor(pipe_conn=10), range(10))
        for res in results:
            print(res)
