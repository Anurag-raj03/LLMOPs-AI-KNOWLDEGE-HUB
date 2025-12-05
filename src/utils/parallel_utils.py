import concurrent.futures

def run_in_parallel(functions):
    results=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_func={executor.submit(fn): fn for fn in functions}
        for future in concurrent.futures.as_completed(future_to_func):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error in parallel task: {e}")

    return results               