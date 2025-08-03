import psutil
from scrapping import *


search_keys = [
    'PI1105914',
    'PI0204016',
    'PI0706928',
    'PI0010489',
    '112013033315',
    '112013013920',
    '112015017565',
    'PI0115683',
    'PI0302240',
    '202013019554',
    '112017015313',
    '112016014626',
    '112019026983',
    '112019001898',
    '102016023421',
    'PI9504431',
    'PI1002654',
    'PI0914017',
    '112018074373',
    '112017006555',
    'PI9705474',
    '112013031248',
    '112018075083',
    '122015001060',
    '102013015305',
    'PI9713309',
    'PI0501830',
    'PI9000725',
    'PI0800931',
    '112020013741',
    '112017018714',
    'PI0213414',
    '112017001585',
    '102017026277',
    'PI9206835',
    '112018076396',
    'PI9307345',
    'PI0205770',
    'PI9709968',
    'PI9503562',
    'PI0709804',
    'PI9606526',
    '112012004219',
    '112014008724',
    '102014027883',
    'MU8300076',
    '112016023605',
    'PI9805536',
    '112012018681',
    '112016024039',
    'PI0510755',
    'PI9904530',
    'PI9707011',
    '112018012284',
    '112020020558',
    '112020012219',
    '102018073373',
    'PI1000158',
    'PI0716877',
    '112014015338',
    'PI8805665',
    'PI9604807',
    'PI9402682',
    'MU8703073',
    'PI0411262',
    '112018007743',
    'PI0519783',
    'PI0823367',
    '112019000839',
    'PI0410131',
    '112020004341',
    'PI0810061',
    'PI0317970',
    'PI0311862',
    'PI0906091',
    '112016004024',
    'MU8402374',
    'MU8601761',
    'PI9305134',
    'PI0013396',
    'MU7201873',
    '112017023010',
    'PI0717129',
    '112016028522',
    '102018014061',
    'PI0508158',
    'PI0417764',
    'MU9102535',
    '112016005489',
    'PI0113578',
    'PI0720422',
    '102019002806',
    '112015024729',
    '112012013137',
    'PI9007872',
    'PI0611942',
    'PI9808711',
    '112012011286',
    'PI0702835',
    'PI9204648',
    '102012015981',
    'MU8700924',
    'PI9306790',
    'PI9917493',
    'PI0201058',
    '102016028504',
    'PI9902180',
    '112015024145',
    'PI0515647',
    '112017015606',
    'PI9006034',
    'PI0002562',
    'PI0818055',
    'PI0105724',
    '112016000749',
    '112013002163',
    'PI9407738',
    'PI0517008',
    'PI9910093',
    'MU7302321',
    'PI9104607',
    'PI9305491',
    'PI0105159',
    '202019010821',
    'PI9909749',
    '112014020359',
    '112012006686',
    'PI1001058',
    'PI8900091',
    '102013033233',
    '112016019106',
    '112012028426',
    'PI9807848',
    'PI9607254',
    'PI0102524',
    'PI9301879',
    '112017017435',
    'PI8806368',
    'PI9705367',
    '102017018722',
    'PI0002094',
    'PI0307316',
    'PI9206470',
    'PI0206746',
    '112016012223',
    'PI0508161',
    '102017026156',
    '102016025114',
    'MU8300961',
    'PI0908032',
    'PI0002873',
    'PI9714610',
    '112012007503',
    'PI9407220',
    '112013018064',
    'PI1105526',
    'PI0810194',
    'PI9103095',
    '112012007786',
    'PI0312998',
    '112019005278',
    'PI0918975',
    '112016003714',
    'PI1010250',
    '112016008615',
    '112016001994',
    '112013009017',
    'MU7601980',
    '112018067531',
    '112017009969',
    'PI0011562',
    '112019002833',
    'PI9603476',
    '112018007618',
    '112017022227',
    '112019025928',
    'PI9403167',
    '122019013837',
    'PI0012472',
    '112020020450',
    'MU7700184',
    'PI0115916',
    'MU7700773',
    '112015021421',
    '102014017697',
    '112015017838',
    'PI1010225',
    '112013015616',
    'PI0503691',
    '112013033839',
    'PI0805188',
    '122019006130',
    '202012022519',
    'PI9501878',
    '112013026151',
    '112015022281',
    'PI0924575',
    'PI1011282',
    '112016016207',
    'PI0507075'
]


def get_process_memory_usage(pid):
    """Get memory usage (PSS) of a process and its children in MB."""
    try:
        process = psutil.Process(pid)
        memory_full_info = process.memory_full_info()
        memory_uss = memory_full_info.uss / (1024 ** 2)  # Convert to MB
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
        return 0.0


if __name__ == '__main__':

    driver, wait = setup_driver()
    driver.get("about:blank")
    
    webdriver_pid = driver.service.process.pid
    print(f"WebDriver PID: {webdriver_pid}")
    total_memory = get_process_memory_usage(webdriver_pid)
    print(f"LAUNCH,{total_memory[0]:.2f},{total_memory[1]:.2f},{total_memory[2]:.2f}")
    navigate_to_search_page(driver, wait)
    total_memory = get_process_memory_usage(webdriver_pid)
    print(f"NAVIGATE,{total_memory[0]:.2f},{total_memory[1]:.2f},{total_memory[2]:.2f}")
    
    for index, search_key in enumerate(search_keys):
        search_by_id(wait, search_key)
        total_memory = get_process_memory_usage(webdriver_pid)
        print(f"SEARCH KEY {search_key},{total_memory[0]:.2f},{total_memory[1]:.2f},{total_memory[2]:.2f}")
    
    driver.execute_script("window.myBigArray = Array(20000000).fill().map(Math.random);")
    total_memory = get_process_memory_usage(webdriver_pid)
    print(f"Total memory usage (random array launched): {total_memory:.2f} MB")
    driver.quit()
