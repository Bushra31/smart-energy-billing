from system import *

def get_int(prompt,mn=1,mx=None):
    while True:
        try:
            v=int(input(prompt))
            if v<mn or (mx and v>mx): print(f"Enter {mn}-{mx}"); continue
            return v
        except: print("Enter valid integer")

def get_float(prompt, mn=0):
    while True:
        try:
            v=float(input(prompt))
            if v<mn: print(f"Enter >= {mn}"); continue
            return v
        except: print("Enter valid number")

def menu():
    print("SMART ENERGY BILLING SYSTEM"+"\n"+"-"*60)
    print("\nUSER: 1.Add 2.Remove 3.Summary")
    print("APPLIANCE: 4.View 5.Assign")
    print("SIMULATION: 6.Daily usage")
    print("BILLING: 7.Calculate 8.Set rates")
    print("VISUALIZATION: 9.Appliances 10.Trend 11.Peak/Normal")
    print("PREDICTION: 12.Next month")
    print("REPORTS: 13.Complete")
    print("SYSTEM: 14.Exit")

def main():
    sys=SystemInfo()
    while True:
        menu()
        c=get_int("Choice (1-14): ", 1, 14)
        if c==1:
            print("\nADD USER")
            add_user(sys, get_int("User ID: "), input("Name: ").strip())
        elif c==2:
            print("\nREMOVE USER")
            remove_user(sys, get_int("User ID: "))
        elif c==3:
            print("\nSUMMARY")
            show_summary(sys, get_int("User ID: "))
        elif c==4:
            print("\nAPPLIANCES")
            print(f"{'Appliance':<25} {'Power (W)':<15}\n" + "-"*40)
            for n, a in sys.appliances.items():print(f"{n:<25} {a.power_watts:<15}")
        elif c==5:
            print("\nASSIGN APPLIANCE")
            uid=get_int("User ID: ")
            if uid in sys.users:
                apps=list(sys.appliances.keys())
                print("\nAvailable:")
                for i, n in enumerate(apps, 1): print(f"  {i}. {n}")
                assign_appliance(sys, uid, apps[get_int(f"Select (1-{len(apps)}): ",1,len(apps)) - 1])
        elif c==6:
            print("\nSIMULATE")
            simulate_usage(sys, get_int("User ID: "), get_int("Days (1-365): ", 1, 365))
        elif c==7:
            print("\nBILL")
            calculate_bill(sys, get_int("User ID: "))
        elif c==8:
            print(f"\nRATES\nCurrent: Normal Rs.{sys.normal_rate}/kWh, Peak Rs.{sys.peak_rate}/kWh")
            print("Update: 1.Normal 2.Peak 3.Both")
            rc=get_int("Choice (1-3): ", 1, 3)
            n=get_float("New normal rate: ") if rc in [1, 3] else None
            p=get_float("New peak rate: ") if rc in [2, 3] else None
            set_rates(sys,n,p)
        elif c==9:
            viz_appliance(sys, get_int("User ID: "))
        elif c==10:
            viz_trend(sys, get_int("User ID: "))
        elif c==11:
            viz_peak_normal(sys, get_int("User ID: "))
        elif c==12:
            predict_next(sys, get_int("User ID: "))
        elif c==13:
            generate_report(sys)
        elif c==14:
            print("-"*30 + "\nExited")
            break
        input("\nPress Enter...")
if __name__ == "__main__":
    main()