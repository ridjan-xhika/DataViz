import sys
from src.sync_data import sync_covid_data
from src.dashboard import app

def main():
    print("DataViz - COVID-19 Dashboard")
    print("=" * 50)
    
    print("\n[1] Sync COVID-19 data to MySQL")
    print("[2] Run Dashboard")
    print("[3] Sync data and run dashboard")
    print("[4] Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        sync_covid_data()
    elif choice == "2":
        print("\nStarting dashboard on http://127.0.0.1:8050/")
        print("Press Ctrl+C to stop the server\n")
        app.run(debug=False)
    elif choice == "3":
        sync_covid_data()
        print("\nStarting dashboard on http://127.0.0.1:8050/")
        print("Press Ctrl+C to stop the server\n")
        app.run(debug=False)
    elif choice == "4":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid option")
        main()

if __name__ == "__main__":
    main()
