import pandas as pd

from itertools import batched
from multiprocessing import Pool
from worker import TaskProcessor


# Global processor instance for each worker process
global_processor = None

def init_worker():
    """Initialize a global TaskProcessor for the worker process."""
    global global_processor
    global_processor = TaskProcessor()

def process_batch(batch):
    """Process a batch using the global TaskProcessor instance."""
    return global_processor(batch)

if __name__ == '__main__':
    test_search_keys = pd.read_pickle('BR_AF_20250103.pkl')['doc-number'].sample(100)
    batched_keys = batched(test_search_keys, 5)

    # Initialize pool with per-worker processor
    with Pool(1, initializer=init_worker) as pool:
        results_packed = []
        try:
            results = pool.imap_unordered(process_batch, batched_keys)
            for res in results:
                results_packed.append(res)
                print('FINISH BATCH')
        except KeyboardInterrupt:  
            pd.to_pickle(pd.DataFrame(results_packed), 'results.pkl')
