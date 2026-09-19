# Custom ADTs (Stack, Queue, HashTable) used across the whole system
from Data_Stractures import Stack , Queue , HashTable
# Manually implemented sorting/searching algorithms
from Algorithms import bubble_sort , insertion_sort , selection_sort , binary_search , sequential_search
# pandas: used only to read the Excel seed dataset into DataFrames.
# I trained on this before (searched a real-world example on how pandas
# reads Excel sheets) and used that as the base for this function.
import pandas
import os

def load_excel_data(file_path):
    # sheet_name=None -> load every sheet into a dict {sheet_name: DataFrame}
    # skiprows=2 -> skip the first 2 header/title rows in the Excel file
    try:
        dfs = pandas.read_excel(file_path, sheet_name=None, skiprows=2)
        all_tables = {}
        
        for sheet_name, df in dfs.items():
            data_size = len(df)
            # Oversize the hash table a bit (1.5x) to reduce collisions
            if data_size > 0:
                size = int(data_size * 1.5)
            else:
                size = 10
                
            requests_sheet = HashTable(size)
            
            # iterrows() walks the DataFrame row by row (row.iloc[i] = column i)
            for _, row in df.iterrows():
                if pandas.notna(row.iloc[0]):  # skip empty ID cells
                    request_id = int(row.iloc[0])
                    request_data = {
                        "Request ID": request_id,
                        "Customer Name": row.iloc[1],
                        "Priority": row.iloc[2],
                        "Estimated Time": row.iloc[3],
                        "Status": row.iloc[4]
                    }
                    requests_sheet.put(request_id, request_data)
            
            all_tables[sheet_name] = requests_sheet
            
        return all_tables
        
    except Exception as e:
        print(f"Error Happened --> {e}")
        return None


# Seed data path - update this to match your local file location
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "System_Dataset.xlsx")
requests = load_excel_data(file_path)  # dict of {sheet_name: HashTable}

# Checks a request's fields before it's accepted into the system
def validate_request(requests_sheet, request_id, customer_name, priority, estimated_time, status):
    try:
        if not str(request_id).isdigit() or int(request_id) <= 1000:  # ID must be numeric and > 1000
            return False

        request_id = int(request_id)

        duplication = requests_sheet.get(request_id)  # reject duplicate IDs
        if duplication:
            return False

        if not customer_name or customer_name.strip() == "" or customer_name.lower() == "unknown":
            return False

        if not str(priority).isdigit() or not (1 <= int(priority) <= 5):
            return False

        if not str(estimated_time).isdigit() or int(estimated_time) <= 0:
            return False

        valid_statuses = ["pending", "processed", "closed", "rejected"]
        if status.lower() not in valid_statuses:
            return False

        return True

    except Exception as e:
        print(f"Error Happened --> {e}")
        return False


# Validates and adds a new request; rejected requests are still stored
# (with status "Rejected") instead of being silently dropped
def add_request(requests_sheet, waiting_queue, request_id, customer_name="unknown",
                priority="0", estimated_time="0", status="pending"):

    if str(request_id).isdigit():
        request_id = int(request_id)
    else:
        request_id = request_id

    if str(priority).isdigit():
        priority = int(priority)
    else:
        priority = 0

    if str(estimated_time).isdigit():
        estimated_time = int(estimated_time)
    else:
        estimated_time = 0
    try:
        if not validate_request(requests_sheet, request_id, customer_name, priority, estimated_time, status):
            rejected_record = {
                "Request ID": request_id,
                "Customer Name": customer_name,
                "Priority": priority,
                "Estimated Time": estimated_time,
                "Status": "Rejected"
            }

            if str(request_id).isdigit():
                requests_sheet.put(int(request_id), rejected_record)
            return False

        request_id = int(request_id)
        priority = int(priority)
        estimated_time = int(estimated_time)

        new_record = {
            "Request ID": request_id,
            "Customer Name": customer_name,
            "Priority": priority,
            "Estimated Time": estimated_time,
            "Status": status
        }

        requests_sheet.put(request_id, new_record)
        waiting_queue.enqueue(request_id)

        return new_record

    except Exception as e:
        print(f"Error in add_request --> {e}")
        return None



# Builds the initial waiting Queue from records already marked "pending"
def waiting_queue(requests):
    waiting = Queue()
    for req in requests:
        if req['Status'].lower() == 'pending':
            waiting.enqueue(req['Request ID'])
    return waiting


# Builds the initial processed Queue from records already marked "processed"
def processed_queue(requests):
    processed = Queue()
    for req in requests:
        if req['Status'].lower() == 'processed':
            processed.enqueue(req['Request ID'])
    return processed


# Global queues used by the whole program (seeded from the dataset)
waiting = waiting_queue(requests["Random Order"].get_all())
processed = processed_queue(requests["Random Order"].get_all())


# FIFO step: dequeues the next request and moves it to "Processed"
def process_request(waiting_list, processed_list, requests_table):
    if waiting_list.is_empty():
        return "There is no [Waiting List]"
    
    next_processed = waiting_list.dequeue()
    processed_list.enqueue(next_processed)
    
    record = requests_table.get(next_processed)
    if record:
        record['Status'] = 'Processed'

    return f"Request {next_processed} processed successfully"

# Runs the chosen manual sort (1=Bubble, 2=Selection, 3=Insertion) on a
# copy of the data so the original HashTable order isn't mutated
def sort_requests(requests_sheet, field, algorithm):
    data = requests_sheet.get_all()
    data_copy = data.copy()

    if algorithm == "1":
        sorted_data, comparisons, swaps, used_field = bubble_sort(data_copy, field)
    elif algorithm == "2":
        sorted_data, comparisons, swaps, used_field = selection_sort(data_copy, field)
    elif algorithm == "3":
        sorted_data, comparisons, swaps, used_field = insertion_sort(data_copy, field)
    else:
        return None

    return {
        "sorted_data": sorted_data,
        "comparisons": comparisons,
        "swaps": swaps,
        "field": used_field
    }

# Stack storing every search performed (most recent on top)
search_history = Stack()

# Runs Sequential (1), Binary (2), or Hash (3) search and logs the
# result into search_history
def search_requests(requests_sheet, target_id, method, field="Request ID"):
    try:
        target_id = int(target_id)
    except Exception as e :
        print(f"Invalid target ID --> {e}")
        return None

    if method == "1":
        data = requests_sheet.get_all()
        search = sequential_search(data, target_id, field)
        search["method"] = "Sequential"

    elif method == "2":
        data = requests_sheet.get_all()
        sorting = insertion_sort(data.copy() , field)  # binary search needs sorted data first
        sorted_data = sorting[0]
        search = binary_search(sorted_data, target_id, field)
        search["method"] = "Binary"

    elif method == "3":
        record = requests_sheet.get(target_id)
        if record:
            search = {"found": True, "index": None, "comparisons": 1}
        else:
            search = {"found": False, "index": None, "comparisons": 1}
        search["method"] = "Hash"

    else:
        return None

    history_record = {
        "target_id": target_id,
        "method": search["method"],
        "result": search,
        "comparisons": search["comparisons"]
    }
    search_history.push(history_record)

    return search


# Peek: just look at the last search without removing it
def view_last_search():
    if search_history.is_empty():
        return None
    return search_history.peek()


# Pop: remove and return the last search
def remove_last_search():
    if search_history.is_empty():
        return None
    return search_history.pop()


# Prints every record currently in the waiting Queue
def view_waiting_queue(waiting_list, requests_sheet):
    if waiting_list.is_empty():
        return None
    for req_id in waiting_list.queue:
        record = requests_sheet.get(req_id)
        print(record)


# Prints every record currently in the processed Queue
def view_processed_queue(processed_list, requests_sheet):
    if processed_list.is_empty():
        return None
    for req_id in processed_list.queue:
        record = requests_sheet.get(req_id)
        print(record)


# Prints stats from the last sort and last search done in this session
def show_statistics(sorting, searching):
    print("    ALGORITHM STATISTICS     ")
    print("      sort Statistics     ")
    if sorting is not None:
        print(f"Field Used: {sorting.get('field')}")
        print(f"Comparisons Count: {sorting.get('comparisons')}")
        print(f"Swaps Count: {sorting.get('swaps')}")
        print(f"Total Sorted Records: {len(sorting.get('sorted_data', []))}")
    else:
        print("No previous sort")

    print("\n     Search Statistics    ")
    if searching is not None:
        print(f"Search Method: {searching.get('method')}")
        print(f"Found Status: {searching.get('found')}")
        print(f"Comparisons Count: {searching.get('comparisons')}")
        if "index" in searching:
            print(f"Index in List: {searching.get('index')}")
    else:
        print("No previous search ")


def main():
    requests_table = requests["Random Order"]
    field_transition = {"1": "Request ID", "2": "Priority", "3": "Estimated Time"}  # maps menu choice -> field name
    sorting = None
    searching = None

    while True:
        print("\nSMART SERVICE CENTER ENGINE      ")
        print("   [1] Add incoming request")
        print("   [2] Process next request")
        print("   [3] Show waiting queue")
        print("   [4] Show processed requests")
        print("   [5] Sort requests")
        print("   [6] Sequential Search")
        print("   [7] Binary Search")
        print("   [8] Hash lookup")
        print("   [9] View/remove last search")
        print("   [10] Show algorithm statistics")
        print("   [11] Exit")

        choice = input("Choose an option: ").strip().replace(" ","")

        if choice == "1":
            request_id = input("Request ID: ")
            name = input("Customer Name: ")
            priority = input("Priority ((1-5) , 1 => Highest): ")
            estimated_time = input("Estimated Time: ")
            request = add_request(requests_table, waiting, request_id, name, priority, estimated_time)

            if request:
                print("\n--- Request Added ---")
                print(f"Request ID    : {request['Request ID']}")
                print(f"Customer Name : {request['Customer Name']}")
                print(f"Priority      : {request['Priority']}")
                print(f"Estimated Time: {request['Estimated Time']} min")
                print(f"Status        : {request['Status']}")
            else:
                print("\nRequest Rejected")

        elif choice == "2":
            print(process_request(waiting, processed, requests_table))

        elif choice == "3":
            print("\n--- Waiting Queue ---")
            if waiting.is_empty():
                print("Waiting queue is empty.")
            else:
                for req_id in waiting.queue:
                    record = requests_table.get(req_id)
                    print(f"\nRequest ID    : {record['Request ID']}")
                    print(f"Customer Name : {record['Customer Name']}")
                    print(f"Priority      : {record['Priority']}")
                    print(f"Estimated Time: {record['Estimated Time']} min")
                    print(f"Status        : {record['Status']}")

        elif choice == "4":
            print("\n--- Processed Requests ---")
            if processed.is_empty():
                print("Processed queue is empty.")
            else:
                for req_id in processed.queue:
                    record = requests_table.get(req_id)
                    print(f"\nRequest ID    : {record['Request ID']}")
                    print(f"Customer Name : {record['Customer Name']}")
                    print(f"Priority      : {record['Priority']}")
                    print(f"Estimated Time: {record['Estimated Time']} min")
                    print(f"Status        : {record['Status']}")

        elif choice == "5":
            field_choice = input("Sort by \n1. Request ID\n2. Priority\n3. Estimated Time\n--> ")
            field = field_transition.get(field_choice)
            if not field:
                print("Invalid field choice.")
                continue
            algorithms = input("Algorithm \n1. Bubble \n2. Selection \n3. Insertion\n--> ")
            sorting = sort_requests(requests_table, field, algorithms)
            if sorting:
                print("\nData sorted successfully.")
                print(f"Sorted by     : {sorting['field']}")
                print(f"Comparisons   : {sorting['comparisons']}")
                print(f"Swaps         : {sorting['swaps']}")

                show_data = input("\nDo you want to display the sorted data? (y/n): ").strip().lower()
                if show_data == "y":
                    print("\n--- Sorted Requests ---")
                    for record in sorting["sorted_data"]:
                        print(f"\nRequest ID    : {record['Request ID']}")
                        print(f"Customer Name : {record['Customer Name']}")
                        print(f"Priority      : {record['Priority']}")
                        print(f"Estimated Time: {record['Estimated Time']} min")
                        print(f"Status        : {record['Status']}")
            else:
                print("Sort failed - check your inputs.")

        elif choice == "6":
            target_id = input("Target ID: ")
            searching = search_requests(requests_table, target_id, "1")
            print("\n--- Sequential Search Result ---")
            if searching:
                print(f"Target ID  : {target_id}")
                print(f"Method     : {searching['method']}")
                print(f"Found      : {searching['found']}")
                if searching['found']:
                    print(f"Index      : {searching['index']}")
                print(f"Comparisons: {searching['comparisons']}")
            else:
                print("Search failed - invalid target ID.")

        elif choice == "7":
            target_id = input("Target ID: ")
            searching = search_requests(requests_table, target_id, "2")
            print("\n--- Binary Search Result ---")
            if searching:
                print(f"Target ID  : {target_id}")
                print(f"Method     : {searching['method']}")
                print(f"Found      : {searching['found']}")
                if searching['found']:
                    print(f"Index      : {searching['index']}")
                else:
                    print(f"Insert Pos : {searching['insert_position']}")
                print(f"Comparisons: {searching['comparisons']}")
            else:
                print("Search failed - invalid target ID.")

        elif choice == "8":
            target_id = input("Target ID: ")
            searching = search_requests(requests_table, target_id, "3")
            print("\n--- Hash Lookup Result ---")
            if searching:
                print(f"Target ID  : {target_id}")
                print(f"Method     : {searching['method']}")
                print(f"Found      : {searching['found']}")
                print(f"Comparisons: {searching['comparisons']}")
            else:
                print("Search failed - invalid target ID.")


        elif choice == "9":
            act = input("(1) View last\n(2) Remove last\n--> ")
            if act == "1":
                result = view_last_search()
                if result:
                    print("\n--- Last Search ---")
                    print(f"Target ID  : {result['target_id']}")
                    print(f"Method     : {result['method']}")
                    print(f"Comparisons: {result['comparisons']}")
                    print(f"Result     : {result['result']}")
                else:
                    print("No search history")
            elif act == "2":
                last = view_last_search()
                if not last:
                    print("No search history")
                else:
                    print("\n--- Last Search (about to be removed) ---")
                    print(f"Target ID  : {last['target_id']}")
                    print(f"Method     : {last['method']}")
                    print(f"Comparisons: {last['comparisons']}")

                    confirm = input("Are you sure you want to remove this search? (y/n): ").strip().lower()
                    if confirm == "y":
                        result = remove_last_search()
                        print("\n--- Removed Search ---")
                        print(f"Target ID  : {result['target_id']}")
                        print(f"Method     : {result['method']}")
                        print(f"Comparisons: {result['comparisons']}")
                        print(f"Result     : {result['result']}")
                    else:
                        print("Cancelled - search not removed.")

        elif choice == "10":
            show_statistics(sorting, searching)

        elif choice == "11":
            print("THANK YOU FOR YOUR TIME\nSEE YOU AGAIN!")
            break

        else:
            print("Invalid choice, please try again.")


main()